"""Validate a prompt-and-images package for manual Google Flow generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {
    "execution_surface", "model", "duration_seconds", "aspect_ratio",
    "prompt_file", "image_only", "image_inputs", "video_inputs", "postprocess",
}


def validate(directory: Path) -> list[str]:
    """Return package errors for a compiled Flow handoff.

    Args:
        directory: Directory containing the prompt and Flow manifest.

    Returns:
        Human-readable validation errors.
    """
    errors: list[str] = []
    manifest_path = directory / "google_flow_settings.json"
    prompt_path = directory / "gemini_omni_1_1_prompt.txt"
    if not manifest_path.is_file():
        return ["missing google_flow_settings.json"]
    if not prompt_path.is_file() or not prompt_path.read_text(encoding="utf-8").strip():
        errors.append("missing or empty gemini_omni_1_1_prompt.txt")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"invalid google_flow_settings.json: {exc}"]
    missing = REQUIRED - set(manifest)
    if missing:
        errors.append(f"manifest missing keys: {', '.join(sorted(missing))}")
        return errors
    if manifest["execution_surface"] != "google_flow_web":
        errors.append("execution_surface must be google_flow_web")
    if manifest["model"] != "gemini_omni_1_1":
        errors.append("model must be gemini_omni_1_1")
    if manifest["aspect_ratio"] not in {"9:16", "16:9"}:
        errors.append("aspect_ratio must be 9:16 or 16:9")
    if not isinstance(manifest["duration_seconds"], (int, float)) or manifest["duration_seconds"] <= 0:
        errors.append("duration_seconds must be positive")
    if manifest["image_only"] is not True or manifest["video_inputs"]:
        errors.append("Flow handoff must be image-only with no video inputs")
    if manifest["prompt_file"] != prompt_path.name:
        errors.append("prompt_file must identify gemini_omni_1_1_prompt.txt")
    for index, image in enumerate(manifest["image_inputs"]):
        label = f"image_inputs[{index}]"
        for key in ("path", "role", "width", "height", "aspect_match", "strict_composition"):
            if key not in image:
                errors.append(f"{label} missing {key}")
        source = Path(image.get("path", ""))
        if not source.is_file():
            errors.append(f"{label} is unavailable: {source}")
        if image.get("strict_composition") and not image.get("aspect_match"):
            errors.append(f"{label} strict frame does not match selected aspect ratio")
    return errors


def main() -> int:
    """Run Flow package validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    errors = validate(args.directory)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Valid Google Flow package: {args.directory.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
