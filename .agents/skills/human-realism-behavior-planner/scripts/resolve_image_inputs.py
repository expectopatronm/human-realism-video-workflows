"""Inventory model-neutral timeline and semantic image inputs."""

import argparse
import hashlib
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
DEFAULT_ROOT = REPO / "generation_artefacts" / "input" / "images"
SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}
SEMANTIC_ROLES = {
    "subject_identity", "face_identity", "body_identity", "clothing",
    "accessory", "object", "environment", "lighting", "style", "pose",
    "composition",
}
CONFIGURATIONS = {
    (1, 0, 0, 0): "first_frame_only",
    (0, 1, 0, 0): "last_frame_only",
    (0, 0, 1, 0): "intermediate_frames_only",
    (0, 0, 0, 1): "reference_frames_only",
    (1, 1, 0, 0): "first_and_last",
    (1, 0, 1, 0): "first_and_intermediate",
    (1, 0, 0, 1): "first_and_references",
    (0, 1, 1, 0): "last_and_intermediate",
    (0, 1, 0, 1): "last_and_references",
    (0, 0, 1, 1): "intermediate_and_references",
    (1, 1, 1, 0): "first_last_and_intermediate",
    (1, 1, 0, 1): "first_last_and_references",
    (1, 0, 1, 1): "first_intermediate_and_references",
    (0, 1, 1, 1): "last_intermediate_and_references",
    (1, 1, 1, 1): "first_last_intermediate_and_references",
}


def natural_key(path):
    """Return a stable, case-insensitive natural filename key."""
    return tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in re.split(r"(\d+)", path.name.casefold())
    )


def images(directory):
    """Return supported images in deterministic order."""
    if not directory.exists():
        return []
    metadata = {"timings.json", "roles.json"}
    files = [path for path in directory.iterdir() if path.is_file() and path.name not in metadata]
    invalid = [path.name for path in files if path.suffix.casefold() not in SUPPORTED]
    if invalid:
        raise ValueError(f"unsupported media in {directory.name}: {', '.join(sorted(invalid))}")
    return sorted(files, key=natural_key)


def load_json(path):
    """Load an object-valued JSON sidecar."""
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain an object")
    return value


def resolve_intermediate(paths, directory, duration, questions):
    """Resolve explicit interior-frame timing without inventing missing times."""
    if not paths:
        return []
    timing_path = directory / "timings.json"
    if not timing_path.is_file():
        questions.append("What time should each intermediate frame occupy?")
        return [
            {"path": str(path), "time_seconds": None, "normalized_time": None,
             "timing_source": "missing"}
            for path in paths
        ]
    timing = load_json(timing_path)
    if set(timing) != {path.name for path in paths}:
        raise ValueError("timings.json keys must exactly match intermediate-frame filenames")
    result = []
    for path in paths:
        raw = timing[path.name]
        if isinstance(raw, (int, float)) and not isinstance(raw, bool):
            value, unit = raw, "seconds"
        elif isinstance(raw, dict) and set(raw) == {"value", "unit"}:
            value, unit = raw["value"], raw["unit"]
        else:
            raise ValueError(f"invalid timing for {path.name}")
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"timing value for {path.name} must be numeric")
        if unit == "normalized":
            if not 0 < value < 1:
                raise ValueError(f"normalized timing for {path.name} must be inside (0, 1)")
            normalized, seconds = value, round(value * duration, 6) if duration else None
        elif unit == "seconds":
            if value <= 0:
                raise ValueError(f"seconds timing for {path.name} must be positive")
            seconds = value
            normalized = round(value / duration, 9) if duration else None
            if duration and value >= duration:
                raise ValueError(f"seconds timing for {path.name} must be inside the clip")
            if duration is None:
                questions.append(f"What is the clip duration needed to place {path.name} at {value} seconds?")
        else:
            raise ValueError(f"timing unit for {path.name} must be seconds or normalized")
        result.append({
            "path": str(path), "time_seconds": seconds,
            "normalized_time": normalized, "timing_source": "sidecar",
        })
    known = [item["normalized_time"] for item in result if item["normalized_time"] is not None]
    if len(known) != len(set(known)):
        raise ValueError("intermediate frame times must be unique")
    return sorted(result, key=lambda item: (
        item["normalized_time"] is None,
        item["normalized_time"] if item["normalized_time"] is not None else item["path"],
    ))


def resolve_references(paths, directory, questions):
    """Resolve optional semantic-role declarations for unpinned references."""
    if not paths:
        return []
    role_path = directory / "roles.json"
    declarations = load_json(role_path) if role_path.is_file() else {}
    if set(declarations) - {path.name for path in paths}:
        raise ValueError("roles.json contains filenames absent from reference_frames")
    result = []
    for path in paths:
        declaration = declarations.get(path.name, {})
        if not isinstance(declaration, dict) or set(declaration) - {"roles", "targets", "notes"}:
            raise ValueError(f"invalid role declaration for {path.name}")
        roles = declaration.get("roles", [])
        targets = declaration.get("targets", [])
        notes = declaration.get("notes")
        if not isinstance(roles, list) or set(roles) - SEMANTIC_ROLES:
            raise ValueError(f"invalid semantic role for {path.name}")
        if not isinstance(targets, list) or any(not isinstance(item, str) or not item for item in targets):
            raise ValueError(f"targets for {path.name} must be non-empty strings")
        if notes is not None and (not isinstance(notes, str) or not notes):
            raise ValueError(f"notes for {path.name} must be null or non-empty text")
        if not roles:
            questions.append(
                f"What should reference frame {path.name} control: identity, appearance, pose, object, environment, lighting, style, or composition?"
            )
        subject_roles = {
            "subject_identity", "face_identity", "body_identity", "clothing",
            "accessory", "pose",
        }
        if set(roles) & subject_roles and not targets:
            questions.append(f"Which subject should reference frame {path.name} control?")
        if "object" in roles and not targets:
            questions.append(f"Which object should reference frame {path.name} control?")
        result.append({"path": str(path), "roles": roles, "targets": targets, "notes": notes})
    return result


def duplicate_role_questions(groups):
    """Find byte-identical files assigned to different role folders."""
    seen = {}
    questions = []
    for role, paths in groups.items():
        for path in paths:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            seen.setdefault(digest, []).append((role, path.name))
    for entries in seen.values():
        roles = {role for role, _ in entries}
        if len(roles) > 1:
            listing = ", ".join(f"{role}/{name}" for role, name in entries)
            questions.append(f"The same image appears in multiple roles ({listing}). Is that dual role intentional?")
    return questions


def resolve(root, duration=None):
    """Resolve the repository image folders into a model-neutral input manifest.

    Args:
        root: Folder containing first, last, intermediate, and reference directories.
        duration: Confirmed clip duration in seconds, when known.

    Returns:
        A serializable manifest with the configuration and unresolved questions.
    """
    root = Path(root).resolve()
    if duration is not None and duration <= 0:
        raise ValueError("duration must be positive")
    groups = {
        "first_frame": images(root / "first_frame"),
        "last_frame": images(root / "last_frame"),
        "intermediate_frames": images(root / "intermediate_frames"),
        "reference_frames": images(root / "reference_frames"),
    }
    if len(groups["first_frame"]) > 1:
        raise ValueError("first_frame accepts at most one image")
    if len(groups["last_frame"]) > 1:
        raise ValueError("last_frame accepts at most one image")
    signature = tuple(int(bool(groups[name])) for name in groups)
    if signature not in CONFIGURATIONS:
        raise ValueError("provide at least one image in a supported role folder")
    questions = duplicate_role_questions(groups)
    intermediate = resolve_intermediate(
        groups["intermediate_frames"], root / "intermediate_frames", duration, questions
    )
    references = resolve_references(
        groups["reference_frames"], root / "reference_frames", questions
    )
    return {
        "configuration": CONFIGURATIONS[signature],
        "duration_seconds": duration,
        "first_frame": str(groups["first_frame"][0]) if groups["first_frame"] else None,
        "last_frame": str(groups["last_frame"][0]) if groups["last_frame"] else None,
        "intermediate_frames": intermediate,
        "reference_frames": references,
        "questions": list(dict.fromkeys(questions)),
        "ready_for_planner_review": not questions,
    }


def main():
    """Run the image-input resolver as a command-line utility."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = resolve(args.root, args.duration)
        text = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
