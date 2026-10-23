---
name: gemini-omni-human-realism-video-prompting
description: Compile a Human Realism Behavior Planner and its reference-image plan into a Gemini Omni video prompt. Use for the Gemini Omni handoff after human behavior planning, not for generating or evaluating video.
---

# Gemini Omni Human Realism Video Prompting

Turn the completed human realism scene plan into one ready-to-paste Gemini Omni prompt. The scene specification defines **what** must happen; the [local Gemini Omni guide](../../../Gemini%20Omni%20Human%20Realism%20Video%20Prompting%20Skill/Gemini%20Omni%20Prompting%20Guide.md) informs **how to phrase it**. This skill prepares a prompt and reference attachment instructions. It does not call a video model or review generated video.

## Inputs and precedence

- Primary input: `scene_spec.json` from [Human Realism Behavior Planner](../human-realism-behavior-planner/SKILL.md), matching its [schema](../human-realism-behavior-planner/references/scene-spec.schema.json).
- Useful context: the paired `scene_spec.md` and `generation_prompt.txt`, the source reference images or handles, their intended attachment order, and any user-specified Gemini surface or presentation settings.
- If no structured specification exists but the user supplied images and scene intent, run the Human Realism Behavior Planner skill first, then continue here. If neither a specification nor enough inputs to create one are available, ask for the missing material.
- Treat the JSON as authoritative for subjects, reference observations, requested changes, ordered beats, camera, setting, timing, constraints, assumptions, and conflicts. Use B and C to clarify wording, never to override A. A new creative instruction that changes the scene must be reconciled into A before compiling the Gemini prompt.

## Compile the prompt

1. Read the JSON and validate it with `python .agents/skills/human-realism-behavior-planner/scripts/validate_spec.py path/to/scene_spec.json` from the repository root. Resolve malformed input with the upstream skill or ask for a corrected specification.
2. Read the local Gemini Omni prompting guide. Use its relevant concepts: shot framing and motion, style, lighting, location, action, direct camera language, real-world plausibility, and concise descriptions of complex actions. Read [references/prompt-patterns.md](references/prompt-patterns.md) for the field mapping and reference rules.
3. Check every `references[].id` against the supplied media. Establish a clear attachment order or user-provided handles; if none is specified, propose the JSON reference order and label it as proposed. Do not claim an image is attached when it is unavailable. Never assume `R1` automatically means Gemini's first image token.
4. Identify any unresolved conflict that changes identity, action, camera, contact, or the final state. Ask for that decision before producing a definitive prompt. Carry nonblocking uncertainty conservatively; do not turn an unknown into an observed detail.
5. Write natural language centered on the subject and references, initial state, ordered action, final state, camera, setting, and only the physical details that materially affect this shot. Use portable natural language when the Gemini surface is unknown. Preserve explicit timing; do not invent timecodes. Make a continuous shot explicit when the specification requires continuity, since Omni can otherwise choose multiple shots. Use a few high-priority visual exclusions rather than copying every rule ID or negative constraint.
6. Compare the draft to A: same people, reference roles, action order, appearance changes, camera, contact sequence, and ending. Remove unsupported embellishment. Do not include JSON keys, component IDs, citations, a quality checklist, or post-generation evaluation in the paste-ready prompt.

## Output

Return **Gemini Omni prompt** as a single copyable prompt. Follow it with a short **Reference attachments** note mapping each scene ID to the actual media/attachment order when references are needed. State missing attachments plainly. If the user requested files, save the prompt alone as `gemini_omni_prompt.txt`; keep the attachment mapping in the reply or a separate handoff note if needed. Do not silently submit the prompt to Gemini or claim that a video was created.

The local guide is the project's primary Omni phrasing source. For a platform-specific tag, setting, or current feature that the guide does not cover, check current [Google DeepMind prompting guidance](https://deepmind.google/models/gemini-omni/prompt-guide/) or [Gemini API documentation](https://ai.google.dev/gemini-api/docs/omni) before using it. Avoid API tokens or settings in a prompt meant for Gemini or Flow unless the user selected that surface and the media mapping is known.
