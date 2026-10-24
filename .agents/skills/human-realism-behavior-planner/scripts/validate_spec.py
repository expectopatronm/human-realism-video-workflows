"""Validate a pre-generation human realism scene specification."""

import argparse
import json
import re
import sys
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
SCHEMA = SKILL / "references" / "scene-spec.schema.json"
STANDARD = ROOT / "Human Realism Behavior Planner" / "Human Appearance, Anatomy & Motion Realism Standard.md"


def unique_object(pairs):
    """Reject duplicate JSON keys before they can silently overwrite values."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_schema(value, rule, schema, path="$"):
    """Check the JSON Schema features used by this skill.

    Args:
        value: JSON value being checked.
        rule: Schema rule for this value.
        schema: Complete schema containing shared definitions.
        path: Location used in error messages.

    Returns:
        A list of structural validation errors.
    """
    if "$ref" in rule:
        name = rule["$ref"].removeprefix("#/$defs/")
        return check_schema(value, schema["$defs"][name], schema, path)

    errors = []
    types = rule.get("type")
    if types:
        choices = types if isinstance(types, list) else [types]
        matches = {
            "object": lambda x: isinstance(x, dict),
            "array": lambda x: isinstance(x, list),
            "string": lambda x: isinstance(x, str),
            "boolean": lambda x: isinstance(x, bool),
            "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
            "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
            "null": lambda x: x is None,
        }
        if not any(matches[k](value) for k in choices):
            return [f"{path}: expected {' or '.join(choices)}"]
    if "const" in rule and value != rule["const"]:
        errors.append(f"{path}: must equal {rule['const']!r}")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"{path}: invalid value {value!r}")

    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            errors.append(f"{path}: string is too short")
        if "pattern" in rule and not re.fullmatch(rule["pattern"], value):
            errors.append(f"{path}: invalid format {value!r}")
    elif isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if "maxItems" in rule and len(value) > rule["maxItems"]:
            errors.append(f"{path}: too many items")
        if rule.get("uniqueItems") and len(value) != len(set(value)):
            errors.append(f"{path}: duplicate items")
        if "items" in rule:
            for index, item in enumerate(value):
                errors.extend(check_schema(item, rule["items"], schema, f"{path}[{index}]"))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in rule and value < rule["minimum"]:
            errors.append(f"{path}: below minimum {rule['minimum']}")
        if "exclusiveMinimum" in rule and value <= rule["exclusiveMinimum"]:
            errors.append(f"{path}: must be greater than {rule['exclusiveMinimum']}")
        if "maximum" in rule and value > rule["maximum"]:
            errors.append(f"{path}: above maximum {rule['maximum']}")
    elif isinstance(value, dict):
        properties = rule.get("properties", {})
        for key in rule.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing {key}")
        if rule.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{path}: unexpected {key}")
        for key in value.keys() & properties.keys():
            errors.extend(check_schema(value[key], properties[key], schema, f"{path}.{key}"))
    return errors


def check_traceability(spec):
    """Check IDs and source names against the unchanged knowledge base.

    Args:
        spec: Structurally valid scene specification.

    Returns:
        A list of cross-reference and source-ID errors.
    """
    source = STANDARD.read_text(encoding="utf-8-sig")
    known_rules = set(re.findall(r"^## (G\d{2})\.", source, re.MULTILINE))
    known_components = dict(re.findall(r"^### (\d{2}\.\d{2}) (.+)$", source, re.MULTILINE))
    errors = []

    def unique_ids(items, label):
        ids = [item["id"] for item in items]
        if len(ids) != len(set(ids)):
            errors.append(f"{label}: duplicate IDs")
        return set(ids)

    refs = unique_ids(spec["references"], "references")
    unique_ids(spec["motion_sources"], "motion_sources")
    subjects = unique_ids(spec["subjects"], "subjects")
    unique_ids(spec["intent"]["beats"], "beats")
    selected_rules = unique_ids(spec["global_rules"], "global_rules")
    for rule_id in selected_rules - known_rules:
        errors.append(f"global_rules: unknown {rule_id}")

    for subject in spec["subjects"]:
        if not subject["reference_ids"]:
            errors.append(f"subject {subject['id']}: no reference image")
        for ref in set(subject["reference_ids"]) - refs:
            errors.append(f"subject {subject['id']}: unknown reference {ref}")
        for anchor in subject["identity_anchors"]:
            if set(anchor["reference_ids"]) - set(subject["reference_ids"]):
                errors.append(f"subject {subject['id']}: identity anchor uses an unassigned reference")

    profiles = spec["realism_selection"]
    profile_subjects = [profile["subject_id"] for profile in profiles]
    if len(profile_subjects) != len(set(profile_subjects)):
        errors.append("realism_selection: duplicate subject profiles")
    if set(profile_subjects) != subjects:
        errors.append("realism_selection: must contain exactly one profile per subject")
    for beat in spec["intent"]["beats"]:
        for subject_id in set(beat["subject_ids"]) - subjects:
            errors.append(f"beat {beat['id']}: unknown subject {subject_id}")

    component_keys = set()
    for component in spec["components"]:
        key = (component["subject_id"], component["component_id"])
        if key in component_keys:
            errors.append(f"components: duplicate {key}")
        component_keys.add(key)
        component_id = component["component_id"]
        if component["subject_id"] not in subjects:
            errors.append(f"component {component_id}: unknown subject")
        if component_id not in known_components:
            errors.append(f"component {component_id}: unknown Level 2 ID")
        elif component["name"] != known_components[component_id]:
            errors.append(f"component {component_id}: name must be {known_components[component_id]!r}")
        trace = component["traceability"]
        if not trace["global_rule_ids"]:
            errors.append(f"component {component_id}: no global rule IDs")
        for rule_id in set(trace["global_rule_ids"]) - selected_rules:
            errors.append(f"component {component_id}: global rule {rule_id} is not selected")
        cited = trace["reference_ids"] + component["reference_observation"]["reference_ids"]
        for ref in set(cited) - refs:
            errors.append(f"component {component_id}: unknown reference {ref}")
        if component["reference_observation"]["observed"] and not component["reference_observation"]["reference_ids"]:
            errors.append(f"component {component_id}: observations need reference IDs")
    errors.extend(check_input_plan(spec, refs, subjects))
    errors.extend(check_realism_selection(spec, selected_rules))
    errors.extend(check_behavior_plan(spec, subjects))
    errors.extend(check_spatial_plan(spec, subjects))
    errors.extend(check_motion_schedule(spec, subjects))
    return errors


def check_input_plan(spec, refs, subjects):
    """Validate image roles, anchor timing, and anchor-to-anchor segments.

    Args:
        spec: Structurally valid scene specification.
        refs: Known image reference IDs.
        subjects: Known subject IDs.

    Returns:
        Semantic errors in the model-neutral input plan.
    """
    errors = []
    plan = spec["input_plan"]
    beats = {beat["id"] for beat in spec["intent"]["beats"]}
    objects = {item["id"] for item in spec["scene_physics"]["objects"]}
    anchors = plan["frame_anchors"]
    anchor_ids = [anchor["id"] for anchor in anchors]
    if len(anchor_ids) != len(set(anchor_ids)):
        errors.append("input_plan: duplicate anchor IDs")
    anchor_map = {anchor["id"]: anchor for anchor in anchors}
    anchor_refs = {anchor["reference_id"] for anchor in anchors}
    roles = [anchor["role"] for anchor in anchors]
    if roles.count("first_frame") > 1 or roles.count("last_frame") > 1:
        errors.append("input_plan: at most one first and one last anchor")
    times = [anchor["normalized_time"] for anchor in anchors]
    if times != sorted(times) or len(times) != len(set(times)):
        errors.append("input_plan: anchors must have unique ascending times")
    duration = plan["duration_seconds"]
    if (duration is None) != (plan["duration_source"] == "unknown"):
        errors.append("input_plan: duration source must agree with duration availability")
    for anchor in anchors:
        label = f"input_plan/{anchor['id']}"
        if anchor["reference_id"] not in refs:
            errors.append(f"{label}: unknown reference")
        if set(anchor["subject_ids"]) - subjects:
            errors.append(f"{label}: unknown subject")
        if set(anchor["beat_ids"]) - beats:
            errors.append(f"{label}: unknown beat")
        time = anchor["normalized_time"]
        if anchor["role"] == "first_frame" and time != 0:
            errors.append(f"{label}: first frame must be at 0")
        if anchor["role"] == "last_frame" and time != 1:
            errors.append(f"{label}: last frame must be at 1")
        if anchor["role"] == "intermediate_frame" and not 0 < time < 1:
            errors.append(f"{label}: intermediate frame must be inside the clip")
        if anchor["role"] == "intermediate_frame" and anchor["timing_source"] == "endpoint":
            errors.append(f"{label}: intermediate frame cannot use endpoint timing")
        if anchor["role"] != "intermediate_frame" and anchor["timing_source"] != "endpoint":
            errors.append(f"{label}: endpoint frame needs endpoint timing")
        seconds = anchor["time_seconds"]
        if duration is not None and seconds is not None and abs(seconds / duration - time) > 1e-6:
            errors.append(f"{label}: seconds and normalized time disagree")

    semantic = plan["semantic_references"]
    semantic_ids = [item["reference_id"] for item in semantic]
    if len(semantic_ids) != len(set(semantic_ids)):
        errors.append("input_plan: each semantic reference needs one assignment")
    for item in semantic:
        label = f"input_plan/semantic/{item['reference_id']}"
        if item["reference_id"] not in refs:
            errors.append(f"{label}: unknown reference")
        if set(item["subject_ids"]) - subjects:
            errors.append(f"{label}: unknown subject")
        if set(item["object_ids"]) - objects:
            errors.append(f"{label}: unknown object")
        subject_roles = {"subject_identity", "face_identity", "body_identity", "clothing", "accessory", "pose"}
        if set(item["roles"]) & subject_roles and not item["subject_ids"]:
            errors.append(f"{label}: subject role needs a subject target")
        if "object" in item["roles"] and not item["object_ids"]:
            errors.append(f"{label}: object role needs an object target")

    semantic_refs = set(semantic_ids)
    dual = set(plan["dual_role_reference_ids"])
    if dual != anchor_refs & semantic_refs:
        errors.append("input_plan: dual-role IDs must equal anchor and semantic overlap")
    if anchor_refs | semantic_refs != refs:
        errors.append("input_plan: every image reference needs a timeline or semantic role")
    signatures = {
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
    signature = (
        int("first_frame" in roles), int("last_frame" in roles),
        int("intermediate_frame" in roles), int(bool(semantic)),
    )
    if signatures.get(signature) != plan["configuration"]:
        errors.append("input_plan: configuration does not match assigned roles")

    conflict_ids = [item["id"] for item in plan["role_conflicts"]]
    if len(conflict_ids) != len(set(conflict_ids)):
        errors.append("input_plan: duplicate role-conflict IDs")
    for conflict in plan["role_conflicts"]:
        if set(conflict["reference_ids"]) - refs:
            errors.append(f"input_plan/{conflict['id']}: unknown reference")
    if plan["loop_intent"] == "seamless" and not {"first_frame", "last_frame"}.issubset(roles):
        errors.append("input_plan: seamless loop intent needs first and last anchors")

    segments = plan["segments"]
    segment_ids = [segment["id"] for segment in segments]
    if len(segment_ids) != len(set(segment_ids)):
        errors.append("input_plan: duplicate segment IDs")
    previous_end = 0.0
    for index, segment in enumerate(segments):
        label = f"input_plan/{segment['id']}"
        start, end = segment["window"]
        if start >= end or abs(start - previous_end) > 1e-9:
            errors.append(f"{label}: segments must cover the clip in order without gaps")
        previous_end = end
        if set(segment["beat_ids"]) - beats:
            errors.append(f"{label}: unknown beat")
        start_id, end_id = segment["from_anchor_id"], segment["to_anchor_id"]
        if start_id is None:
            if start != 0:
                errors.append(f"{label}: null start anchor is allowed only at clip start")
        elif start_id not in anchor_map or anchor_map[start_id]["normalized_time"] != start:
            errors.append(f"{label}: start anchor does not match segment boundary")
        if end_id is None:
            if end != 1:
                errors.append(f"{label}: null end anchor is allowed only at clip end")
        elif end_id not in anchor_map or anchor_map[end_id]["normalized_time"] != end:
            errors.append(f"{label}: end anchor does not match segment boundary")
    if abs(previous_end - 1.0) > 1e-9:
        errors.append("input_plan: segments must end at 1")
    boundaries = {segments[0]["window"][0]} | {segment["window"][1] for segment in segments}
    expected_boundaries = {0.0, 1.0} | set(times)
    if boundaries != expected_boundaries:
        errors.append("input_plan: every anchor must form an interpolation-segment boundary")
    return errors


def check_behavior_plan(spec, subjects):
    """Check the research-layer plan against subject beats and motion tracks.

    Args:
        spec: Structurally valid scene specification.
        subjects: Subject IDs already checked for uniqueness.

    Returns:
        Semantic errors in channel timing, physiology, dynamics, and physics.
    """
    errors = []
    expected = {"gaze", "face", "head", "gesture", "posture", "locomotion", "speech"}
    beats = {beat["id"] for beat in spec["intent"]["beats"]}
    plans = spec["behavior_plan"]
    plan_subjects = [plan["subject_id"] for plan in plans]
    if len(plan_subjects) != len(set(plan_subjects)) or set(plan_subjects) != subjects:
        errors.append("behavior_plan: must contain exactly one plan per subject")
    schedules = {item["subject_id"]: item for item in spec["motion_schedule"]}
    physics = spec["scene_physics"]
    environment_ids = {item["id"] for item in physics["environmental_drivers"]}
    contact_ids = {item["id"] for item in physics["support_contacts"]}
    force_ids = {item["id"] for item in physics["force_fields"]}

    def check_beats(ids, label):
        if set(ids) - beats:
            errors.append(f"{label}: unknown beat IDs")

    for plan in plans:
        subject = plan["subject_id"]
        label = f"behavior_plan {subject}"
        subject_beats = {
            beat["id"] for beat in spec["intent"]["beats"]
            if subject in beat["subject_ids"]
        }
        control = plan["performance_control"]
        support = control["support_state"]
        posture = control["posture_preservation"]
        layers = control["temporal_layers"]
        layer_ids = [layer["id"] for layer in layers]
        layer_map = {layer["id"]: layer for layer in layers}
        if len(layer_ids) != len(set(layer_ids)):
            errors.append(f"{label}: duplicate temporal-layer IDs")
        primary_layers = [layer for layer in layers if layer["kind"] == "primary_voluntary"]
        if len(primary_layers) != 1:
            errors.append(f"{label}: performance control needs exactly one primary voluntary layer")
        concurrency = control["concurrency_policy"]
        dominant_id = concurrency["dominant_track_id"]
        if dominant_id not in layer_map:
            errors.append(f"{label}: dominant temporal layer is unknown")
        elif layer_map[dominant_id]["kind"] != "primary_voluntary":
            errors.append(f"{label}: dominant temporal layer must be primary voluntary")
        subthreshold = concurrency["subthreshold_track_ids"]
        if set(subthreshold) - set(layer_ids) or dominant_id in subthreshold:
            errors.append(f"{label}: invalid subthreshold temporal-layer IDs")
        if any(layer_map[item]["amplitude"] not in {"subthreshold", "barely_perceptible"}
               for item in subthreshold if item in layer_map):
            errors.append(f"{label}: subthreshold tracks must stay below salient amplitude")
        channels_by_name = {item["channel"]: item for item in plan["channels"]}
        support_dependent = any(
            channels_by_name.get(name, {}).get("status") == "active"
            for name in {"posture", "locomotion"}
        )
        if support_dependent and support["posture_class"] == "unknown":
            errors.append(f"{label}: active posture or locomotion needs a resolved support state")
        if support_dependent and support["pelvis_height"] == "unknown":
            errors.append(f"{label}: active posture or locomotion needs an explicit pelvis-height policy")
        if posture["authority"] == "strict" and not posture["prohibited_normalization"]:
            errors.append(f"{label}: strict posture preservation needs prohibited normalizations")
        variability = control["variability_policy"]
        if variability["mode"] == "bounded_aperiodic" and not variability["dimensions"]:
            errors.append(f"{label}: bounded aperiodic motion needs variation dimensions")
        expected_loop = {
            "none": "none", "seamless": "seamless_forward", "ping_pong": "ping_pong",
        }[spec["input_plan"]["loop_intent"]]
        if control["loop_policy"]["mode"] != expected_loop:
            errors.append(f"{label}: performance loop policy contradicts input loop intent")
        channel_names = [item["channel"] for item in plan["channels"]]
        if set(channel_names) != expected or len(channel_names) != len(set(channel_names)):
            errors.append(f"{label}: channels must cover each behavior channel once")
        channels = {item["channel"]: item for item in plan["channels"]}
        for channel in plan["channels"]:
            check_beats(channel["beat_ids"], f"{label}/{channel['channel']}")
            if set(channel["beat_ids"]) - subject_beats:
                errors.append(f"{label}/{channel['channel']}: beat belongs to another subject")
            window = channel["window"]
            if window is not None and window[0] >= window[1]:
                errors.append(f"{label}/{channel['channel']}: invalid window")
            if channel["status"] in {"active", "held"} and (not channel["behavior"] or not channel["beat_ids"]):
                errors.append(f"{label}/{channel['channel']}: active channel needs behavior and beats")
            if channel["status"] in {"not_visible", "not_applicable"} and window is not None:
                errors.append(f"{label}/{channel['channel']}: inactive channel cannot have a window")
            phases = channel["phases"]
            names = [phase["name"] for phase in phases]
            phase_order = {name: index for index, name in enumerate(
                ["preparation", "stroke", "hold", "relaxation", "return"]
            )}
            if len(names) != len(set(names)):
                errors.append(f"{label}/{channel['channel']}: duplicate behavior phases")
            if channel["status"] == "active" and channel["channel"] in {"gesture", "head"} and not phases:
                errors.append(f"{label}/{channel['channel']}: active gesture or head motion needs phases")
            if any(phase_order[a] >= phase_order[b] for a, b in zip(names, names[1:])):
                errors.append(f"{label}/{channel['channel']}: behavior phases out of order")
            previous_end = None
            for phase in phases:
                start, end = phase["window"]
                if start >= end or (window and (start < window[0] or end > window[1])):
                    errors.append(f"{label}/{channel['channel']}: invalid behavior phase window")
                if previous_end is not None and start < previous_end:
                    errors.append(f"{label}/{channel['channel']}: behavior phases overlap")
                previous_end = end
            for sync in channel["sync_points"]:
                other = channels.get(sync["with_channel"])
                other_names = {item["name"] for item in other["phases"]} if other else set()
                if sync["own_phase"] not in names or sync["other_phase"] not in other_names:
                    errors.append(f"{label}/{channel['channel']}: sync point needs existing phases")
                    continue
                own_window = next(item["window"] for item in phases if item["name"] == sync["own_phase"])
                other_window = next(item["window"] for item in other["phases"] if item["name"] == sync["other_phase"])
                relation = sync["relation"]
                valid = {
                    "before": own_window[1] <= other_window[0],
                    "overlap": max(own_window[0], other_window[0]) < min(own_window[1], other_window[1]),
                    "after": own_window[0] >= other_window[1],
                }[relation]
                if not valid:
                    errors.append(f"{label}/{channel['channel']}: sync point relation contradicts timing")
        qualities = plan["movement_quality"]
        quality_beats = [item["beat_id"] for item in qualities]
        if len(quality_beats) != len(set(quality_beats)) or set(quality_beats) != subject_beats:
            errors.append(f"{label}: movement_quality must cover each subject beat once")
        face = plan["facial_plan"]
        units = face["action_units"]
        face_channel = next((item for item in plan["channels"] if item["channel"] == "face"), None)
        if face["visibility"] == "not_visible" and units:
            errors.append(f"{label}: hidden face cannot have visible action units")
        if face["expression_change"] and face["visibility"] != "not_visible" and not units:
            errors.append(f"{label}: visible expression change needs action units")
        if face["expression_change"] and face_channel and face_channel["status"] != "active":
            errors.append(f"{label}: expression change needs active face channel")
        if len([unit["code"] for unit in units]) != len(set(unit["code"] for unit in units)):
            errors.append(f"{label}: duplicate action units")
        for unit in units:
            check_beats(unit["beat_ids"], f"{label}/{unit['code']}")
            if not unit["beat_ids"] or set(unit["beat_ids"]) - subject_beats:
                errors.append(f"{label}/{unit['code']}: needs subject beat IDs")
            if not unit["onset"] <= unit["apex"] <= unit["offset"]:
                errors.append(f"{label}/{unit['code']}: onset, apex, offset are out of order")
        unit_codes = {unit["code"] for unit in units}
        for combination in face["combinations"]:
            if set(combination["codes"]) - unit_codes:
                errors.append(f"{label}: AU combination cites an unplanned unit")
        physiology = plan["physiology_states"]
        expected_physiology = {"swallowing", "exertion", "fatigue", "autonomic_response", "speech_breath"}
        physiology_names = [item["cue"] for item in physiology]
        if len(physiology_names) != len(set(physiology_names)) or set(physiology_names) != expected_physiology:
            errors.append(f"{label}: physiology states must cover all extended cues")
        for state in physiology:
            if state["status"] in {"required", "conditional"} and (
                not state["driver"] or not state["visible_effects"] or not state["timing_relation"]
            ):
                errors.append(f"{label}/{state['cue']}: active physiology needs driver, effect, and timing")
        for coupling in plan["physiology_couplings"]:
            check_beats(coupling["beat_ids"], f"{label}/physiology")
            if coupling["source"] == coupling["target"]:
                errors.append(f"{label}: physiology coupling needs distinct source and target")
        schedule = schedules.get(subject, {})
        tracks = {item["id"] for item in schedule.get("secondary_tracks", [])}
        passive = plan["passive_elements"]
        passive_ids = [item["id"] for item in passive]
        if len(passive_ids) != len(set(passive_ids)):
            errors.append(f"{label}: duplicate passive element IDs")
        for element in passive:
            linked = element["dynamics_track_ids"]
            if set(linked) - tracks:
                errors.append(f"{label}/{element['id']}: unknown dynamics track")
            if element["status"] == "affected" and not linked:
                errors.append(f"{label}/{element['id']}: affected element needs dynamics track")
            if element["status"] != "affected" and linked:
                errors.append(f"{label}/{element['id']}: held or hidden element cannot have dynamics track")
        links = [item["track_id"] for item in plan["dynamics_links"]]
        if set(links) != tracks or len(links) != len(set(links)):
            errors.append(f"{label}: dynamics_links must match secondary tracks once")
        for link in plan["dynamics_links"]:
            check_beats(link["beat_ids"], f"{label}/{link['track_id']}")
            kind = link["driver_kind"]
            allowed = {
                "primary_beat": subject_beats,
                "vitality_cue": {item["cue"] for item in schedule.get("vitality_tracks", [])},
                "environment": environment_ids,
                "contact": contact_ids,
                "secondary_track": tracks,
            }[kind]
            if link["driver_ref"] not in allowed:
                errors.append(f"{label}/{link['track_id']}: unknown dynamics driver")
            if set(link["propagates_to"]) - tracks or link["track_id"] in link["propagates_to"]:
                errors.append(f"{label}/{link['track_id']}: invalid dynamics propagation")
        graph = {link["track_id"]: link["propagates_to"] for link in plan["dynamics_links"]}
        def reaches_start(start, current, seen):
            for target in graph.get(current, []):
                if target == start or (target not in seen and reaches_start(start, target, seen | {target})):
                    return True
            return False
        if any(reaches_start(track, track, {track}) for track in graph):
            errors.append(f"{label}: dynamics propagation contains a cycle")

    object_ids = [item["id"] for item in physics["objects"]]
    if len(object_ids) != len(set(object_ids)):
        errors.append("scene_physics: duplicate object IDs")
    if len(contact_ids) != len(physics["support_contacts"]):
        errors.append("scene_physics: duplicate contact IDs")
    if len(force_ids) != len(physics["force_fields"]):
        errors.append("scene_physics: duplicate force IDs")
    for contact in physics["support_contacts"]:
        if contact["subject_id"] not in subjects:
            errors.append("scene_physics: unknown contact subject")
        if contact["object_id"] is not None and contact["object_id"] not in object_ids:
            errors.append("scene_physics: contact cites unknown object")
        check_beats(contact["beat_ids"], "scene_physics/contact")
    driver_ids = [item["id"] for item in physics["environmental_drivers"]]
    if len(driver_ids) != len(set(driver_ids)):
        errors.append("scene_physics: duplicate environmental driver IDs")
    for driver in physics["environmental_drivers"]:
        if driver["window"][0] >= driver["window"][1]:
            errors.append(f"scene_physics/{driver['id']}: invalid window")
    for force in physics["force_fields"]:
        if force["window"][0] >= force["window"][1]:
            errors.append(f"scene_physics/{force['id']}: invalid force window")
    for dependency in physics["visual_dependencies"]:
        check_beats(dependency["beat_ids"], "scene_physics/visual_dependency")
        allowed = {
            "primary_beat": beats, "environment": environment_ids,
            "contact": contact_ids, "force_field": force_ids,
        }[dependency["driver_kind"]]
        if dependency["driver_ref"] not in allowed:
            errors.append("scene_physics: visual dependency has unknown driver")
    return errors


def check_spatial_plan(spec, subjects):
    """Validate subject/camera paths, interactions, and occlusion coverage.

    Args:
        spec: Structurally valid scene specification.
        subjects: Subject IDs already checked for uniqueness.

    Returns:
        Semantic errors in the spatial and interaction plan.
    """
    errors = []
    plan = spec["spatial_plan"]
    beats = {beat["id"] for beat in spec["intent"]["beats"]}
    subject_beats = {
        subject: {
            beat["id"] for beat in spec["intent"]["beats"]
            if subject in beat["subject_ids"]
        }
        for subject in subjects
    }
    objects = {item["id"] for item in spec["scene_physics"]["objects"]}
    tracks = plan["subject_tracks"]
    track_subjects = [track["subject_id"] for track in tracks]
    if len(track_subjects) != len(set(track_subjects)) or set(track_subjects) != subjects:
        errors.append("spatial_plan: must contain exactly one subject track per subject")
    profiles = {item["id"]: item for item in spec["subjects"]}
    for track in tracks:
        subject = track["subject_id"]
        if set(track["beat_ids"]) != subject_beats.get(subject, set()):
            errors.append(f"spatial_plan {subject}: track must cover every subject beat once")
        if track["reference_coverage"] == "insufficient" and not profiles[subject]["unseen_region_policy"]:
            errors.append(f"spatial_plan {subject}: insufficient coverage needs an unseen-region policy")
    interaction_ids = [item["id"] for item in plan["interactions"]]
    if len(interaction_ids) != len(set(interaction_ids)):
        errors.append("spatial_plan: duplicate interaction IDs")
    for interaction in plan["interactions"]:
        label = f"spatial_plan/{interaction['id']}"
        if set(interaction["subject_ids"]) - subjects:
            errors.append(f"{label}: unknown subject")
        if set(interaction["object_ids"]) - objects:
            errors.append(f"{label}: unknown object")
        if set(interaction["beat_ids"]) - beats:
            errors.append(f"{label}: unknown beat")
        if interaction["kind"] == "human_human" and len(interaction["subject_ids"]) < 2:
            errors.append(f"{label}: human-human interaction needs at least two subjects")
        if interaction["kind"] == "human_object" and not interaction["object_ids"]:
            errors.append(f"{label}: human-object interaction needs an object")
    event_ids = [item["id"] for item in plan["occlusion_events"]]
    if len(event_ids) != len(set(event_ids)):
        errors.append("spatial_plan: duplicate occlusion event IDs")
    for event in plan["occlusion_events"]:
        if event["subject_id"] not in subjects:
            errors.append(f"spatial_plan/{event['id']}: unknown subject")
        if event["window"][0] >= event["window"][1]:
            errors.append(f"spatial_plan/{event['id']}: invalid occlusion window")
    camera = plan["camera_track"]
    if camera["window"][0] >= camera["window"][1]:
        errors.append("spatial_plan: invalid camera window")
    if camera["status"] == "static" and camera["depth_change"] != "none":
        errors.append("spatial_plan: static camera cannot change depth")
    return errors


def check_realism_selection(spec, selected_rules):
    """Validate baseline vitality and repetition decisions against components."""
    errors = []
    expected_cues = {
        "respiration", "blinking", "ocular_fixation", "facial_tonus",
        "postural_micro_adjustment",
    }
    component_map = {
        profile["subject_id"]: {
            component["component_id"]: component
            for component in spec["components"]
            if component["subject_id"] == profile["subject_id"]
        }
        for profile in spec["realism_selection"]
    }
    dependencies = {
        "respiration": {"10.01", "10.02", "10.03", "15.01", "15.02", "15.04"},
        "blinking": {"03.02"},
        "ocular_fixation": {"03.05"},
        "facial_tonus": {"02.03", "03.02", "03.03", "05.02", "07.01", "07.02", "07.03"},
        "postural_micro_adjustment": {"08.01", "08.02", "09.03", "11.01", "11.03", "15.05", "16.01"},
    }
    active = {"required", "conditional"}
    active_motion = {"yes", "conditional"}

    for profile in spec["realism_selection"]:
        subject_id = profile["subject_id"]
        cues = profile["baseline_cues"]
        cue_names = [cue["cue"] for cue in cues]
        if len(cue_names) != len(set(cue_names)):
            errors.append(f"realism_selection {subject_id}: duplicate baseline cues")
        if set(cue_names) != expected_cues:
            errors.append(f"realism_selection {subject_id}: baseline cues must cover {sorted(expected_cues)}")
        if profile["subject_state"] == "nonliving":
            if any(cue["status"] != "not_applicable" for cue in cues):
                errors.append(f"realism_selection {subject_id}: nonliving cues must be not_applicable")
        elif any(cue["status"] == "not_applicable" for cue in cues):
            errors.append(f"realism_selection {subject_id}: living or unknown cues cannot be not_applicable")
        selected_components = component_map.get(subject_id, {})
        for cue in cues:
            if cue["status"] not in active:
                continue
            if not cue["visible_effects"]:
                errors.append(f"realism_selection {subject_id}/{cue['cue']}: active cue needs visible_effects")
            if not cue["timing_strategy"]:
                errors.append(f"realism_selection {subject_id}/{cue['cue']}: active cue needs timing_strategy")
            if not cue["variability"]:
                errors.append(f"realism_selection {subject_id}/{cue['cue']}: active cue needs variability")
            if "G16" not in selected_rules:
                errors.append(f"realism_selection {subject_id}/{cue['cue']}: active baseline vitality requires G16")
            matched = dependencies[cue["cue"]] & selected_components.keys()
            if not matched:
                errors.append(
                    f"realism_selection {subject_id}/{cue['cue']}: no supporting Level 2 component"
                )
            else:
                active_components = [
                    selected_components[component_id]
                    for component_id in matched
                    if (
                        selected_components[component_id]["primary_motion"]["required"] in active_motion
                        or selected_components[component_id]["secondary_motion_and_physics"]["required"] in active_motion
                    )
                ]
                if not active_components:
                    errors.append(
                        f"realism_selection {subject_id}/{cue['cue']}: supporting component has no active motion"
                    )
                elif not any(
                    "G16" in component["traceability"]["global_rule_ids"]
                    for component in active_components
                ):
                    errors.append(
                        f"realism_selection {subject_id}/{cue['cue']}: supporting component must trace to G16"
                    )

        repetition = profile["repetition_variation"]
        if repetition["repeated_action"]:
            if repetition["status"] == "not_applicable":
                errors.append(
                    f"realism_selection {subject_id}/repetition: repeated action needs a variation disposition"
                )
            if repetition["status"] in active:
                if len(repetition["dimensions"]) < 2:
                    errors.append(
                        f"realism_selection {subject_id}/repetition: vary at least two dimensions"
                    )
                if not repetition["timing_strategy"]:
                    errors.append(
                        f"realism_selection {subject_id}/repetition: active variation needs timing_strategy"
                    )
        elif repetition["status"] != "not_applicable":
            errors.append(
                f"realism_selection {subject_id}/repetition: nonrepeated action must be not_applicable"
            )
    if any(item["disposition"] == "unresolved" for item in spec["intent_resolutions"]):
        if not spec["unresolved_conflicts"]:
            errors.append("intent_resolutions: unresolved decisions must appear in unresolved_conflicts")
    return errors


def check_motion_schedule(spec, subjects):
    """Validate temporal orchestration against beats and realism decisions."""
    errors = []
    active = {"required", "conditional"}

    def check_windows(windows, label, allow_overlap=False):
        previous_end = None
        for start, end in windows:
            if start >= end:
                errors.append(f"{label}: invalid window")
            if not allow_overlap and previous_end is not None and start < previous_end:
                errors.append(f"{label}: windows overlap or regress")
            previous_end = end

    def contained(inner, outer):
        return outer[0] <= inner[0] and inner[1] <= outer[1]
    beat_order = {beat["id"]: index for index, beat in enumerate(spec["intent"]["beats"])}
    beats_by_subject = {
        subject_id: [
            beat["id"] for beat in spec["intent"]["beats"]
            if subject_id in beat["subject_ids"]
        ]
        for subject_id in subjects
    }
    profiles = {item["subject_id"]: item for item in spec["realism_selection"]}
    schedules = spec["motion_schedule"]
    schedule_subjects = [item["subject_id"] for item in schedules]
    if len(schedule_subjects) != len(set(schedule_subjects)):
        errors.append("motion_schedule: duplicate subject schedules")
    if set(schedule_subjects) != subjects:
        errors.append("motion_schedule: must contain exactly one schedule per subject")

    for schedule in schedules:
        subject_id = schedule["subject_id"]
        phases = schedule["primary_phases"]
        phase_beats = [phase["beat_id"] for phase in phases]
        if phase_beats != beats_by_subject.get(subject_id, []):
            errors.append(
                f"motion_schedule {subject_id}: primary phases must follow every subject beat once"
            )
        for phase in phases:
            if phase["beat_id"] not in beat_order:
                errors.append(f"motion_schedule {subject_id}: unknown beat {phase['beat_id']}")
            active_windows = phase["active_motion_windows"]
            dwell_windows = phase["dwell_windows"]
            check_windows(active_windows, f"motion_schedule {subject_id}/{phase['beat_id']}/active")
            check_windows(dwell_windows, f"motion_schedule {subject_id}/{phase['beat_id']}/dwell")
            for label, windows in (("active", active_windows), ("dwell", dwell_windows)):
                if any(not contained(window, phase["window"]) for window in windows):
                    errors.append(
                        f"motion_schedule {subject_id}/{phase['beat_id']}: {label} window outside phase"
                    )
            if any(
                max(active[0], dwell[0]) < min(active[1], dwell[1])
                for active in active_windows for dwell in dwell_windows
            ):
                errors.append(
                    f"motion_schedule {subject_id}/{phase['beat_id']}: active and dwell windows overlap"
                )
            if phase["phase_kind"] == "dwell" and not dwell_windows:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: dwell phase needs dwell window")
            if phase["phase_kind"] != "dwell" and not active_windows:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: moving phase needs active window")
            if phase["tempo"]["descriptor"] == "slow" and not phase["tempo"]["slow_motion"]:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: slow tempo must be explicit")
            if phase["tempo"]["source"] == "reference_video" and not spec["motion_sources"]:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: missing motion source")
        check_windows(
            [phase["window"] for phase in phases],
            f"motion_schedule {subject_id}/primary",
        )

        actions = schedule["articulated_actions"]
        action_ids = [action["id"] for action in actions]
        if len(action_ids) != len(set(action_ids)):
            errors.append(f"motion_schedule {subject_id}: duplicate articulated-action IDs")
        known_actions = set(action_ids)
        referenced_actions = set()
        for action in actions:
            unknown_beats = set(action["beat_ids"]) - set(phase_beats)
            if unknown_beats:
                errors.append(f"motion_schedule {subject_id}/{action['id']}: unknown beat IDs")
            chain_regions = [link["region"] for link in action["kinematic_chain"]]
            if len(chain_regions) != len(set(chain_regions)):
                errors.append(f"motion_schedule {subject_id}/{action['id']}: duplicate chain regions")
        for phase in phases:
            unknown_actions = set(phase["action_ids"]) - known_actions
            if unknown_actions:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: unknown action IDs")
            if phase["phase_kind"] != "dwell" and not phase["action_ids"]:
                errors.append(f"motion_schedule {subject_id}/{phase['beat_id']}: moving phase needs action IDs")
            referenced_actions.update(phase["action_ids"])
        if referenced_actions != known_actions:
            errors.append(f"motion_schedule {subject_id}: every articulated action must be referenced")

        profile = profiles.get(subject_id)
        if not profile:
            continue
        cue_status = {cue["cue"]: cue["status"] for cue in profile["baseline_cues"]}
        tracks = schedule["vitality_tracks"]
        track_names = [track["cue"] for track in tracks]
        if len(track_names) != len(set(track_names)) or set(track_names) != set(cue_status):
            errors.append(f"motion_schedule {subject_id}: vitality tracks must cover each cue once")
        for track in tracks:
            cue = track["cue"]
            if cue not in cue_status:
                continue
            if track["status"] != cue_status[cue]:
                errors.append(f"motion_schedule {subject_id}/{cue}: status differs from realism_selection")
            if track["status"] in active:
                if track["mode"] == "inactive" or not track["windows"]:
                    errors.append(f"motion_schedule {subject_id}/{cue}: active cue needs scheduled windows")
                if not track["phase_relation"] or not track["variability"]:
                    errors.append(f"motion_schedule {subject_id}/{cue}: active cue needs coordination and variability")
            elif track["status"] in {"not_visible", "not_applicable"} and (
                track["mode"] != "inactive" or track["windows"]
            ):
                errors.append(f"motion_schedule {subject_id}/{cue}: inactive cue must not schedule windows")
            elif track["mode"] != "inactive" and (
                not track["windows"] or not track["phase_relation"] or not track["variability"]
            ):
                errors.append(f"motion_schedule {subject_id}/{cue}: scheduled cue needs windows, coordination, and variability")
            check_windows(track["windows"], f"motion_schedule {subject_id}/{cue}")
            count_range = track["count_range"]
            if count_range and count_range[0] > count_range[1]:
                errors.append(f"motion_schedule {subject_id}/{cue}: invalid count range")
            if track["mode"] == "event" and track["status"] in active and count_range is None:
                errors.append(f"motion_schedule {subject_id}/{cue}: event track needs a count range")
            if track["mode"] == "event" and count_range and count_range[1] > len(track["windows"]):
                errors.append(f"motion_schedule {subject_id}/{cue}: event count exceeds candidate windows")
            event_duration = track["event_duration_seconds"]
            if track["mode"] == "event" and track["status"] in active and event_duration is None:
                errors.append(f"motion_schedule {subject_id}/{cue}: active event needs a duration range")
            if track["mode"] != "event" and event_duration is not None:
                errors.append(f"motion_schedule {subject_id}/{cue}: only event tracks use event duration")
            if event_duration and event_duration[0] > event_duration[1]:
                errors.append(f"motion_schedule {subject_id}/{cue}: invalid event duration range")
            if track["mode"] == "inactive" and count_range is not None:
                errors.append(f"motion_schedule {subject_id}/{cue}: inactive cue cannot have a count range")

        repetition = profile["repetition_variation"]
        if repetition["repeated_action"] and repetition["status"] in active:
            groups = {}
            for phase in phases:
                if phase["repetition_group"]:
                    groups.setdefault(phase["repetition_group"], []).append(phase)
            repeated_groups = [items for items in groups.values() if len(items) > 1]
            if not repeated_groups:
                errors.append(f"motion_schedule {subject_id}: repeated action needs a repetition group")
            scheduled_dimensions = set()
            for items in repeated_groups:
                for phase in items[1:]:
                    scheduled_dimensions.update(phase["variation_dimensions"])
                    if not phase["variation_note"]:
                        errors.append(
                            f"motion_schedule {subject_id}/{phase['beat_id']}: repeated phase needs a variation note"
                        )
            required_dimensions = set(repetition["dimensions"])
            for items in repeated_groups:
                for phase in items[1:]:
                    assigned = set(phase["variation_dimensions"])
                    if not assigned & required_dimensions:
                        errors.append(
                            f"motion_schedule {subject_id}/{phase['beat_id']}: repeated phase needs a selected variation dimension"
                        )
                    if assigned - required_dimensions:
                        errors.append(
                            f"motion_schedule {subject_id}/{phase['beat_id']}: uses unselected variation dimensions"
                        )
            if len(scheduled_dimensions & required_dimensions) < 2:
                errors.append(
                    f"motion_schedule {subject_id}: schedule must realize at least two selected variation dimensions"
                )
            if not schedule["anti_synchrony_rules"]:
                errors.append(f"motion_schedule {subject_id}: repeated action needs anti-synchrony rules")

        track_ids = [track["id"] for track in schedule["secondary_tracks"]]
        if len(track_ids) != len(set(track_ids)):
            errors.append(f"motion_schedule {subject_id}: duplicate secondary track IDs")
        for track in schedule["secondary_tracks"]:
            check_windows(track["windows"], f"motion_schedule {subject_id}/{track['id']}")
        protected_ids = [window["id"] for window in schedule["protected_windows"]]
        if len(protected_ids) != len(set(protected_ids)):
            errors.append(f"motion_schedule {subject_id}: duplicate protected-window IDs")
        check_windows(
            [window["window"] for window in schedule["protected_windows"]],
            f"motion_schedule {subject_id}/protected",
        )
        all_dwells = [window for phase in phases for window in phase["dwell_windows"]]
        for protected in schedule["protected_windows"]:
            if not any(contained(protected["window"], dwell) for dwell in all_dwells):
                errors.append(
                    f"motion_schedule {subject_id}/{protected['id']}: protected window must use an existing dwell"
                )
        active_cues = [track["cue"] for track in tracks if track["status"] in active]
        expected_priorities = {"primary_action", *active_cues, *track_ids}
        priorities = schedule["priority_order"]
        if set(priorities) != expected_priorities:
            errors.append(
                f"motion_schedule {subject_id}: priority_order must contain primary_action, "
                "every active vitality cue, and every secondary track exactly once"
            )
        if sum(track["mode"] != "inactive" for track in tracks) > 1:
            if not schedule["anti_synchrony_rules"]:
                errors.append(f"motion_schedule {subject_id}: concurrent vitality needs anti-synchrony rules")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="Path to scene_spec.json")
    args = parser.parse_args()
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
        spec = json.loads(args.spec.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
        errors = check_schema(spec, schema, schema)
        if not errors:
            errors.extend(check_traceability(spec))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Valid pre-generation scene specification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
