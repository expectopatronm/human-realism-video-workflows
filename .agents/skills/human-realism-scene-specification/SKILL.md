---
name: human-realism-scene-specification
description: Turn reference images and a user's intended image-to-video scene into a traceable human realism scene specification and generation prompt. Use for photorealistic human subject planning before video generation.
---

# Human Realism Scene Specification

Produce a pre-generation specification for the human subject in an image-to-video scene. The supported knowledge base covers adult female anatomy; apply its rules conditionally to the actual subject, framing, and action. Do not present an unobserved characteristic as a reference fact.

## Knowledge base

Use only these three existing guideline files as the knowledge base:

- ../../../Human Realism Scene Specification Skill/Human Appearance, Anatomy & Motion Realism Standard.md — purpose, G01–G29 global rules, and Level 2 component IDs and requirements.
- ../../../Human Realism Scene Specification Skill/Standard Template A — Master Component Rule.md — interpret the applicable rule dimensions (anatomy, appearance, motion, physics, interaction, continuity, applicability).
- ../../../Human Realism Scene Specification Skill/Standard Template B — Agent-Generated Scene Specification.md — component-level structure A–H and J.

Do not read or use the Gemini Omni Prompting Guide while constructing A–C. The separate [Gemini Omni Human Realism Video Prompting](../gemini-omni-human-realism-video-prompting/SKILL.md) skill may use it after the scene specification is complete. Do not edit any knowledge-base file. Load the global rules and only the Level 2 entries relevant to the scene; do not paste the entire inventory into an output.

For exact output keys and statuses, read [references/output-contract.md](references/output-contract.md). The machine-readable contract is [references/scene-spec.schema.json](references/scene-spec.schema.json).

## Inputs

Require at least one accessible reference image and the user's scene intent. Accept multiple images, each with a stable reference ID. If an image cannot be opened or the intended action is too incomplete to establish a scene, ask for that missing input. Otherwise proceed, recording ordinary uncertainty and reversible assumptions. Distinguish visually observed facts, explicit user wishes, and inferred staging.

## Workflow

1. **Reference analysis.** Inspect each image directly. Assign scene, subject, and reference IDs. Record visible anatomy, appearance, pose, clothing, accessories, setting, occlusion, confidence, and unknowns. Reconcile multiple views without treating hidden details as observed.
2. **Intent interpretation.** Separate the user's requested action, expression, camera, environment, timing, and appearance changes from reasonable assumptions. Add no unrequested behavior.
3. **Scene timeline.** Lay out initial state, ordered action beats, simultaneous movements, dependencies, and final state. Assign timing only when supplied or necessary, and label assumed timing.
4. **Anatomical selection.** Classify relevant Level 2 components as active, visible-static, occluded, outside-frame, n/a, or uncertain across the planned sequence. Detail active components, preserve visible-static ones, and include hidden components only when motion or reappearance matters.
5. **Rule application.** Map relevant G01–G29 and Level 2 IDs to each selected component. Use Template A's dimensions to populate Template B's observation, preservation, primary and secondary motion, physics, deformation, interaction, continuity, negative constraints, and traceability.
6. **Dependency resolution.** Align connected anatomy, gaze and expression, weight transfer, clothing, object contact, lighting, camera perspective, and occlusion/reappearance. Resolve conflicts in this order: applicable safety and consent constraints; explicit user instructions and intentional creative changes; reference-established identity and appearance; anatomical and physical plausibility; scene-inferred behavior; optional embellishment. Record conflicts that remain.
7. **Specification construction.** Assemble subject and reference metadata, scene intent, global constraints, timeline, selected component requirements, negative constraints, assumptions, and traceability into one coherent scene specification.
8. **Preflight validation.** Check that requested actions and important active regions are covered, timing and physics are compatible, reference appearance is preserved, unknowns are not presented as facts, and mandatory requirements are distinguished from optional details. Resolve or report contradictions. This checks the specification before generation; it is not generated-video quality assessment.
9. **Deliver only these three artifacts:** (A) structured scene specification JSON matching the schema; (B) a human-readable specification reflecting the same facts and constraints; (C) a direct generation prompt derived from them. The prompt should state subject/reference preservation, action beats, camera, relevant physical behavior, and high-priority exclusions. Do not include a quality assurance checklist, evaluation status, scoring rubric, or post-generation review.

If writing files, use scene_spec.json, scene_spec.md, and generation_prompt.txt together in the requested output directory. If responding in chat, label A, B, and C clearly. Do not claim that video was generated. Before delivering JSON, run the included structural validator:

    python scripts/validate_spec.py path/to/scene_spec.json

The validator checks the pre-generation specification's format and traceability. It does not evaluate generated video.

When the user requests a Gemini Omni-specific handoff, pass the validated JSON and available reference-image mapping to the separate Gemini Omni skill. Keep this skill's structured specification as the source of truth.
