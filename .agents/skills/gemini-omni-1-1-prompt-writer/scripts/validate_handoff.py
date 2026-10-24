"""Validate a Human Realism Behavior Planner handoff for prompt compilation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = ("scene_spec.json", "scene_spec.md", "generation_prompt.txt")
REQUIRED_ROOT_KEYS = {
    "schema_version",
    "scene_id",
    "references",
    "input_plan",
    "subjects",
    "intent",
    "behavior_plan",
    "spatial_plan",
    "scene_physics",
    "motion_schedule",
    "unresolved_conflicts",
}


def validate_handoff(output_dir: Path) -> list[str]:
    """Return actionable validation errors for a planner output directory.

    Args:
        output_dir: Directory containing the canonical planner artifacts.

    Returns:
        A list of validation errors. An empty list means the handoff is ready.
    """
    errors: list[str] = []
    for name in REQUIRED_FILES:
        path = output_dir / name
        if not path.is_file():
            errors.append(f"missing required artifact: {name}")
        elif path.stat().st_size == 0:
            errors.append(f"required artifact is empty: {name}")

    spec_path = output_dir / "scene_spec.json"
    if not spec_path.is_file() or spec_path.stat().st_size == 0:
        return errors

    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"scene_spec.json is not valid UTF-8 JSON: {exc}")
        return errors

    missing_keys = sorted(REQUIRED_ROOT_KEYS - set(spec))
    if missing_keys:
        errors.append(f"scene_spec.json is missing root keys: {', '.join(missing_keys)}")
    if spec.get("schema_version") != "1.7":
        errors.append("scene_spec.json must use schema_version 1.7")
    if not spec.get("scene_id"):
        errors.append("scene_spec.json has no scene_id")
    if not spec.get("references"):
        errors.append("scene_spec.json has no image references")
    for reference in spec.get("references") or []:
        source = reference.get("source")
        if source and Path(source).is_absolute() and not Path(source).is_file():
            errors.append(f"local image reference is unavailable: {source}")
    if spec.get("unresolved_conflicts"):
        errors.append("scene_spec.json contains unresolved_conflicts")

    readable_path = output_dir / "scene_spec.md"
    if readable_path.is_file() and spec.get("scene_id"):
        try:
            readable = readable_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"scene_spec.md is not readable UTF-8: {exc}")
        else:
            if spec["scene_id"] not in readable:
                errors.append("scene_spec.md does not identify the JSON scene_id")

    input_plan = spec.get("input_plan") or {}
    anchors = input_plan.get("frame_anchors") or []
    semantic_refs = input_plan.get("semantic_references") or []
    if not anchors and not semantic_refs:
        errors.append("input_plan has neither timeline anchors nor semantic references")

    schedule_path = output_dir / "motion_schedule_resolved.json"
    if schedule_path.is_file():
        try:
            schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"motion_schedule_resolved.json is invalid: {exc}")
        else:
            if schedule.get("scene_id") != spec.get("scene_id"):
                errors.append("resolved schedule scene_id does not match scene_spec.json")

    return errors


def main() -> int:
    """Run the command-line validator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    errors = validate_handoff(args.output_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Handoff valid: {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
