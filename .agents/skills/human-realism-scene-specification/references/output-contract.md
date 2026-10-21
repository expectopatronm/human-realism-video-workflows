# Output contract

## A. Structured JSON

Use the keys and enums in scene-spec.schema.json. The root contains:

- schema_version = "1.0" and a stable scene_id.
- references: every inspected image, its path or user-provided handle, concise observation, and confidence.
- subjects: one entry per person, with the image IDs supporting identity and explicit appearance changes.
- intent: the user's request, setting/camera/duration when supplied, initial state, ordered beats, and final state. Unknown optional scene settings are null.
- global_rules: selected G01–G29 rules with scene-specific constraints.
- components: selected Level 2 components, each with Template B's observation, intent, preservation, primary motion, secondary motion, deformation/interaction, continuity, negative constraints, and traceability. Template B's acceptance/evaluation section is intentionally absent.
- assumptions and unresolved_conflicts: explicit limits of the evidence and decisions.

Use exact Level 2 component IDs such as "03.02", not invented identifiers. The component name should match the source heading. Put observed reference details only in reference_observation; put planned changes and plausible unseen behavior in the other fields or assumptions. A component can be active, visible-static, occluded, outside-frame, n/a, or uncertain. Include occluded/outside-frame components only when they causally matter to the visible scene.

For a stationary component, set primary_motion.required to "no", give a short stillness description, and keep timing null. Secondary motion may independently be "no" or "conditional". Avoid generic breathing, blinking, or hair motion unless the scene makes them relevant.

Keep arrays empty where the category has no applicable constraint. Use null for unknown scalar details. Reference IDs in every component and subject must exist in references. Subject IDs in beats and components must exist in subjects. Every global rule ID must exist in the standard. A traceable component should cite at least one relevant global rule.

## B. Human-readable specification

Use the same scene ID, subjects, references, action beats, selected component IDs, motion/physics, preservation constraints, assumptions, and unresolved conflicts as A. Organize for quick human review; group low-impact components when doing so remains unambiguous. State uncertainty plainly. Do not add facts or actions absent from A.

## C. Generation prompt

Write a single ready-to-use prompt or a concise positive prompt plus negative constraints. Identify the subject by reference image IDs or handles. Describe the visible beginning, ordered action, ending, camera, contact, physical response, and invariant appearance. Prioritize constraints that materially affect this shot. Do not dump the full JSON or every anatomical rule. If an unresolved conflict blocks a faithful prompt, state the needed user choice instead of silently choosing a version.

No artifact includes a quality assurance checklist, pass/fail status, generated-video evaluation, or post-generation instructions.
