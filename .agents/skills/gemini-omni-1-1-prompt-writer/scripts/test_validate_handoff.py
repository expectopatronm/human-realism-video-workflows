"""Tests for the Gemini Omni planner-handoff validator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from validate_handoff import validate_handoff


def valid_spec() -> dict:
    """Return the smallest structurally valid handoff specification."""
    return {
        "schema_version": "1.7",
        "scene_id": "scene-1",
        "references": [{"id": "ref-1"}],
        "input_plan": {"frame_anchors": [{"id": "first"}], "semantic_references": []},
        "subjects": [],
        "intent": {},
        "behavior_plan": [],
        "spatial_plan": {},
        "scene_physics": {},
        "motion_schedule": [],
        "unresolved_conflicts": [],
    }


class ValidateHandoffTests(unittest.TestCase):
    def make_handoff(self, root: Path, spec: dict | None = None) -> None:
        """Create the three canonical planner artifacts for a test."""
        (root / "scene_spec.json").write_text(
            json.dumps(spec or valid_spec()), encoding="utf-8"
        )
        (root / "scene_spec.md").write_text("# Scene scene-1", encoding="utf-8")
        (root / "generation_prompt.txt").write_text("Generate the scene.", encoding="utf-8")

    def test_accepts_valid_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_handoff(root)
            self.assertEqual(validate_handoff(root), [])

    def test_rejects_missing_artifact_and_unresolved_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = valid_spec()
            spec["unresolved_conflicts"] = ["Choose an ending."]
            self.make_handoff(root, spec)
            (root / "generation_prompt.txt").unlink()
            errors = validate_handoff(root)
            self.assertIn("missing required artifact: generation_prompt.txt", errors)
            self.assertIn("scene_spec.json contains unresolved_conflicts", errors)

    def test_rejects_mismatched_resolved_schedule(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_handoff(root)
            (root / "motion_schedule_resolved.json").write_text(
                json.dumps({"scene_id": "other-scene"}), encoding="utf-8"
            )
            self.assertIn(
                "resolved schedule scene_id does not match scene_spec.json",
                validate_handoff(root),
            )

    def test_rejects_mismatched_readable_spec(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_handoff(root)
            (root / "scene_spec.md").write_text("# A different scene", encoding="utf-8")
            self.assertIn(
                "scene_spec.md does not identify the JSON scene_id",
                validate_handoff(root),
            )


if __name__ == "__main__":
    unittest.main()
