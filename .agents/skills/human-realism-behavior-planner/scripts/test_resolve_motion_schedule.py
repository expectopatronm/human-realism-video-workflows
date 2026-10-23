"""Test normalized motion-schedule resolution."""

import unittest

from resolve_motion_schedule import resolve
from test_validate_spec import sample


class ScheduleResolutionTests(unittest.TestCase):
    def test_resolves_normalized_windows_to_seconds(self):
        spec = sample()
        phase = spec["motion_schedule"][0]["primary_phases"][0]
        phase["window"] = [0.25, 0.75]
        phase["dwell_windows"] = [[0.25, 0.75]]
        result = resolve(spec, 12)
        resolved = result["subjects"][0]["primary_phases"][0]
        self.assertEqual(resolved["window_seconds"], [3.0, 9.0])
        self.assertEqual(resolved["dwell_windows_seconds"], [[3.0, 9.0]])

    def test_rejects_nonpositive_duration(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            resolve(sample(), 0)

    def test_carries_behavior_spatial_plan_and_physics_into_handoff(self):
        spec = sample()
        result = resolve(spec, 12)
        channel = result["subjects"][0]["behavior_plan"]["channels"][3]
        self.assertEqual(channel["window_seconds"], [0.0, 12.0])
        self.assertEqual(result["spatial_plan"]["camera_track"]["window_seconds"], [0.0, 12.0])
        self.assertEqual(result["spatial_plan"]["subject_tracks"][0]["path"], "No spatial travel.")
        self.assertEqual(result["scene_physics"]["support_contacts"][0]["surface"], "table")

    def test_resolves_input_anchors_and_segments(self):
        result = resolve(sample(), 12)["input_plan"]
        self.assertEqual(result["frame_anchors"][0]["resolved_time_seconds"], 0.0)
        self.assertEqual(result["segments"][0]["window_seconds"], [0.0, 12.0])

    def test_rejects_duration_conflicting_with_input_plan(self):
        spec = sample()
        spec["input_plan"]["duration_seconds"] = 10
        spec["input_plan"]["duration_source"] = "user"
        with self.assertRaisesRegex(ValueError, "input-plan duration"):
            resolve(spec, 12)

    def test_resolves_occlusion_windows(self):
        spec = sample()
        spec["spatial_plan"]["occlusion_events"] = [{
            "id": "occlusion-01",
            "subject_id": "person-01",
            "occluder": "Foreground object.",
            "window": [0.25, 0.5],
            "reappearance_constraint": "Restore the same visible hand identity."
        }]
        event = resolve(spec, 12)["spatial_plan"]["occlusion_events"][0]
        self.assertEqual(event["window_seconds"], [3.0, 6.0])

    def test_resolves_protected_windows_and_preserves_priority(self):
        spec = sample()
        schedule = spec["motion_schedule"][0]
        schedule["protected_windows"] = [{
            "id": "quiet-1",
            "window": [0.25, 0.5],
            "purpose": "Make a subtle cue legible.",
            "permitted_motion": ["Quiet cue."],
            "suppressed_motion": ["Large action."]
        }]
        result = resolve(spec, 12)["subjects"][0]
        self.assertEqual(result["protected_windows"][0]["window_seconds"], [3.0, 6.0])
        self.assertEqual(result["priority_order"], ["primary_action"])


if __name__ == "__main__":
    unittest.main()
