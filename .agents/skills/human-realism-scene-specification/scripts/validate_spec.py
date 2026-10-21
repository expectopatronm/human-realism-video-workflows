"""Validate a pre-generation human realism scene specification."""

import argparse
import json
import re
import sys
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
SCHEMA = SKILL / "references" / "scene-spec.schema.json"
STANDARD = ROOT / "Human Realism Scene Specification Skill" / "Human Appearance, Anatomy & Motion Realism Standard.md"


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
        if rule.get("uniqueItems") and len(value) != len(set(value)):
            errors.append(f"{path}: duplicate items")
        if "items" in rule:
            for index, item in enumerate(value):
                errors.extend(check_schema(item, rule["items"], schema, f"{path}[{index}]"))
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
