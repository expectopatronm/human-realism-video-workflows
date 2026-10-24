---
name: human-realism-behavior-planner
description: Plan complete, model-neutral human behavior and motion from first, last, timed intermediate, and semantic reference images plus scene intent. Use for photorealistic image-to-video work before any model-specific prompting or generation.
---

# Human Realism Behavior Planner

Produce a model-neutral pre-generation behavior plan for each human subject in an image-to-video scene. The supported knowledge base covers adult female anatomy; apply its rules conditionally to the actual subject, framing, and action. Do not present an unobserved characteristic as a reference fact.

## Knowledge base

Use these three existing guideline files as the anatomy and component knowledge base:

- ../../../Human Realism Behavior Planner/Human Appearance, Anatomy & Motion Realism Standard.md — purpose, G01–G29 global rules, and Level 2 component IDs and requirements.
- ../../../Human Realism Behavior Planner/Standard Template A — Master Component Rule.md — interpret the applicable rule dimensions (anatomy, appearance, motion, physics, interaction, continuity, applicability).
- ../../../Human Realism Behavior Planner/Standard Template B — Agent-Generated Scene Specification.md — component-level structure A–H and J.

Do not read or use a model-specific prompting guide while constructing A–C. A separate downstream prompting skill may use its guide after the behavior plan is complete. Do not edit any knowledge-base file. Load the global rules and only the Level 2 entries relevant to the scene; do not paste the entire inventory into an output.

For exact output keys and statuses, read [references/output-contract.md](references/output-contract.md). The machine-readable contract is [references/scene-spec.schema.json](references/scene-spec.schema.json).
Use [references/selection-policy.md](references/selection-policy.md) to resolve incomplete, contradictory, ambiguous, or physically implausible intent and to select baseline vitality. This policy operationalizes the standard and is not an additional anatomy source.
Use [references/behavior-planning.md](references/behavior-planning.md) for the model-neutral behavior channels, movement quality, facial actions, physiology coupling, passive dynamics, scene physics, and clarification gate. Its research basis informs planning without changing the anatomy source files.
Use [references/multi-image-conditioning.md](references/multi-image-conditioning.md) to distinguish timeline anchors from semantic references, enumerate all supported image combinations, segment anchor-to-anchor motion, and decide when image-role or timing ambiguity requires a question.

## Inputs

Require at least one accessible image and the user's scene intent. Accept a first frame, last frame, timed intermediate frames, unpinned semantic references, or any non-empty combination of those four classes. In this repository, treat the four subfolders under `Human Realism Behavior Planner/images/` as authoritative role declarations. Read scene intent from the user's request. If an image cannot be opened, an intermediate time is missing, an image role is ambiguous, or the intended action is too incomplete to establish a scene, ask for the missing decision. Otherwise proceed, recording ordinary uncertainty and reversible assumptions. Distinguish visually observed facts, explicit user wishes, and inferred staging.

## Workflow

1. **Input-role resolution.** Inventory all images before interpreting their content. Classify each as first frame, last frame, timed intermediate frame, semantic reference, or an explicitly declared dual role. Derive one of the fifteen supported configurations. Require explicit intermediate times and semantic targets; never convert multiple reference views into chronological frames. Build `input_plan`, sort anchors, and divide the full timeline into consecutive anchor-to-anchor segments. Require first and last anchors for a seamless loop. For ping-pong playback, allow first-frame-only input and make the generated endpoint a stable zero-velocity turnaround that reverses without a visible jerk.
2. **Reference analysis.** Inspect each image directly. Assign scene, subject, and reference IDs. Record visible anatomy, appearance, pose, clothing, accessories, setting, occlusion, confidence, and unknowns. For each subject, define identity anchors, view coverage, and a policy for regions that planned movement may reveal. Reconcile multiple views without treating hidden details as observed or allowing one reference role to silently govern another.
3. **Intent interpretation and clarification.** Separate requested action, expression, camera, environment, timing, appearance changes, anchor states, and semantic preservation from reference facts and assumptions. Do not invent narrative behavior. Identify omissions, ambiguity, contradictions, reference conflicts, impossible anchor transitions, and physical impossibilities. Apply the selection policy and both clarification gates. Ask targeted questions before final output when a choice would materially change the user's purpose; record answers and other material decisions in `intent_resolutions` and resolved role conflicts in `input_plan`.
4. **Baseline realism selection.** For each subject, determine subject state and realism mode, then explicitly decide respiration, blinking, ocular fixation, facial tonus, and postural micro-adjustment. Treat visible baseline physiology as part of rendering a living subject rather than as an optional story action. When an action repeats, specify bounded variation in at least two dimensions unless exact repetition is intentional.
5. **Behavior and scene physics.** Build one `behavior_plan` per subject with all seven channel dispositions and applicable phase synchronization, Body/Space/Shape/Effort for each beat, a visibility-aware facial AU plan, explicit extended-physiology decisions, relevant physiology couplings, and an acyclic causal dynamics graph. Build `scene_physics` for objects, qualitative force fields, support/contact, environmental drivers, and visible dependencies. Keep inferred movement quality and unseen details explicit.
6. **Spatial and interaction planning.** Build `spatial_plan` separately from body behavior. Describe the camera track and each subject's path, depth, orientation, support, and reference coverage. Decouple camera motion from subject motion. For human-object, human-human, and human-environment interaction, specify roles, affordances, approach, contact, manipulation, release, and reactions as applicable. Record planned occlusion and reappearance. If a material viewpoint change exposes unsupported identity detail, ask for another reference or constrain the movement before final output.
7. **Scene timeline and motion scheduling.** Lay out initial state, ordered action beats, simultaneous movements, dependencies, and final state. Reconcile every beat and primary phase with its enclosing input-plan segment and the anchor state at each boundary. If a motion-reference video is supplied, register it in `motion_sources` and extract its travel, rotation, burst/dwell rhythm, tempo, contact, recoil, and follow-through while excluding its identity and setting unless requested. Build one normalized `motion_schedule` per subject using the [motion scheduling contract](references/motion-scheduling.md). Separate active travel from dwell, state tempo and velocity profiles, define articulated kinematic chains, and schedule vitality only around the preserved primary performance. Protected windows must be existing dwells; never invent pauses or slow motion to expose a cue.
8. **Anatomical selection.** Classify relevant Level 2 components as active, visible-static, occluded, outside-frame, n/a, or uncertain across the planned sequence. Detail active components, preserve visible-static ones, and include hidden components only when motion or reappearance matters. Every required or conditional baseline cue must select at least one supporting component and `G16`.
9. **Rule application.** Map relevant G01–G29 and Level 2 IDs to each selected component. Use Template A's dimensions to populate Template B's observation, preservation, primary and secondary motion, physics, deformation, interaction, continuity, negative constraints, and traceability.
10. **Dependency resolution.** Align connected anatomy, respiration, gaze and expression, weight transfer, clothing, hair, soft tissue, object contact, lighting, camera perspective, anchor transitions, and occlusion/reappearance. Give every secondary movement a physical or anatomical driver. Preserve bounded human variation without adding random or unrelated motion.
11. **Plan construction.** Assemble image roles, anchors, semantic assignments, interpolation segments, subject and reference metadata, scene intent, realism selection, behavior plans, spatial plan, scene physics, motion schedule, intent resolutions, global constraints, selected component requirements, assumptions, and traceability into one coherent specification.
12. **Preflight validation.** Check configuration against assigned roles; anchor order and timing; semantic targets; dual-role declarations; segment coverage and boundary alignment; reference conflicts; anchor-to-anchor feasibility; identity-anchor references; subject and camera paths; interaction roles and affordances; occlusion/reappearance; channel and beat coverage; phase synchronization; facial timing and combinations; extended-physiology dispositions; dynamics links and propagation; object and force references; support/contact; baseline-cue disposition; schedule coverage and window order; cue/status agreement; event duration; protected-window separation; priority coverage; variation realization; anti-synchrony; timing and physics; reference fidelity; and evidence boundaries. Resolve or report contradictions. This checks the plan before generation; it is not generated-video quality assessment.
13. **Deliver only these three artifacts:** (A) structured scene specification JSON matching the schema; (B) a human-readable specification reflecting the same facts and constraints; (C) a model-neutral generation brief derived from them. Compile the input, behavior, spatial, physics, and motion plans into natural visible behavior while keeping the requested primary action dominant. If a blocking question remains unanswered, ask it before delivering these artifacts. Do not include model-specific syntax, a quality assurance checklist, evaluation status, scoring rubric, or post-generation review.

If writing files, use scene_spec.json, scene_spec.md, and generation_prompt.txt together in the requested output directory. If responding in chat, label A, B, and C clearly. Do not claim that video was generated. Before delivering JSON, run the included structural validator:

    python scripts/validate_spec.py path/to/scene_spec.json

For the repository folder workflow, inventory image roles before visual planning:

    python scripts/resolve_image_inputs.py "../../../Human Realism Behavior Planner/images" --duration 10

The validator checks the pre-generation specification's format and traceability. It does not evaluate generated video.

When a destination duration is known, resolve the normalized schedule before model-specific compilation:

    python scripts/resolve_motion_schedule.py path/to/scene_spec.json --duration 12 --output path/to/motion_schedule_resolved.json

This conversion preserves input anchors and interpolation segments, behavior, spatial planning, scene physics, candidate event windows, count ranges, event-duration bounds, protected windows, priority, coordination, and anti-synchrony. It does not choose exact blink frames or generate random motion.

When the user requests a Gemini Omni 1.1 handoff, invoke `$gemini-omni-1-1-prompt-writer` on the complete planner output directory. Pass all three canonical artifacts and the resolved motion schedule when available. Keep this skill's structured specification as the source of truth.
