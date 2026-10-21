"""Exercise valid and broken scene specifications."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import validate_spec


def sample():
    """Build a minimal traceable still scene.

    Returns:
        A scene specification used by the validator tests.
    """
    return {
        "schema_version": "1.0",
        "scene_id": "scene-01",
        "references": [
            {"id": "ref-01", "source": "sample-image.png", "observation": "A visible hand rests on a table.", "confidence": "high"}
        ],
        "subjects": [
            {"id": "person-01", "reference_ids": ["ref-01"], "identity_constraints": ["Preserve the visible hand."], "appearance_changes": []}
        ],
        "intent": {
            "request": "Keep the subject still.",
            "setting": None,
            "camera": "Static close shot",
            "duration": None,
            "initial_state": "Hand rests on table.",
            "beats": [{"id": "beat-01", "action": "Remain still.", "subject_ids": ["person-01"]}],
            "final_state": "Hand remains on table."
        },
        "global_rules": [
            {"id": "G01", "constraint": "Preserve visible identity."},
            {"id": "G18", "constraint": "Maintain table contact."}
        ],
        "components": [{
            "subject_id": "person-01",
            "component_id": "14.01",
            "name": "Hands — General",
            "applicability": "visible-static",
            "priority": "high",
            "reference_observation": {
                "observed": ["Hand rests on table."], "unknown": [],
                "reference_ids": ["ref-01"], "confidence": "high"
            },
            "scene_intent": {"role": "Maintain contact.", "initial_state": "Resting.", "final_state": "Resting."},
            "appearance_preservation": {"invariants": ["Visible shape."], "allowed_changes": []},
            "primary_motion": {"required": "no", "description": "Remain still.", "timing": None, "constraints": []},
            "secondary_motion_and_physics": {"required": "no", "drivers": [], "behavior": []},
            "deformation_and_interaction": {"requirements": [], "contacts": ["Table."], "occlusion": None},
            "temporal_continuity": {"invariants": ["Stable position."], "allowed_changes": [], "occlusion_recovery": None},
            "negative_constraints": ["No sliding."],
            "traceability": {
                "global_rule_ids": ["G01", "G18"], "reference_ids": ["ref-01"],
                "assumptions": [], "unresolved_conflicts": []
            }
        }],
        "assumptions": [],
        "unresolved_conflicts": []
    }


class ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(validate_spec.SCHEMA.read_text(encoding="utf-8"))

    def errors(self, spec):
        errors = validate_spec.check_schema(spec, self.schema, self.schema)
        if not errors:
            errors += validate_spec.check_traceability(spec)
        return errors

    def test_valid_scene(self):
        self.assertEqual(self.errors(sample()), [])

    def test_unknown_component_is_rejected(self):
        spec = sample()
        spec["components"][0]["component_id"] = "99.99"
        self.assertTrue(any("unknown Level 2 ID" in error for error in self.errors(spec)))

    def test_broken_reference_is_rejected(self):
        spec = sample()
        spec["components"][0]["reference_observation"]["reference_ids"] = ["missing"]
        self.assertTrue(any("unknown reference" in error for error in self.errors(spec)))

    def test_evaluation_field_is_rejected(self):
        spec = sample()
        spec["components"][0]["evaluation_status"] = "pass"
        self.assertTrue(any("unexpected evaluation_status" in error for error in self.errors(spec)))

    def test_cli_and_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scene_spec.json"
            path.write_text(json.dumps(sample()), encoding="utf-8")
            command = [sys.executable, str(Path(__file__).with_name("validate_spec.py")), str(path)]
            self.assertEqual(subprocess.run(command, capture_output=True, text=True).returncode, 0)
            path.write_text('{"scene_id":"a","scene_id":"b"}', encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate JSON key", result.stderr)


if __name__ == "__main__":
    unittest.main()
