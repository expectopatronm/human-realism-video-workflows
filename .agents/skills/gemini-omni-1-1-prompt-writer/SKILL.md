---
name: gemini-omni-1-1-prompt-writer
description: Convert a completed Human Realism Behavior Planner handoff into a ready-to-paste Gemini Omni 1.1 prompt and image-only Google Flow settings manifest. Use after behavior planning; do not use to invent or revise the underlying behavior plan.
---

# Gemini Omni 1.1 Prompt Writer

Compile a validated, model-neutral Human Realism Behavior Planner output into a Gemini Omni 1.1 prompt and a manual Google Flow settings manifest. Preserve the planner's decisions; this skill translates them into an image-only Flow handoff rather than performing behavior planning again.

## Required sources

Read all three canonical planner artifacts from the same output directory:

- `scene_spec.json` — source of truth for facts, timing, references, and constraints.
- `scene_spec.md` — human-readable cross-check; it must not override the JSON.
- `generation_prompt.txt` — model-neutral synthesis to refine, not copy mechanically.

If `motion_schedule_resolved.json` is present, use its seconds-based timing. Otherwise preserve chronological and relative timing from `scene_spec.json`; do not invent exact seconds.

Before writing, read the model guide at `../../../Gemini Omni 1.1 Prompt Writer/Gemini Omni 1.1 Prompting Guide.md`. Do not treat its example prompts as scene content.

This workflow accepts prompt text plus images only. Never require or bind a video as a Gemini/Flow generation input. A motion-reference video may have informed the planner, but the writer uses only its recorded motion evidence and user-approved still-image anchors.

Require the duration the user will select in Google Flow. Resolve the intended output aspect ratio from an explicit current request first, then from `../../../workflow_defaults.json`; ask only when neither supplies it. Accept only `9:16` or `16:9`, and never infer the selection from image dimensions. This repository currently defaults to `16:9`, while an explicit `9:16` request remains supported. Treat the Flow selections as authoritative and use the confirmed duration to resolve timing. Inspect every timeline-anchor image dimension before compilation. For strict composition, each first or last frame must already match the selected aspect ratio within normal integer-rounding tolerance; source padding that retains another ratio is insufficient. Stop and request deterministic canvas preparation rather than asking the model to recompose the image. Use `scripts/prepare_flow_canvas.py` when the user wants neutral code-based extension without altering source pixels.

## Handoff validation

Run:

    python scripts/validate_handoff.py path/to/planner-output-directory

Stop and ask a targeted question if a required artifact is absent or invalid, the artifacts identify different scenes, `unresolved_conflicts` is non-empty, an input image needed for generation is unavailable, the Flow duration or aspect ratio is missing, a strict timeline anchor does not match the selected aspect ratio, an action-critical motion envelope is unresolved or does not fit the selected frame, a critical control lacks a viable enforcement channel, or a choice would materially change the requested shot. Do not ask about optional details that the planner intentionally left open.

## Prompt compilation

1. Establish the image-only generation mode from `input_plan`: map every supplied image to the corresponding Google Flow first-frame, last-frame, intermediate-frame, or reference-image role. Never present a semantic reference as a chronological frame, and never include a video input. Describe timeline anchors in time order, including exact adherence requirements.
2. Build an internal hard-invariant ledger from the JSON. Include every `control_requirement` and its enforcement channel. Include `performance_control`: behavioral reading and prohibited readings, support topology, pelvis height, posture invariants and prohibited normalization, primary-action observability, activation risk, prompt strategy, semantic-activation control, facial-state control, temporal layers, prompt exposure, concurrency class, bounded variability, and reverse-sensitive loop handling. Include `composition_control`: its reference, scale, crop, background registration, visible boundary invariants, off-frame regions, permitted screen-space motion, camera-substitution policy, and complete motion envelope. For each action-critical element, preserve its required visibility and edge clearance across the whole path. Also include every held behavior channel, observed limb/contact state, visible-static component, identity or appearance preservation rule, suppressed physiology cue, prohibited substitution, loop boundary, and user-declared invariant. The ledger is for reasoning, not a list to copy. A requirement enforced by a Flow setting, image anchor, prepared canvas, or deterministic postprocess must not be misrepresented as prompt-only control.
3. Open with the confirmed duration, continuous-shot intent, and one positive composition-lock sentence. Aspect ratio belongs in the Flow manifest, not as a substitute for selecting it in the UI. For strict composition, state that the aspect-matched first frame defines immutable subject scale, crop boundaries, and registered background, then name two or three visible landmarks that remain at the same apparent size and approximate screen position. When action-critical elements move near the boundary, add one concise positive instruction that their complete trajectories remain visible inside the frame with the planned safe margin. Do not describe the unused vertical or horizontal room as an invitation to recompose. Do not repeat camera-motion vocabulary or build a list of lens moves to negate. Never request a wider generated view, zoom-out, or reframing to make a motion envelope fit; the anchor must already provide the needed clearance.
4. Describe the primary human action in chronological order and plain visible language, following `prompt_strategy`. With `direct_evidence`, use only the smallest low-risk set of visible cues. With `holistic_outcome`, describe the overall visible result and keep the diagnostic initiation chain internal. With `reclassify`, use the declared fallback action class; with `accept_ambiguity`, do not claim more mechanical certainty than the crop supports; with `ask_user`, stop. Preserve behavioral reading and posture invariants ahead of diagnostic strength. Never turn hidden mechanics into a sequence of separately animated visible regions. Preserve anchor-to-anchor order, visible posture, subject trajectory, expression, gaze, interactions, and final state. Use exact seconds for major beats and every explicit dwell when supported; never weaken “hold from A to B” into “settled by B.” Keep hidden mechanics behind a visibility firewall: do not name off-frame regions or causal mechanisms unless the shot intentionally reveals or directly interacts with them. Translate hidden causal requirements into visible outcomes.
5. Apply `semantic_activation_control` before drafting action text. Remove social, affective, cinematic, and spatial labels whose likely bundled behavior exceeds the plan. Use `prompt_safe_description`; disambiguate orientation, gaze, screen position, balance, and camera position instead of using overloaded words such as `center`. Treat every social meaning as channel-specific behavior, not permission for a smile, gesture, posture change, or camera move.
6. Apply `facial_state_control` independently from head pose and gaze. For strict authority, state the reference expression positively and permit only the listed changes. When necessary, add one concise shot-critical prohibition covering the prohibited transition; do not rely on a broad phrase such as “preserve expression.”
7. Apply the temporal-layer exposure contract. Write the primary `explicit` layer. Mention a `compact` layer once only when its visible result matters. Do not name `implicit` or `omit` layers. Never enumerate multiple subthreshold head, face, eye, breath, tissue, hair, and fabric motions merely because they exist in the planner; each named motion can become an exaggerated generation target. Translate `slow_deliberate` only onto its own voluntary layer. When needed, summarize all retained background realism in one non-action phrase such as “natural real-time stillness.”
8. Add only materially visible causal secondary responses. Do not enumerate every component, anatomy rule, candidate event window, or micro-cue. Convert schedule relationships into natural overlap, lag, damping, and settling rather than a sequence of full-body poses.
9. State identity, appearance, held gesture/limb state, and environment preservation from their actual evidence roles. Do not expand a face reference into authority over body, clothing, pose, or setting.
10. End only with a genuinely necessary shot-critical prohibition that cannot be expressed positively. Prefer positive invariants. Never append a catalog of prohibited camera moves, pose changes, anatomy failures, or micro-actions.

Exploit Gemini Omni's world understanding: describe the intended physical result clearly without dumping anatomical rules, JSON field names, AU codes, component IDs, or internal reasoning. Keep the requested performance dominant. Do not add story beats, camera motion, dialogue, audio, appearance changes, or visual details absent from the planner. More planner detail does not justify a longer prompt when the same human behavior can be expressed as one causal instruction.

Before writing, compare the draft against the hard-invariant ledger. Revise until each prompt-enforced invariant is represented directly or by an unambiguous positive higher-level instruction, while anchor-, setting-, and postprocess-enforced controls stay in the Flow manifest. Then perform an activation audit: treat every motion noun, verb, named anatomical region, endpoint distinction, social label, affective adjective, cinematic phrase, and ambiguous spatial word as something Gemini may expand. Remove duplicated, hidden, subthreshold, purely diagnostic, bundled, and region-by-region causal language. For restrained behavior, reject a draft that names several sequential body movers, creates multiple distinct poses, changes facial affect without authorization, or makes the primary action more performative than the declared behavioral reading.

For looped work, state the exact loop mode. A ping-pong source must end at the planned zero-velocity turnaround with all driven secondary motion settled; do not falsely require its last frame to match its first frame. Keep reverse-sensitive events away from the turnaround when the plan requires it, and never claim that deterministic replay creates genuinely non-repeating behavior.

If primary-action observability is insufficient or its activation risk is high, follow its fallback and prompt strategy before compiling. Do not write a stronger action claim than the plan can safely make observable. Bounded ambiguity is preferable to changing the action family, posture state, or behavioral reading.

## Output

Write exactly two files in the planner output directory:

- `gemini_omni_1_1_prompt.txt` — only the ready-to-paste prompt, without a preamble, analysis, checklist, or generation claim.
- `google_flow_settings.json` — the manual Flow selections and image-slot bindings: execution surface, model label, duration, aspect ratio, prompt filename, image-only input policy, each image path and declared role, source dimensions, aspect-match result, and any deterministic postprocess.

Run `scripts/validate_flow_package.py` on the output directory before delivery.

Follow [references/output-contract.md](references/output-contract.md) for the final artifact contract.
