# Human realism selection policy

Use this policy while converting reference evidence and user intent into the scene specification. It operationalizes the Human Realism Standard; it does not replace it.

## Selection principle

Preserve the user's story and requested action while supplying the minimum visible physiology needed for a living human to read as alive. Baseline physiology is not a new narrative action. Do not invent gestures, emotions, gaze targets, prop interactions, or camera moves.

For every subject, make an explicit decision for all five baseline cues: respiration, blinking, ocular fixation, facial tonus, and postural micro-adjustment. Never omit a cue merely because the user did not mention it.

## Resolve imperfect intent

Apply evidence and constraints in this order:

1. Applicable safety and consent constraints.
2. Explicit intentional stylization or nonrealism.
3. The user's scene purpose, requested action, and current reference evidence.
4. Anatomical and physical plausibility.
5. Baseline physiology for the subject's state, visibility, support, and shot duration.
6. Optional embellishment.

Record every material repair in `intent_resolutions`:

- **Omission:** infer a conservative baseline only when it is visible and compatible with the scene. Record the assumption when it materially affects the prompt.
- **Ambiguity:** choose the smallest reversible interpretation that preserves the request. Ask the user before final output if different choices would substantially change identity, story, framing, contact, or the ending.
- **Contradiction:** reconcile an obvious local conflict from the surrounding request and reference. Ask the user when there is no reliable basis for choosing a material alternative.
- **Physical impossibility:** for a naturalistic scene, replace the impossible mechanism with the nearest feasible action that preserves its purpose. Describe the correction. For clearly intentional fantasy or stylization, retain it and mark `intentional_stylization`.
- **Reference conflict:** an explicit requested change may override reference appearance. Otherwise preserve reference-established identity and visible state.

Do not silently alter identity, narrative meaning, emotional intent, framing, object contact, or the requested final state.

## Human-performance clarification gate

Read [human-motion-control.md](human-motion-control.md) for restrained, idle, held, looped, micro-realistic, hidden-support, or one-anchor performances. Ask one grouped set of questions before final output when the user has not established a materially important human-control choice:

- primary-motion magnitude;
- facial freedom and whether mouth, jaw, throat, brows, or cheeks are locked;
- respiration readability and permitted regions;
- held limbs, contacts, and support assumptions;
- duration meaning and loop endpoint behavior.

Treat first-frame-only control of a long or multi-phase action, occluded support mechanics, held expression with visible respiration, several competing micro-cues, and strict loops without an endpoint anchor as higher uncertainty. Do not hide that uncertainty inside ordinary assumptions. Offer the smallest naturalistic option as a default, but obtain the user's answer when the alternatives visibly change the performance.

Safety, age, consent, or identity confirmation may still be necessary, but it does not satisfy this performance gate.

## Baseline cue decisions

Use `required` when the cue should be plainly represented, `conditional` when its expression depends on a beat or visibility, `suppressed` only for an explicit or physically justified reduction, `not_visible` when framing or occlusion hides it, `not_applicable` for a nonliving subject, and `uncertain` when evidence is inadequate.

### Respiration

- Usually required or conditional for an awake living subject in a multi-second shot when the upper torso is visible.
- For quiet breathing, initiate primarily in the lower ribcage and upper abdomen. Upper chest, clothing, and supported soft tissue may follow secondarily according to framing; shoulder and neck-base motion should be absent or nearly imperceptible unless breathing is deliberately pronounced.
- Use a non-metronomic phase and amplitude description. Do not make each cycle identical.
- Explicitly hold jaw, lip aperture, tongue, throat, chin, head height, and gaze unless speech, swallowing, gasping, exertion, or another requested action requires them. Parted lips do not authorize mouth breathing or mouth-shape drift.
- Prohibit throat bobbing, chin lift, head recoil, shoulder shrug, and whole-body vertical pulsing for ordinary quiet respiration.
- Suppress only for a justified breath hold, strong exertion phase, speech pattern, medical state, or explicit intentional stillness. A suppressed cue still needs a rationale.

Supporting Level 2 components can include `10.01`, `10.02`, `10.03`, `15.01`, `15.02`, and `15.04`.

### Blinking

- Usually required or conditional when an awake subject's eyes are visible for multiple seconds.
- Preserve gaze intent through closure and reopening. Eyelashes follow the eyelids rather than acting independently.
- Specify sparse, irregular placement compatible with the action. Do not use clocklike intervals or require constant blinking.
- Suppress only when a deliberately unbroken stare is central to the requested performance, and record the tradeoff.

The principal supporting component is `03.02`.

### Ocular fixation

- Usually required when the eyes are visible, including direct eye contact.
- Keep fixation stable at the narrative target while allowing restrained coordinated correction. Do not turn micro-correction into side-to-side looking or wandering gaze.

The principal supporting component is `03.05`.

### Facial tonus

- Usually required or conditional when the face is visible, even for a neutral, bored, or stone-still expression.
- Preserve the requested expression with restrained eyelid, cheek, brow, jaw, and lip coordination. Neutrality does not mean frozen facial tissue.
- Do not add arbitrary eyebrow raises, lip motion, twitching, or a change of emotion.
- When the expression is held, keep unrequested jaw, lip-aperture, throat, brow, and cheek actions held. Living tonus is not a micro-expression loop.

Supporting components can include `02.03`, `03.02`, `03.03`, `05.02`, `07.01`, `07.02`, and `07.03`.

### Postural micro-adjustment

- Usually required or conditional for unsupported standing, seated balance, or held poses lasting multiple seconds.
- Couple small head, neck, shoulder, spine, pelvis, and support changes to balance and the requested primary action.
- Reduce or suppress it when the subject is externally supported, deliberately immobilized, asleep, unconscious, or intentionally stylized as frozen.
- Do not turn it into an independent sway, nod, shrug, or whole-body pose change. It should support balance and remain subordinate to the primary action.

Supporting components can include `08.01`, `08.02`, `09.03`, `11.01`, `11.03`, `15.05`, and `16.01`.

Every active baseline cue requires `G16`, at least one relevant Level 2 component, a visible effect, a timing strategy, and bounded variability.

## Repeated human action

When an action repeats, decide whether natural variation is required. For naturalistic human repetition, vary at least two of these dimensions within narrow bounds:

- `interval` or `dwell_duration`;
- `amplitude`;
- `trajectory` or `endpoint`;
- `acceleration_profile`;
- `inter_region_phase` between connected body regions;
- `secondary_response` or `settling`.

Variation must remain causal and compatible with the requested rhythm. It should prevent mechanical duplication without producing random motion or changing the action. Exact repetition is appropriate only when the user requests mechanical motion, a mathematically exact loop, or intentional nonrealism.

## Motion budget

Prioritize the requested primary action. Allow at most one or two additional cues to be plainly legible at the same moment unless the action physiologically requires more. Represent other applicable cues below deliberate-performance amplitude or conditionally suppress them with a scene-specific rationale. Secondary motion must have a driver: respiration, inertia, gravity, contact, muscle action, or the primary movement. Do not independently animate every visible body part.

Hair, fabric, soft tissue, eyelids, eyelashes, shoulders, and facial regions should respond to their physical or anatomical drivers. Their movement should include a small lag or settling when appropriate, not an unrelated decorative loop.

## Motion scheduling

After selecting vitality and repetition behavior, build one `motion_schedule` per subject. Apply the detailed [motion scheduling contract](motion-scheduling.md). Use normalized clip windows from `0.0` to `1.0` so the schedule remains independent of the destination duration.

1. Map every beat involving the subject to one ordered, non-overlapping primary phase. Preserve user timing when supplied; otherwise choose and record conservative relative timing.
2. Put repeated instances in a shared `repetition_group`. The first instance establishes the movement family. Every later instance identifies bounded differences drawn from the selected repetition dimensions.
3. Create exactly one prioritized vitality track for each baseline cue. Use `continuous` for ongoing fixation or tonus, `event` for sparse actions such as blinks, `windowed` for beat-dependent behavior, and `inactive` only when the cue's disposition is inactive.
4. Use windows rather than exact instants for irregular biological events. A count range selects how many windows are used; it does not require an event in every window. Give event tracks a physically plausible duration range in seconds.
5. State the phase relationship between each active vitality cue and the primary action. Do not align every blink, breath transition, micro-adjustment, and secondary-motion peak with action boundaries.
6. Add secondary tracks only for visible, materially important responses. Each needs a driver, response, active window, lag, damping, and settling rule.
7. Reserve short protected windows when dominant motion would conceal a required subtle cue. State which motion continues and which motion is reduced; do not freeze the subject.
8. Add a descending priority order containing the primary action, each active cue, and each secondary track exactly once. Add coordination rules that preserve connected anatomy, then anti-synchrony rules for repeated action so bounded variation remains causal rather than random.

The schedule is a temporal orchestration contract, not per-frame animation. It describes allowed windows, dependencies, and bounded differences while leaving continuous biological motion available to the video model.

## Preflight selection check

Before building the final prompt, verify that:

- every subject has exactly one realism profile and all five baseline cues have explicit dispositions;
- an awake, visible human is not treated as a static object merely because the user omitted physiology;
- each active cue maps to `G16` and supporting Level 2 components;
- suppression and intentional stillness have scene-specific rationales;
- repeated natural human action has bounded variation in at least two dimensions;
- each subject has one motion schedule whose primary phases cover its beats in order;
- active vitality tracks agree with the realism selection and have usable timing windows, priority, and event-duration bounds where applicable;
- protected windows do not overlap, and priority order covers the primary action, active vitality, and secondary motion exactly once;
- repeated phases realize at least two selected variation dimensions and include anti-synchrony rules;
- every scheduled secondary response has a physical or anatomical driver, lag, damping, and settling;
- every restrained performance has an amplitude decision, quiet-region guards, and prohibited substitutions;
- quiet respiration cannot be read as swallowing, speech, gasping, shrugging, or whole-body vertical motion;
- plainly legible simultaneous cues remain within the motion budget;
- held expression preserves unrequested mouth, jaw, throat, brow, and cheek states;
- regional starts, peaks, reversals, and stops are not globally synchronized into pose-to-pose motion;
- all corrections, assumptions, stylizations, and unresolved material conflicts are recorded;
- the human-readable specification and generation prompt contain each required or conditional cue in concrete visible terms.

## Research basis

- Harris and Wolpert describe signal-dependent motor noise as a constraint on biological movement: https://www.nature.com/articles/29528
- Chaisanguanthum et al. show structured variability in repeated reaches: https://www.jneurosci.org/content/34/36/12071
- Doughty's review reports substantial spontaneous blink-rate variability across people and conditions: https://pmc.ncbi.nlm.nih.gov/articles/PMC6449783/
- Yamamoto et al. describe respiratory effects on standing postural sway: https://pubmed.ncbi.nlm.nih.gov/25780094/
- Caron et al. examine ventilation and postural stabilization during quiet standing: https://pubmed.ncbi.nlm.nih.gov/15265579/
