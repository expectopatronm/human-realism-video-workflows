"""Resolve normalized scene motion windows into destination seconds."""

import argparse
import json
from pathlib import Path

import validate_spec


def seconds(window, duration):
    """Convert a normalized window to rounded destination seconds."""
    return [round(point * duration, 3) for point in window]


def resolve(spec, duration):
    """Compile a validated model-independent motion schedule for one duration."""
    if duration <= 0:
        raise ValueError("duration must be positive")
    planned_duration = spec["input_plan"]["duration_seconds"]
    if planned_duration is not None and abs(planned_duration - duration) > 1e-9:
        raise ValueError("duration conflicts with the confirmed input-plan duration")
    result = {
        "scene_id": spec["scene_id"],
        "duration_seconds": duration,
        "input_plan": {
            **spec["input_plan"],
            "duration_seconds": duration,
            "frame_anchors": [
                {
                    **anchor,
                    "resolved_time_seconds": round(anchor["normalized_time"] * duration, 3),
                }
                for anchor in spec["input_plan"]["frame_anchors"]
            ],
            "segments": [
                {**segment, "window_seconds": seconds(segment["window"], duration)}
                for segment in spec["input_plan"]["segments"]
            ],
        },
        "spatial_plan": {
            **spec["spatial_plan"],
            "camera_track": {
                **spec["spatial_plan"]["camera_track"],
                "window_seconds": seconds(
                    spec["spatial_plan"]["camera_track"]["window"], duration
                ),
            },
            "occlusion_events": [
                {**event, "window_seconds": seconds(event["window"], duration)}
                for event in spec["spatial_plan"]["occlusion_events"]
            ],
        },
        "scene_physics": {
            **spec["scene_physics"],
            "force_fields": [
                {**field, "window_seconds": seconds(field["window"], duration)}
                for field in spec["scene_physics"]["force_fields"]
            ],
            "environmental_drivers": [
                {**driver, "window_seconds": seconds(driver["window"], duration)}
                for driver in spec["scene_physics"]["environmental_drivers"]
            ],
        },
        "subjects": [],
    }
    plans = {plan["subject_id"]: plan for plan in spec["behavior_plan"]}
    for schedule in spec["motion_schedule"]:
        plan = plans[schedule["subject_id"]]
        subject = {
            "subject_id": schedule["subject_id"],
            "behavior_plan": {
                **plan,
                "channels": [
                    {
                        **channel,
                        "window_seconds": seconds(channel["window"], duration) if channel["window"] else None,
                        "phases": [
                            {**phase, "window_seconds": seconds(phase["window"], duration)}
                            for phase in channel["phases"]
                        ],
                    }
                    for channel in plan["channels"]
                ],
                "facial_plan": {
                    **plan["facial_plan"],
                    "action_units": [
                        {**unit, "onset_seconds": round(unit["onset"] * duration, 3),
                         "apex_seconds": round(unit["apex"] * duration, 3),
                         "offset_seconds": round(unit["offset"] * duration, 3)}
                        for unit in plan["facial_plan"]["action_units"]
                    ],
                },
            },
            "primary_phases": [
                {
                    **phase,
                    "window_seconds": seconds(phase["window"], duration),
                    "active_motion_windows_seconds": [
                        seconds(window, duration) for window in phase["active_motion_windows"]
                    ],
                    "dwell_windows_seconds": [
                        seconds(window, duration) for window in phase["dwell_windows"]
                    ],
                }
                for phase in schedule["primary_phases"]
            ],
            "articulated_actions": schedule["articulated_actions"],
            "vitality_tracks": [
                {
                    **track,
                    "windows_seconds": [seconds(window, duration) for window in track["windows"]],
                }
                for track in schedule["vitality_tracks"]
            ],
            "secondary_tracks": [
                {
                    **track,
                    "windows_seconds": [seconds(window, duration) for window in track["windows"]],
                }
                for track in schedule["secondary_tracks"]
            ],
            "protected_windows": [
                {
                    **window,
                    "window_seconds": seconds(window["window"], duration),
                }
                for window in schedule["protected_windows"]
            ],
            "priority_order": schedule["priority_order"],
            "coordination_rules": schedule["coordination_rules"],
            "anti_synchrony_rules": schedule["anti_synchrony_rules"],
        }
        result["subjects"].append(subject)
    return result


def load_valid_spec(path):
    """Load a scene specification and run structural and semantic validation."""
    schema = json.loads(
        validate_spec.SCHEMA.read_text(encoding="utf-8-sig"),
        object_pairs_hook=validate_spec.unique_object,
    )
    spec = json.loads(
        path.read_text(encoding="utf-8-sig"),
        object_pairs_hook=validate_spec.unique_object,
    )
    errors = validate_spec.check_schema(spec, schema, schema)
    if not errors:
        errors = validate_spec.check_traceability(spec)
    if errors:
        raise ValueError("; ".join(errors))
    return spec


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--duration", required=True, type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = resolve(load_valid_spec(args.spec), args.duration)
        text = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
