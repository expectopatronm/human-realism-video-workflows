"""Test model-neutral image-input resolution."""

import json
import tempfile
import unittest
from itertools import product
from pathlib import Path

from resolve_image_inputs import CONFIGURATIONS, resolve


class ImageInputResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for name in ("first_frame", "last_frame", "intermediate_frames", "reference_frames"):
            (self.root / name).mkdir()

    def tearDown(self):
        self.temporary.cleanup()

    def add(self, folder, name, content=None):
        """Add a small test image placeholder."""
        path = self.root / folder / name
        path.write_bytes(content or f"{folder}/{name}".encode())
        return path

    def test_all_fifteen_nonempty_configurations(self):
        for signature in (bits for bits in product((0, 1), repeat=4) if any(bits)):
            with self.subTest(signature=signature):
                for folder in self.root.iterdir():
                    for path in folder.iterdir():
                        path.unlink()
                if signature[0]:
                    self.add("first_frame", "first.png")
                if signature[1]:
                    self.add("last_frame", "last.png")
                if signature[2]:
                    self.add("intermediate_frames", "middle.png")
                    (self.root / "intermediate_frames" / "timings.json").write_text(
                        json.dumps({"middle.png": {"value": 0.5, "unit": "normalized"}}),
                        encoding="utf-8",
                    )
                if signature[3]:
                    self.add("reference_frames", "identity.png")
                    (self.root / "reference_frames" / "roles.json").write_text(
                        json.dumps({"identity.png": {"roles": ["subject_identity"], "targets": ["person-01"]}}),
                        encoding="utf-8",
                    )
                self.assertEqual(resolve(self.root)["configuration"], CONFIGURATIONS[signature])

    def test_missing_intermediate_timing_becomes_question(self):
        self.add("intermediate_frames", "middle.png")
        result = resolve(self.root)
        self.assertFalse(result["ready_for_planner_review"])
        self.assertIn("What time", result["questions"][0])

    def test_seconds_timing_needs_duration(self):
        self.add("intermediate_frames", "middle.png")
        (self.root / "intermediate_frames" / "timings.json").write_text(
            json.dumps({"middle.png": 2.0}), encoding="utf-8"
        )
        result = resolve(self.root)
        self.assertIsNone(result["intermediate_frames"][0]["normalized_time"])
        self.assertTrue(result["questions"])

    def test_resolves_seconds_and_normalized_timing(self):
        self.add("intermediate_frames", "a.png")
        self.add("intermediate_frames", "b.png")
        (self.root / "intermediate_frames" / "timings.json").write_text(
            json.dumps({
                "a.png": {"value": 0.25, "unit": "normalized"},
                "b.png": {"value": 6, "unit": "seconds"},
            }), encoding="utf-8"
        )
        frames = resolve(self.root, 8)["intermediate_frames"]
        self.assertEqual([item["normalized_time"] for item in frames], [0.25, 0.75])
        self.assertEqual([item["time_seconds"] for item in frames], [2.0, 6])

    def test_unassigned_reference_role_becomes_question(self):
        self.add("reference_frames", "person.png")
        result = resolve(self.root)
        self.assertFalse(result["ready_for_planner_review"])
        self.assertIn("What should reference frame", result["questions"][0])

    def test_subject_reference_without_target_becomes_question(self):
        self.add("reference_frames", "person.png")
        (self.root / "reference_frames" / "roles.json").write_text(
            json.dumps({"person.png": {"roles": ["subject_identity"]}}), encoding="utf-8"
        )
        result = resolve(self.root)
        self.assertTrue(any("Which subject" in question for question in result["questions"]))

    def test_duplicate_cross_role_image_needs_confirmation(self):
        self.add("first_frame", "first.png", b"same")
        self.add("reference_frames", "identity.png", b"same")
        (self.root / "reference_frames" / "roles.json").write_text(
            json.dumps({"identity.png": {"roles": ["subject_identity"]}}), encoding="utf-8"
        )
        result = resolve(self.root)
        self.assertTrue(any("dual role" in question for question in result["questions"]))

    def test_rejects_multiple_first_frames(self):
        self.add("first_frame", "a.png")
        self.add("first_frame", "b.png")
        with self.assertRaisesRegex(ValueError, "at most one"):
            resolve(self.root)


if __name__ == "__main__":
    unittest.main()
