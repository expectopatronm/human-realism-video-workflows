---
name: gemini-omni-1-1-prompt-writer
description: Convert a completed Human Realism Behavior Planner handoff into a ready-to-use Gemini Omni 1.1 image-to-video prompt. Use after behavior planning; do not use to invent or revise the underlying behavior plan.
---

# Gemini Omni 1.1 Prompt Writer

Compile a validated, model-neutral Human Realism Behavior Planner output into one Gemini Omni 1.1 generation prompt. Preserve the planner's decisions; this skill translates them into model-appropriate natural language rather than performing behavior planning again.

## Required sources

Read all three canonical planner artifacts from the same output directory:

- `scene_spec.json` — source of truth for facts, timing, references, and constraints.
- `scene_spec.md` — human-readable cross-check; it must not override the JSON.
- `generation_prompt.txt` — model-neutral synthesis to refine, not copy mechanically.

If `motion_schedule_resolved.json` is present, use its seconds-based timing. Otherwise preserve chronological and relative timing from `scene_spec.json`; do not invent exact seconds.

Before writing, read the model guide at `../../../Gemini Omni 1.1 Prompt Writer/Gemini Omni 1.1 Prompting Guide.md`. Do not treat its example prompts as scene content.

## Handoff validation

Run:

    python scripts/validate_handoff.py path/to/planner-output-directory

Stop and ask a targeted question if a required artifact is absent or invalid, the artifacts identify different scenes, `unresolved_conflicts` is non-empty, an input reference needed for generation is unavailable, or a choice would materially change the requested shot. Do not ask about optional details that the planner intentionally left open.

## Prompt compilation

1. Establish the generation mode from `input_plan`: name every supplied image by its declared timeline or semantic role. Never present a semantic reference as a chronological frame. Describe first, intermediate, and last anchors in time order, including exact adherence requirements.
2. Open with the shot identity: duration when known, style, subject, location, framing, continuous-shot intent, and camera behavior. Use the guide's natural videography language such as `locked-off`, `fixed`, or the requested camera move.
3. Describe the primary action chronologically. Preserve anchor-to-anchor segments, action ordering, support/contact, subject trajectory, expression, gaze, interactions, occlusion, and the final state. Use seconds only when supported by the validated input or resolved schedule.
4. Integrate living realism as visible cause and effect: posture and weight transfer drive connected anatomy; acceleration and deceleration drive hair, fabric, and soft-tissue response; breathing, blinking, fixation, facial tonus, and micro-adjustment retain their planner-assigned status, timing, priority, and anti-synchrony.
5. State identity, appearance, composition, lighting, and environment preservation from their actual evidence roles. Do not expand a face reference into authority over body, clothing, pose, or setting.
6. End with a compact preservation and avoidance clause containing only shot-critical failure modes. Prefer affirmative direction, but retain explicit prohibitions when the planner marks them as important.

Exploit Gemini Omni's world understanding: describe the intended physical result clearly without dumping anatomical rules, JSON field names, AU codes, component IDs, or internal reasoning. Keep the requested performance dominant. Do not add story beats, camera motion, dialogue, audio, appearance changes, or visual details absent from the planner.

For looped work, state the exact loop mode. A ping-pong source must end at the planned zero-velocity turnaround with all driven secondary motion settled; do not falsely require its last frame to match its first frame.

## Output

Write exactly one ready-to-paste prompt to `gemini_omni_1_1_prompt.txt` in the planner output directory unless the user chooses another destination. Do not include a preamble, analysis, JSON, quality checklist, scoring rubric, or claim that video was generated.

Follow [references/output-contract.md](references/output-contract.md) for the final artifact contract.
