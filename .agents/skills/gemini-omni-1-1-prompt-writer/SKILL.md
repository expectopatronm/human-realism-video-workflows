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
2. Build an internal hard-invariant ledger from the JSON before drafting. Include `performance_control`: behavioral reading and prohibited readings, support topology, pelvis height, posture invariants and prohibited normalization, primary-action observability, temporal layers, prompt exposure, concurrency class, bounded variability, and reverse-sensitive loop handling. Include `composition_control`: its reference, scale, crop, background registration, visible boundary invariants, off-frame regions, permitted screen-space motion, and camera-substitution policy. Also include every held behavior channel, observed limb/contact state, visible-static component, identity or appearance preservation rule, suppressed physiology cue, prohibited substitution, loop boundary, and user-declared invariant. The ledger is for reasoning, not a list to copy. A constraint may be enforced by omission or by one positive invariant.
3. Open with the target aspect ratio, duration when known, continuous-shot intent, and one positive composition-lock sentence. For strict composition, state that the first frame defines immutable subject scale, crop boundaries, and registered background, then name two or three visible landmarks that remain at the same apparent size and approximate screen position. Do not repeat camera-motion vocabulary or build a list of lens moves to negate.
4. Describe the primary human action in chronological order and plain visible language. Compile its completion criterion, initiation order, endpoint evidence, and the smallest set of required visible cues that distinguishes it from the listed substitutions. Do not rely on the action label alone. Preserve anchor-to-anchor order, visible posture, subject trajectory, expression, gaze, interactions, and final state. Use exact seconds for major beats and every explicit dwell when supported; never weaken “hold from A to B” into “settled by B.” Keep hidden mechanics behind a visibility firewall: do not name off-frame regions or causal mechanisms unless the shot intentionally reveals or directly interacts with them. Translate hidden causal requirements into visible outcomes.
5. Apply the temporal-layer exposure contract. Write the primary `explicit` layer. Mention a `compact` layer once only when its visible result matters. Do not name `implicit` or `omit` layers. Never enumerate multiple subthreshold head, face, eye, breath, tissue, hair, and fabric motions merely because they exist in the planner; each named motion can become an exaggerated generation target. Translate `slow_deliberate` only onto its own voluntary layer. When needed, summarize all retained background realism in one non-action phrase such as “natural real-time stillness.”
6. Add only materially visible causal secondary responses. Do not enumerate every component, anatomy rule, candidate event window, or micro-cue. Convert schedule relationships into natural overlap, lag, damping, and settling rather than a sequence of full-body poses.
7. State identity, appearance, held gesture/limb state, and environment preservation from their actual evidence roles. Do not expand a face reference into authority over body, clothing, pose, or setting.
8. End only with a genuinely necessary shot-critical prohibition that cannot be expressed positively. Prefer positive invariants. Never append a catalog of prohibited camera moves, pose changes, anatomy failures, or micro-actions.

Exploit Gemini Omni's world understanding: describe the intended physical result clearly without dumping anatomical rules, JSON field names, AU codes, component IDs, or internal reasoning. Keep the requested performance dominant. Do not add story beats, camera motion, dialogue, audio, appearance changes, or visual details absent from the planner. More planner detail does not justify a longer prompt when the same human behavior can be expressed as one causal instruction.

Before writing the file, compare the draft against the internal hard-invariant ledger. Revise until every required visible invariant is represented directly, by an unambiguous positive higher-level instruction, or by intentionally withholding hidden mechanics and nonessential motion targets. This is semantic coverage, not a word-matching exercise. Then perform an activation audit: treat every motion noun and verb in the draft as something Gemini may animate. Remove duplicated, hidden, subthreshold, and purely diagnostic motion language. Preserve observed held regions through positive visible-state language rather than exposing off-frame causal detail.

For looped work, state the exact loop mode. A ping-pong source must end at the planned zero-velocity turnaround with all driven secondary motion settled; do not falsely require its last frame to match its first frame. Keep reverse-sensitive events away from the turnaround when the plan requires it, and never claim that deterministic replay creates genuinely non-repeating behavior.

If primary-action observability is insufficient, follow its fallback before compiling: ask the user, constrain the result to visible behavior, or use the declared fallback action class. Do not write a stronger action claim than the plan can make observable.

## Output

Write exactly one ready-to-paste prompt to `gemini_omni_1_1_prompt.txt` in the planner output directory unless the user chooses another destination. Do not include a preamble, analysis, JSON, quality checklist, scoring rubric, or claim that video was generated.

Follow [references/output-contract.md](references/output-contract.md) for the final artifact contract.
