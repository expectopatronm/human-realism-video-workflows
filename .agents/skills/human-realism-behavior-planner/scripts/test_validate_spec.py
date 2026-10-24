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
        "schema_version": "1.7",
        "scene_id": "scene-01",
        "references": [
            {"id": "ref-01", "source": "sample-image.png", "observation": "A visible hand rests on a table.", "confidence": "high"}
        ],
        "input_plan": {
            "configuration": "first_frame_only",
            "duration_seconds": None,
            "duration_source": "unknown",
            "frame_anchors": [{
                "id": "anchor-first", "reference_id": "ref-01",
                "role": "first_frame", "normalized_time": 0.0,
                "time_seconds": 0.0, "timing_source": "endpoint",
                "adherence": "exact_requested_state", "subject_ids": ["person-01"],
                "beat_ids": ["beat-01"], "preserve": ["Observed hand pose and framing."]
            }],
            "semantic_references": [],
            "segments": [{
                "id": "segment-01", "window": [0.0, 1.0],
                "from_anchor_id": "anchor-first", "to_anchor_id": None,
                "beat_ids": ["beat-01"],
                "transition_intent": "Continue the held pose from the opening frame.",
                "continuity_constraints": ["Keep the hand supported by the table."],
                "feasibility": "plausible"
            }],
            "dual_role_reference_ids": [], "role_conflicts": [], "loop_intent": "none"
        },
        "motion_sources": [],
        "subjects": [
            {
                "id": "person-01", "reference_ids": ["ref-01"],
                "identity_constraints": ["Preserve the visible hand."],
                "identity_anchors": [{
                    "region": "hands", "reference_ids": ["ref-01"],
                    "invariant": "Preserve the visible hand shape and appearance.",
                    "visibility": "visible"
                }],
                "view_coverage": ["Close view of one hand."],
                "unseen_region_policy": "Do not invent or reveal unsupported identity details.",
                "appearance_changes": []
            }
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
        "realism_selection": [{
            "subject_id": "person-01",
            "subject_state": "awake",
            "realism_mode": "intentional-stillness",
            "baseline_cues": [
                {
                    "cue": cue,
                    "status": "not_visible",
                    "rationale": "The close framing shows only the hand.",
                    "visible_effects": [],
                    "timing_strategy": None,
                    "variability": None
                }
                for cue in [
                    "respiration", "blinking", "ocular_fixation", "facial_tonus",
                    "postural_micro_adjustment"
                ]
            ],
            "repetition_variation": {
                "repeated_action": False,
                "status": "not_applicable",
                "dimensions": [],
                "timing_strategy": None,
                "rationale": "The requested still pose has no repeated action."
            }
        }],
        "behavior_plan": [{
            "subject_id": "person-01",
            "channels": [{
                "channel": channel, "status": "held" if channel == "gesture" else "not_visible",
                "beat_ids": ["beat-01"] if channel == "gesture" else [],
                "behavior": "Hand remains in its observed pose." if channel == "gesture" else None,
                "window": [0.0, 1.0] if channel == "gesture" else None,
                "phases": [], "sync_points": [],
                "sync_with": []
            } for channel in ["gaze", "face", "head", "gesture", "posture", "locomotion", "speech"]],
            "movement_quality": [{
                "beat_id": "beat-01", "body": "Hand stays supported.",
                "initiator": "No intentional motion.", "space": "No travel.",
                "pathway": "stationary", "range": "none", "shape": "Held hand shape.",
                "effort": {key: "unspecified" for key in ["weight", "space", "time", "flow"]},
                "evidence": "requested"
            }],
            "facial_plan": {"visibility": "not_visible", "expression_change": False,
                            "action_units": [], "combinations": [],
                            "rationale": "The face is outside the frame."},
            "physiology_states": [{
                "cue": cue, "status": "not_visible", "driver": None,
                "visible_effects": [], "timing_relation": None,
                "rationale": "The close frame shows only the hand."
            } for cue in ["swallowing", "exertion", "fatigue", "autonomic_response", "speech_breath"]],
            "physiology_couplings": [], "passive_elements": [], "dynamics_links": [],
            "coordination_rules": ["Keep the hand supported by the table."]
        }],
        "spatial_plan": {
            "camera_track": {
                "status": "static", "path": "No camera translation.",
                "orientation": "Fixed toward the hand.", "framing": "Close shot of the hand.",
                "depth_change": "none", "window": [0.0, 1.0],
                "subject_motion_decoupled": True
            },
            "subject_tracks": [{
                "subject_id": "person-01", "beat_ids": ["beat-01"],
                "path": "No spatial travel.", "depth_change": "none",
                "orientation_change": "None.", "support_relation": "Hand remains supported by the table.",
                "reference_coverage": "sufficient"
            }],
            "interactions": [], "occlusion_events": []
        },
        "scene_physics": {
            "gravity": "Ordinary downward gravity.",
            "objects": [{"id": "table-01", "description": "Stable table", "mass_class": "unknown",
                         "mobility": "fixed"}],
            "force_fields": [{"id": "gravity-01", "kind": "gravity", "strength": "unknown",
                              "direction": "downward", "window": [0.0, 1.0]}],
            "support_contacts": [{"id": "contact-01", "subject_id": "person-01",
                                  "object_id": "table-01", "surface": "table", "mode": "support",
                                  "friction": "unknown", "beat_ids": ["beat-01"],
                                  "continuity": "No sliding."}],
            "environmental_drivers": [], "visual_dependencies": []
        },
        "motion_schedule": [{
            "subject_id": "person-01",
            "primary_phases": [{
                "beat_id": "beat-01",
                "window": [0.0, 1.0],
                "phase_kind": "dwell",
                "active_motion_windows": [],
                "dwell_windows": [[0.0, 1.0]],
                "tempo": {
                    "source": "natural_default",
                    "descriptor": "still",
                    "slow_motion": False,
                    "evidence": "The request explicitly asks the hand to remain still."
                },
                "velocity_profile": {
                    "onset": "No intentional onset.",
                    "acceleration": "None.",
                    "peak": "None.",
                    "deceleration": "None.",
                    "arrival": "Maintain the existing contact."
                },
                "action_ids": [],
                "repetition_group": None,
                "variation_dimensions": [],
                "variation_note": None
            }],
            "articulated_actions": [],
            "vitality_tracks": [{
                "cue": cue,
                "status": "not_visible",
                "priority": "low",
                "mode": "inactive",
                "windows": [],
                "count_range": None,
                "event_duration_seconds": None,
                "phase_relation": None,
                "variability": None
            } for cue in [
                "respiration", "blinking", "ocular_fixation", "facial_tonus",
                "postural_micro_adjustment"
            ]],
            "secondary_tracks": [],
            "protected_windows": [],
            "priority_order": ["primary_action"],
            "coordination_rules": ["Keep the visible hand in stable table contact."],
            "anti_synchrony_rules": []
        }],
        "intent_resolutions": [],
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

    def test_missing_behavior_channel_is_rejected(self):
        spec = sample()
        spec["behavior_plan"][0]["channels"].pop()
        self.assertTrue(any("channels" in error for error in self.errors(spec)))

    def test_expression_change_needs_action_units(self):
        spec = sample()
        face = spec["behavior_plan"][0]["facial_plan"]
        face.update(visibility="visible", expression_change=True)
        self.assertTrue(any("expression change needs action units" in error for error in self.errors(spec)))

    def test_action_unit_phase_order_is_checked(self):
        spec = sample()
        face = spec["behavior_plan"][0]["facial_plan"]
        face.update(visibility="visible", expression_change=True, action_units=[{
            "code": "AU12", "beat_ids": ["beat-01"], "laterality": "bilateral", "intensity": "B",
            "onset": 0.6, "apex": 0.4, "offset": 0.8,
            "visible_effect": "Lip corners rise.", "confidence": "medium"
        }])
        self.assertTrue(any("out of order" in error for error in self.errors(spec)))

    def test_secondary_track_needs_dynamics_link(self):
        spec = sample()
        spec["motion_schedule"][0]["secondary_tracks"].append({
            "id": "cloth-01", "driver": "hand motion", "response": "sleeve settles",
            "windows": [[0.1, 0.3]], "lag": "short", "damping": "gentle", "settling": "ends by 0.3"
        })
        self.assertTrue(any("dynamics_links must match" in error for error in self.errors(spec)))

    def test_behavior_phase_sync_must_match_timing(self):
        spec = sample()
        channels = spec["behavior_plan"][0]["channels"]
        gesture = next(item for item in channels if item["channel"] == "gesture")
        gesture["phases"] = [{"name": "stroke", "window": [0.2, 0.4]}]
        gesture["sync_points"] = [{
            "own_phase": "stroke", "with_channel": "gaze",
            "other_phase": "hold", "relation": "before"
        }]
        gaze = next(item for item in channels if item["channel"] == "gaze")
        gaze["phases"] = [{"name": "hold", "window": [0.1, 0.3]}]
        self.assertTrue(any("sync point relation contradicts timing" in error for error in self.errors(spec)))

    def test_extended_physiology_needs_causal_details(self):
        spec = sample()
        state = spec["behavior_plan"][0]["physiology_states"][1]
        state["status"] = "required"
        self.assertTrue(any("active physiology needs driver" in error for error in self.errors(spec)))

    def test_contact_object_must_exist(self):
        spec = sample()
        spec["scene_physics"]["support_contacts"][0]["object_id"] = "missing"
        self.assertTrue(any("contact cites unknown object" in error for error in self.errors(spec)))

    def test_visual_dependency_driver_must_exist(self):
        spec = sample()
        spec["scene_physics"]["visual_dependencies"].append({
            "driver_kind": "contact", "driver_ref": "missing",
            "cause": "Hand contact changes", "effect_kind": "shadow",
            "effect": "Contact shadow changes", "beat_ids": ["beat-01"]
        })
        self.assertTrue(any("visual dependency has unknown driver" in error for error in self.errors(spec)))

    def test_affected_passive_element_needs_track(self):
        spec = sample()
        spec["behavior_plan"][0]["passive_elements"].append({
            "id": "sleeve-01", "material": "fabric", "status": "affected",
            "dynamics_track_ids": [], "rationale": "The sleeve should follow the hand."
        })
        self.assertTrue(any("affected element needs dynamics track" in error for error in self.errors(spec)))

    def test_identity_anchor_must_use_subject_reference(self):
        spec = sample()
        spec["subjects"][0]["identity_anchors"][0]["reference_ids"] = ["missing"]
        self.assertTrue(any("identity anchor uses an unassigned reference" in error for error in self.errors(spec)))

    def test_subject_track_must_cover_subject_beats(self):
        spec = sample()
        spec["spatial_plan"]["subject_tracks"][0]["beat_ids"] = []
        self.assertTrue(any("track must cover every subject beat" in error for error in self.errors(spec)))

    def test_human_object_interaction_needs_known_object(self):
        spec = sample()
        spec["spatial_plan"]["interactions"].append({
            "id": "interaction-01", "kind": "human_object",
            "subject_ids": ["person-01"], "object_ids": ["missing"],
            "beat_ids": ["beat-01"], "affordance": "support",
            "approach": None, "contact": "Hand remains in contact.",
            "manipulation": None, "release": None, "reaction_dependencies": []
        })
        errors = self.errors(spec)
        self.assertTrue(any("unknown object" in error for error in errors))

    def test_static_camera_cannot_change_depth(self):
        spec = sample()
        spec["spatial_plan"]["camera_track"]["depth_change"] = "approach"
        self.assertTrue(any("static camera cannot change depth" in error for error in self.errors(spec)))

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

    def test_all_baseline_cues_are_required(self):
        spec = sample()
        cues = spec["realism_selection"][0]["baseline_cues"]
        cues[-1] = json.loads(json.dumps(cues[0]))
        self.assertTrue(any("baseline cues must cover" in error for error in self.errors(spec)))

    def test_active_blink_requires_g16_and_eyelid_component(self):
        spec = sample()
        blink = spec["realism_selection"][0]["baseline_cues"][1]
        blink.update({
            "status": "required",
            "rationale": "The awake subject's visible eyes need physiological closure.",
            "visible_effects": ["Brief coordinated upper-eyelid closure and reopening."],
            "timing_strategy": "One non-periodic blink during the held gaze.",
            "variability": "Do not place the blink at a beat midpoint."
        })
        errors = self.errors(spec)
        self.assertTrue(any("requires G16" in error for error in errors))
        self.assertTrue(any("no supporting Level 2 component" in error for error in errors))

    def test_active_blink_with_dependencies_is_valid(self):
        spec = sample()
        spec["global_rules"].append({
            "id": "G16",
            "constraint": "Preserve restrained biological micro-movement."
        })
        blink = spec["realism_selection"][0]["baseline_cues"][1]
        blink.update({
            "status": "required",
            "rationale": "The awake subject's visible eyes need physiological closure.",
            "visible_effects": ["Brief coordinated upper-eyelid closure and reopening."],
            "timing_strategy": "One non-periodic blink during the held gaze.",
            "variability": "Do not place the blink at a beat midpoint."
        })
        spec["motion_schedule"][0]["vitality_tracks"][1].update({
            "status": "required",
            "priority": "high",
            "mode": "event",
            "windows": [[0.25, 0.75]],
            "count_range": [1, 1],
            "event_duration_seconds": [0.12, 0.25],
            "phase_relation": "Place one blink away from the exact midpoint.",
            "variability": "The window permits non-clocklike placement."
        })
        spec["motion_schedule"][0]["priority_order"] = ["primary_action", "blinking"]
        eyelid = json.loads(json.dumps(spec["components"][0]))
        eyelid.update({
            "component_id": "03.02",
            "name": "Upper Eyelids",
            "applicability": "active",
            "reference_observation": {
                "observed": ["Eyes are visible and open."],
                "unknown": [],
                "reference_ids": ["ref-01"],
                "confidence": "high"
            },
            "primary_motion": {
                "required": "yes",
                "description": "Close and reopen once in a natural blink.",
                "timing": "Non-periodic during the held gaze.",
                "constraints": ["Preserve gaze direction across the blink."]
            },
            "traceability": {
                "global_rule_ids": ["G01", "G16"],
                "reference_ids": ["ref-01"],
                "assumptions": [],
                "unresolved_conflicts": []
            }
        })
        spec["components"].append(eyelid)
        self.assertEqual(self.errors(spec), [])

    def test_repetition_requires_bounded_variation(self):
        spec = sample()
        spec["realism_selection"][0]["repetition_variation"] = {
            "repeated_action": True,
            "status": "required",
            "dimensions": ["interval"],
            "timing_strategy": "Unequal intervals within the requested pace.",
            "rationale": "Human repetitions should not be mechanically identical."
        }
        self.assertTrue(any("vary at least two dimensions" in error for error in self.errors(spec)))

    def test_living_subject_cannot_mark_vitality_not_applicable(self):
        spec = sample()
        spec["realism_selection"][0]["baseline_cues"][0]["status"] = "not_applicable"
        self.assertTrue(any("living or unknown cues cannot be not_applicable" in error for error in self.errors(spec)))

    def test_repeated_action_needs_variation_disposition(self):
        spec = sample()
        spec["realism_selection"][0]["repetition_variation"]["repeated_action"] = True
        self.assertTrue(any("needs a variation disposition" in error for error in self.errors(spec)))

    def test_motion_schedule_must_cover_subject_beats_in_order(self):
        spec = sample()
        spec["motion_schedule"][0]["primary_phases"][0]["beat_id"] = "missing"
        self.assertTrue(any("primary phases" in error for error in self.errors(spec)))

    def test_active_vitality_track_needs_a_window(self):
        spec = sample()
        cue = spec["realism_selection"][0]["baseline_cues"][0]
        cue.update({
            "status": "required",
            "visible_effects": ["Subtle movement."],
            "timing_strategy": "Continuous.",
            "variability": "Low amplitude."
        })
        track = spec["motion_schedule"][0]["vitality_tracks"][0]
        track.update({
            "status": "required",
            "mode": "continuous",
            "phase_relation": "Independent of the held pose.",
            "variability": "Low amplitude."
        })
        errors = self.errors(spec)
        self.assertTrue(any("active cue needs scheduled windows" in error for error in errors))

    def test_invalid_motion_window_is_rejected(self):
        spec = sample()
        spec["motion_schedule"][0]["primary_phases"][0]["window"] = [0.8, 0.2]
        self.assertTrue(any("invalid window" in error for error in self.errors(spec)))

    def test_event_track_requires_duration_range(self):
        spec = sample()
        track = spec["motion_schedule"][0]["vitality_tracks"][1]
        track.update({
            "status": "required",
            "mode": "event",
            "windows": [[0.2, 0.4]],
            "count_range": [1, 1],
            "phase_relation": "Use the quiet window.",
            "variability": "Avoid the midpoint."
        })
        self.assertTrue(any("duration range" in error for error in self.errors(spec)))

    def test_priority_order_covers_active_and_secondary_tracks(self):
        spec = sample()
        spec["motion_schedule"][0]["secondary_tracks"] = [{
            "id": "cloth_response",
            "driver": "Body movement",
            "response": "Cloth follows the body.",
            "windows": [[0.0, 1.0]],
            "lag": "Slight lag.",
            "damping": "Strong damping.",
            "settling": "Settles before the end."
        }]
        self.assertTrue(any("priority_order" in error for error in self.errors(spec)))

    def test_protected_windows_must_not_overlap(self):
        spec = sample()
        spec["motion_schedule"][0]["protected_windows"] = [
            {
                "id": "quiet-1", "window": [0.1, 0.3], "purpose": "Expose a subtle cue.",
                "permitted_motion": ["Quiet cue."], "suppressed_motion": ["Large action."]
            },
            {
                "id": "quiet-2", "window": [0.2, 0.4], "purpose": "Expose another cue.",
                "permitted_motion": ["Quiet cue."], "suppressed_motion": ["Large action."]
            }
        ]
        self.assertTrue(any("protected" in error for error in self.errors(spec)))

    def test_protected_window_must_use_existing_dwell(self):
        spec = sample()
        phase = spec["motion_schedule"][0]["primary_phases"][0]
        phase["dwell_windows"] = [[0.0, 0.2]]
        spec["motion_schedule"][0]["protected_windows"] = [{
            "id": "invented-pause",
            "window": [0.4, 0.6],
            "purpose": "Expose a subtle cue.",
            "permitted_motion": ["Quiet cue."],
            "suppressed_motion": ["No additional suppression."]
        }]
        self.assertTrue(any("existing dwell" in error for error in self.errors(spec)))

    def test_active_and_dwell_windows_cannot_overlap(self):
        spec = sample()
        phase = spec["motion_schedule"][0]["primary_phases"][0]
        phase.update({
            "phase_kind": "composite",
            "active_motion_windows": [[0.2, 0.7]],
            "dwell_windows": [[0.6, 1.0]]
        })
        self.assertTrue(any("active and dwell windows overlap" in error for error in self.errors(spec)))

    def test_reference_tempo_requires_motion_source(self):
        spec = sample()
        phase = spec["motion_schedule"][0]["primary_phases"][0]
        phase["tempo"].update({
            "source": "reference_video",
            "descriptor": "reference_matched",
            "evidence": "Match the source recording."
        })
        self.assertTrue(any("missing motion source" in error for error in self.errors(spec)))

    def test_motion_source_duration_must_be_positive(self):
        spec = sample()
        spec["motion_sources"] = [{
            "id": "motion-01",
            "source": "source.mp4",
            "role": "motion_only",
            "duration_seconds": 0,
            "observation": "A visible motion reference.",
            "excluded_attributes": [],
            "confidence": "high"
        }]
        self.assertTrue(any("must be greater" in error for error in self.errors(spec)))

    def test_moving_phase_requires_articulated_action(self):
        spec = sample()
        phase = spec["motion_schedule"][0]["primary_phases"][0]
        phase.update({
            "phase_kind": "transition",
            "active_motion_windows": [[0.0, 1.0]],
            "dwell_windows": []
        })
        self.assertTrue(any("moving phase needs action IDs" in error for error in self.errors(spec)))

    def test_repeated_schedule_requires_realized_variation(self):
        spec = sample()
        spec["intent"]["beats"].append({
            "id": "beat-02", "action": "Repeat.", "subject_ids": ["person-01"]
        })
        repetition = spec["realism_selection"][0]["repetition_variation"]
        repetition.update({
            "repeated_action": True,
            "status": "required",
            "dimensions": ["interval", "amplitude"],
            "timing_strategy": "Use two non-identical repetitions.",
            "rationale": "Avoid mechanical duplication."
        })
        phases = spec["motion_schedule"][0]["primary_phases"]
        phases[0].update({
            "window": [0.0, 0.5],
            "dwell_windows": [[0.0, 0.5]],
            "repetition_group": "repeat"
        })
        phases.append({
            "beat_id": "beat-02",
            "window": [0.5, 1.0],
            "phase_kind": "dwell",
            "active_motion_windows": [],
            "dwell_windows": [[0.5, 1.0]],
            "tempo": {
                "source": "natural_default",
                "descriptor": "still",
                "slow_motion": False,
                "evidence": "The repeated beat remains a held pose."
            },
            "velocity_profile": {
                "onset": "No intentional onset.",
                "acceleration": "None.",
                "peak": "None.",
                "deceleration": "None.",
                "arrival": "Maintain contact."
            },
            "action_ids": [],
            "repetition_group": "repeat",
            "variation_dimensions": ["interval"],
            "variation_note": "The second repetition lasts slightly longer."
        })
        self.assertTrue(any("at least two selected" in error for error in self.errors(spec)))

    def test_unresolved_repair_is_reported_as_conflict(self):
        spec = sample()
        spec["intent_resolutions"] = [{
            "source_text": "Turn both left and right at the same instant.",
            "issue_type": "contradiction",
            "disposition": "unresolved",
            "resolution": "A direction must be chosen.",
            "rationale": "The requests cannot both be satisfied in one rigid head pose."
        }]
        self.assertTrue(any("must appear in unresolved_conflicts" in error for error in self.errors(spec)))

    def test_input_configuration_must_match_roles(self):
        spec = sample()
        spec["input_plan"]["configuration"] = "reference_frames_only"
        self.assertTrue(any("configuration" in error for error in self.errors(spec)))

    def test_reference_only_input_plan_is_valid(self):
        spec = sample()
        spec["input_plan"].update({
            "configuration": "reference_frames_only",
            "frame_anchors": [],
            "semantic_references": [{
                "reference_id": "ref-01", "roles": ["subject_identity"],
                "subject_ids": ["person-01"], "object_ids": [], "priority": "critical",
                "preserve": ["Visible identity."], "exclude": ["Do not copy a timeline state."]
            }],
            "segments": [{
                "id": "segment-01", "window": [0.0, 1.0],
                "from_anchor_id": None, "to_anchor_id": None,
                "beat_ids": ["beat-01"], "transition_intent": "Generate the complete timeline.",
                "continuity_constraints": ["Preserve the assigned identity."],
                "feasibility": "plausible"
            }],
        })
        self.assertEqual(self.errors(spec), [])

    def test_full_anchor_and_reference_plan_is_valid(self):
        spec = sample()
        for identifier in ("ref-middle", "ref-last", "ref-identity"):
            spec["references"].append({
                "id": identifier, "source": f"{identifier}.png",
                "observation": "A supplied view of the same hand.", "confidence": "high"
            })
        spec["subjects"][0]["reference_ids"].extend(["ref-middle", "ref-last", "ref-identity"])
        spec["input_plan"].update({
            "configuration": "first_last_intermediate_and_references",
            "duration_seconds": 10,
            "duration_source": "user",
            "frame_anchors": [
                spec["input_plan"]["frame_anchors"][0],
                {
                    "id": "anchor-middle", "reference_id": "ref-middle",
                    "role": "intermediate_frame", "normalized_time": 0.5,
                    "time_seconds": 5, "timing_source": "user",
                    "adherence": "exact_requested_state", "subject_ids": ["person-01"],
                    "beat_ids": ["beat-01"], "preserve": ["Midpoint pose."]
                },
                {
                    "id": "anchor-last", "reference_id": "ref-last",
                    "role": "last_frame", "normalized_time": 1.0,
                    "time_seconds": 10, "timing_source": "endpoint",
                    "adherence": "exact_requested_state", "subject_ids": ["person-01"],
                    "beat_ids": ["beat-01"], "preserve": ["Ending pose."]
                },
            ],
            "semantic_references": [{
                "reference_id": "ref-identity", "roles": ["subject_identity"],
                "subject_ids": ["person-01"], "object_ids": [], "priority": "critical",
                "preserve": ["Visible identity."], "exclude": ["Do not copy pose or timing."]
            }],
            "segments": [
                {
                    "id": "segment-01", "window": [0.0, 0.5],
                    "from_anchor_id": "anchor-first", "to_anchor_id": "anchor-middle",
                    "beat_ids": ["beat-01"], "transition_intent": "Move into the midpoint pose.",
                    "continuity_constraints": ["Maintain support."], "feasibility": "plausible"
                },
                {
                    "id": "segment-02", "window": [0.5, 1.0],
                    "from_anchor_id": "anchor-middle", "to_anchor_id": "anchor-last",
                    "beat_ids": ["beat-01"], "transition_intent": "Move into the ending pose.",
                    "continuity_constraints": ["Maintain support."], "feasibility": "plausible"
                },
            ],
        })
        self.assertEqual(self.errors(spec), [])

    def test_first_anchor_must_be_at_start(self):
        spec = sample()
        spec["input_plan"]["frame_anchors"][0]["normalized_time"] = 0.2
        self.assertTrue(any("first frame must be at 0" in error for error in self.errors(spec)))

    def test_every_reference_needs_an_input_role(self):
        spec = sample()
        spec["references"].append({
            "id": "ref-02", "source": "extra.png",
            "observation": "An additional view.", "confidence": "high"
        })
        self.assertTrue(any("every image reference" in error for error in self.errors(spec)))

    def test_semantic_identity_reference_needs_subject_target(self):
        spec = sample()
        spec["input_plan"]["semantic_references"] = [{
            "reference_id": "ref-01", "roles": ["subject_identity"],
            "subject_ids": [], "object_ids": [], "priority": "critical",
            "preserve": ["Identity."], "exclude": ["Pose."]
        }]
        spec["input_plan"]["dual_role_reference_ids"] = ["ref-01"]
        spec["input_plan"]["configuration"] = "first_and_references"
        self.assertTrue(any("subject role needs" in error for error in self.errors(spec)))

    def test_dual_role_reference_must_be_declared(self):
        spec = sample()
        spec["input_plan"]["semantic_references"] = [{
            "reference_id": "ref-01", "roles": ["subject_identity"],
            "subject_ids": ["person-01"], "object_ids": [], "priority": "critical",
            "preserve": ["Identity."], "exclude": ["Do not copy timing."]
        }]
        spec["input_plan"]["configuration"] = "first_and_references"
        self.assertTrue(any("dual-role" in error for error in self.errors(spec)))

    def test_segment_boundaries_must_match_anchors(self):
        spec = sample()
        spec["input_plan"]["segments"][0]["window"] = [0.1, 1.0]
        self.assertTrue(any("segments must cover" in error for error in self.errors(spec)))

    def test_every_anchor_must_split_the_timeline(self):
        spec = sample()
        spec["references"].append({
            "id": "ref-middle", "source": "middle.png",
            "observation": "An interior state.", "confidence": "high"
        })
        spec["subjects"][0]["reference_ids"].append("ref-middle")
        spec["input_plan"]["configuration"] = "first_and_intermediate"
        spec["input_plan"]["frame_anchors"].append({
            "id": "anchor-middle", "reference_id": "ref-middle",
            "role": "intermediate_frame", "normalized_time": 0.5,
            "time_seconds": None, "timing_source": "user",
            "adherence": "exact_requested_state", "subject_ids": ["person-01"],
            "beat_ids": ["beat-01"], "preserve": ["Interior pose."]
        })
        self.assertTrue(any("every anchor" in error for error in self.errors(spec)))

    def test_duration_source_must_match_duration(self):
        spec = sample()
        spec["input_plan"]["duration_source"] = "user"
        self.assertTrue(any("duration source" in error for error in self.errors(spec)))

    def test_seconds_and_normalized_time_must_agree(self):
        spec = sample()
        plan = spec["input_plan"]
        plan["duration_seconds"] = 10
        plan["duration_source"] = "user"
        plan["frame_anchors"][0]["time_seconds"] = 2
        self.assertTrue(any("seconds and normalized" in error for error in self.errors(spec)))

    def test_seamless_loop_intent_needs_both_endpoints(self):
        spec = sample()
        spec["input_plan"]["loop_intent"] = "seamless"
        self.assertTrue(any("seamless loop intent" in error for error in self.errors(spec)))

    def test_ping_pong_loop_accepts_first_frame_only(self):
        spec = sample()
        spec["input_plan"]["loop_intent"] = "ping_pong"
        self.assertEqual(self.errors(spec), [])

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
