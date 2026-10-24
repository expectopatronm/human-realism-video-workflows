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

Require the intended Gemini output aspect ratio. Accept only `9:16` or `16:9`; ask the user when neither is supplied, and never infer it from the input image's shape. Treat source-image padding as framing allowance rather than permission to zoom, crop, or recompose the human subject.

## Handoff validation

Run:

    python scripts/validate_handoff.py path/to/planner-output-directory

Stop and ask a targeted question if a required artifact is absent or invalid, the artifacts identify different scenes, `unresolved_conflicts` is non-empty, an input reference needed for generation is unavailable, the target aspect ratio is missing, or a choice would materially change the requested shot. Do not ask about optional details that the planner intentionally left open.

## Prompt compilation

1. Establish the generation mode from `input_plan`: name every supplied image by its declared timeline or semantic role. Never present a semantic reference as a chronological frame. Describe first, intermediate, and last anchors in time order, including exact adherence requirements.
2. Build an internal hard-invariant ledger from the JSON before drafting. Include every held behavior channel, observed limb/contact state, visible-static component, identity or appearance preservation rule, suppressed physiology cue, prohibited substitution, loop boundary, and user-declared invariant. Do not output the ledger, but do not omit an item merely to shorten the prompt.
3. Open with the target aspect ratio, duration when known, continuous-shot intent, and the requested camera/framing state. Do not invent cinematography. Use the guide's natural terms such as `locked-off`, `fixed`, or the requested camera move.
4. Describe the primary human action in chronological order and plain action language. Preserve anchor-to-anchor order, support/contact, subject trajectory, expression, gaze, interactions, and final state. Use exact seconds for major beats only when supported; do not turn every blink, breath, or secondary response into a timestamped command.
5. Add one compact human-realism clause following the planner's motion budget. Preserve the primary action as dominant, keep plainly legible concurrent cues limited, retain quiet-region guards, and name prohibited substitutions. For quiet respiration, explicitly keep mouth aperture, jaw, throat, chin, head height, and shoulder elevation stable unless the plan says otherwise.
6. Add only materially visible causal secondary responses. Do not enumerate every component, anatomy rule, candidate event window, or micro-cue. Convert schedule relationships into natural overlap, lag, damping, and settling rather than a sequence of full-body poses.
7. State identity, appearance, held gesture/limb state, and environment preservation from their actual evidence roles. Do not expand a face reference into authority over body, clothing, pose, or setting.
8. End with the shortest set of shot-critical failure prohibitions not already expressed positively.

Exploit Gemini Omni's world understanding: describe the intended physical result clearly without dumping anatomical rules, JSON field names, AU codes, component IDs, or internal reasoning. Keep the requested performance dominant. Do not add story beats, camera motion, dialogue, audio, appearance changes, or visual details absent from the planner. More planner detail does not justify a longer prompt when the same human behavior can be expressed as one causal instruction.

Before writing the file, compare the draft against the internal hard-invariant ledger. Revise until every human-behavior invariant is represented directly or by an unambiguous higher-level instruction. This is semantic coverage, not a word-matching exercise. In particular, never drop held hands/arms, mouth/jaw/throat locks, support contacts, or facial-expression holds.

For looped work, state the exact loop mode. A ping-pong source must end at the planned zero-velocity turnaround with all driven secondary motion settled; do not falsely require its last frame to match its first frame.

## Output

Write exactly one ready-to-paste prompt to `gemini_omni_1_1_prompt.txt` in the planner output directory unless the user chooses another destination. Do not include a preamble, analysis, JSON, quality checklist, scoring rubric, or claim that video was generated.

Follow [references/output-contract.md](references/output-contract.md) for the final artifact contract.
