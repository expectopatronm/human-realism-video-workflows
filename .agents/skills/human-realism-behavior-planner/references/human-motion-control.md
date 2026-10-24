# Human motion control and quiet-performance planning

Use this reference when a scene depends on restrained, idle, held, looped, or micro-realistic human behavior. It defines how to prevent robotic pose changes and exaggerated biological cues. It does not govern camera language, shot composition, or model-specific generation settings.

## Clarification before planning

Do not equate a syntactically complete request with a sufficiently controlled performance. Ask one grouped set of short questions when any missing choice below would materially change visible human behavior:

- **Primary-motion magnitude:** barely perceptible, restrained but readable, or clearly visible.
- **Behavioral reading:** the ordinary activity or state the body should communicate, and readings it must not drift into (for example waiting rather than performing).
- **Support topology:** standing, seated, leaning, or otherwise supported; which contacts bear weight; whether pelvis height and lower-limb flexion are fixed.
- **Facial freedom:** blink-only face lock, preserved expression with minute tonus, or limited micro-expression.
- **Respiration readability:** nearly imperceptible, subtly readable, or clearly readable; identify whether lower ribs/upper abdomen, upper chest, or both may show it.
- **Held-body regions:** whether observed hands, arms, shoulders, jaw, lips, throat, or support contacts must remain fixed.
- **Hidden support:** whether to infer conservative planted support or constrain/reframe the action until support evidence is supplied.
- **Loop interpretation:** whether the stated duration is the generated source or the complete loop, and whether the endpoint is a seamless match or a ping-pong turnaround.

Do not ask again when the user already answered a choice. Age, consent, safety, or identity questions do not substitute for performance clarification.

Treat these configurations as higher uncertainty rather than ordinary omissions:

- one timeline anchor controlling a long or multi-phase performance;
- important movement driven by occluded feet, pelvis, hands, or contact;
- held expression combined with visible breathing, parted lips, or exposed throat;
- several requested micro-cues competing with a subtle primary action;
- strict looping without a supplied endpoint;
- words such as `subtle`, `slow`, `natural`, `idle`, or `sensual` without an amplitude or facial-freedom decision.

When the user declines to decide, use the smallest physically plausible amplitude, lock unrequested facial and gestural degrees of freedom, and record that conservative choice. Do not silently choose a more expressive performance.

## Motion economy

Human realism is not the maximum number of moving regions. Build an explicit motion budget:

1. Preserve the primary action as the only dominant track.
2. Allow at most one or two additional cues to be plainly legible at the same moment unless the action physiologically requires more.
3. Allow several causally justified cues concurrently only when each remains below deliberate-performance amplitude. Subthreshold concurrency is natural; synchronized salience is not.
4. Keep all observed but unrequested regions in `held` or visible-static states and state what prevents drift.
5. Never animate a region merely because it is visible.

For each active or held channel, identify:

- initiator and physical driver;
- allowed range and apparent amplitude class;
- regions that follow with overlap or lag;
- regions that remain quiet;
- arrival behavior and residual settling;
- prohibited substitutions, such as a camera change standing in for body movement or a swallow standing in for respiration.

## Non-robotic transitions

Avoid treating beats as a sequence of full-body poses. Natural movement should have a continuous center-of-mass path and overlapping regional timing:

- support pressure changes first;
- pelvis and spine respond continuously;
- shoulders, neck, and head follow with small, nonuniform delays;
- passive elements lag and settle according to their material;
- not every region begins, peaks, reverses, or stops together;
- a dwell preserves quiet vitality and residual balance rather than becoming a frozen keyframe.

Do not insert independent sways, nods, shrugs, mouth actions, or gaze shifts to make a held pose look alive. For repeated movements, vary narrowly without changing the action family. Prefer differences in acceleration, dwell, or inter-region phase over visibly different endpoints when continuity is important.

## Support topology and posture preservation

Classify the starting support state before prescribing motion. Record weight-bearing contacts, external supports, initial load distribution, lower-limb state, and whether pelvis height is fixed or allowed to change. A first frame is already a physical state, not a staging pose the model may normalize before beginning the action.

When posture authority is strict, list both invariants and prohibited normalizations. In particular, prevent an in-place action from becoming a stand-up, sit-down, crouch release, knee extension, pelvis lift, canonical straightening, or re-centering unless requested. If occlusion makes the support state materially ambiguous, ask the user or constrain the action to what is visible.

## Independent temporal layers

Do not use one speed adjective for the whole body. Assign each layer its own clock:

- voluntary action may be slow and deliberate;
- balance compensation occurs in real time but remains small;
- respiration follows a biological cadence;
- blinks retain normal event duration;
- hair, fabric, and soft tissue respond at their material speed, then damp and settle;
- head, eye, and facial tonus may contain bounded aperiodic micro-variation without changing gaze or expression.

`Slow` describes the requested voluntary travel unless the user explicitly requests slow-motion footage. It must not stretch blink closure, passive bounce, fabric settling, or other physical responses. Conversely, preserving normal response speed does not authorize larger amplitude or extra cycles.

## Behavioral intent and bounded variation

Separate behavioral intent from facial expression. A sensual, stern, neutral, or cheerful face does not by itself make the body flirt, dance, pose, or perform. State the intended everyday reading and prohibited readings, then choose effort, amplitude, and rhythm that support it.

Natural idle behavior is bounded and aperiodic, not frozen and not random. Permit minute non-cyclic differences in acceleration, dwell, inter-region lag, fixation correction, head support, eyelid/cheek/brow tonus, and settling. Keep mouth, jaw, throat, gaze target, support state, and expression category invariant when required. A generated clip remains deterministic on replay; genuine long-run non-repetition requires multiple variants, a longer source, or a procedural playback system.

Do not assume every planned micro-cue should be named in a generation prompt. A video model may amplify any named motion into a salient action. Mark ordinary subthreshold vitality as implicit or omitted unless its absence has already been demonstrated and a compact instruction is necessary. Never solve a weak result by accumulating a catalog of additional micro-actions.

Keep causal planning details behind a visibility boundary. Off-frame feet, knees, hips, contacts, and support mechanics can constrain the visible result without being named to a model when the shot must not reveal them. Phrase the visible outcome—stable scale, crop, vertical position, and restrained internal deformation—instead.

## Quiet respiration

Quiet respiration must remain distinct from swallowing, drinking, gasping, speaking, sighing, or exertion.

Unless the user requests otherwise:

- initiate low in the ribcage and upper abdomen;
- use very low amplitude and a soft, non-metronomic reversal;
- let upper chest, fitted clothing, and supported soft tissue respond secondarily;
- keep shoulder elevation at zero or nearly zero;
- keep the jaw, lip aperture, tongue, throat, chin, head height, and gaze target stable;
- do not add a throat bob, chin lift, mouth opening, head recoil, or whole-body vertical pulse;
- do not align the breath reversal with every weight-shift arrival or blink.

If the lips are already parted, preserve the observed aperture rather than using it as permission for respiratory mouth motion. A visible swallow is a separate extended-physiology action and must be explicitly requested or causally justified.

## Held face and gaze

A held expression may contain living tonus without changing the expression category. Define the face as separate controlled regions:

- gaze target and binocular coordination;
- eyelid/blink behavior;
- brow and cheek tonus;
- lip corners and lip aperture;
- jaw and throat;
- head pose and neck support.

When the user requests a fixed expression, default unrequested mouth, jaw, throat, brow, and cheek actions to held. Blinking does not authorize gaze drift, mouth motion, a head reset, or a simultaneous full-face change. Head tilt does not authorize loss of facial orientation or large neck translation.

## Weight transfer and support

For an in-place weight transfer:

- both feet remain planted unless a step is requested;
- pressure redistribution precedes visible pelvis motion;
- the center of mass travels continuously within the support base;
- pelvis, spine, and shoulders counterbalance rather than translating as one rigid cutout;
- head response is smaller than torso response unless explicitly requested;
- hidden support mechanics must not reveal invented feet or change the crop;
- observed arm/hand placement remains held unless needed for balance and authorized by the user;
- deceleration may drive one damped secondary response, never repeated decorative bouncing.
- preserve starting pelvis height and lower-limb flexion unless vertical travel is explicitly requested;
- use slow voluntary transfer with normal-speed, low-amplitude physical response rather than globally slowed motion;
- vary tiny head and facial support corrections independently within bounds instead of tying a visible head tilt to every arrival.

If the support base is invisible and the requested magnitude cannot be inferred conservatively, ask for the magnitude or constrain the movement rather than inventing a large shift.

## Preflight

Before finalizing a quiet human performance, confirm that:

- every unanswered high-impact control choice was asked or conservatively resolved with the user's knowledge;
- the primary action has an amplitude class and continuous causal path;
- held regions and prohibited substitutions are explicit;
- respiration cannot be mistaken for swallowing, speech, gasping, or a shrug;
- facial freedom matches the requested expression;
- plainly visible concurrent cues remain within the motion budget;
- support topology, pelvis-height policy, and posture-normalization prohibitions are explicit;
- behavioral intent cannot be misread as a more performative action;
- voluntary, biological, compensatory, and passive layers retain their own time scales;
- bounded micro-variation preserves gaze and expression without freezing the face;
- starts, peaks, reversals, and stops are not globally synchronized;
- a first-frame-only, long-duration, or hidden-support plan is identified as higher uncertainty;
- the generation brief preserves every human-behavior hard invariant.
