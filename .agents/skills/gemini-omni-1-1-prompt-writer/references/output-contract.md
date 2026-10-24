# Output contract

The writer produces `gemini_omni_1_1_prompt.txt` and `google_flow_settings.json` in the planner output directory. The package is for manual use in Google Flow and accepts prompt text plus images only; video input is prohibited.

The file contains only the ready-to-paste Gemini Omni 1.1 prompt. It must:

- identify each supplied image by its declared timeline or semantic role;
- use the user-selected Flow duration for all exact timing;
- preserve the canonical scene, subject, identity, continuity, and evidence boundaries from `scene_spec.json`;
- express the shot, camera, framing, style, lighting, location, chronological action, visible human realism, secondary physical responses, final state, and critical constraints relevant to the scene;
- use seconds-based timing only when duration or a resolved schedule supports it;
- preserve intermediate and endpoint anchor adherence without treating semantic references as frames;
- preserve loop semantics, including a settled turnaround for ping-pong playback;
- preserve every held human-behavior channel, observed limb/contact state, facial lock, quiet-region guard, suppressed physiology cue, and prohibited human-motion substitution;
- apply the planner's semantic-activation control so social, affective, cinematic, or spatial labels cannot silently add expression, gesture, posture, or camera behavior;
- apply facial-state control independently from head pose, gaze, and blinking;
- preserve behavioral intent, support topology, pelvis height, starting-posture invariants, and every prohibited pose normalization;
- enforce strict composition with one positive first-frame screen-space lock covering subject scale, crop boundaries, registered background, and visible landmarks;
- preserve every action-critical motion envelope so the complete hand, limb, hair, prop, or garment trajectory remains inside the intended frame with its planned edge clearance; intentional crop remains intentional, but accidental boundary clipping is prohibited;
- require an aspect-matched wider prepared anchor or constrained action when the motion envelope cannot fit; never use generated zooming or reframing as a clearance mechanism;
- keep off-frame anatomy and causal mechanics out of the prompt unless the shot intentionally reveals them;
- follow the planner's prompt strategy: expose direct evidence only when low risk; otherwise use a holistic outcome, reclassification, clarification, or bounded ambiguity without copying the diagnostic causal chain;
- never claim an action more strongly than its observability and fallback permit;
- preserve behavioral reading and posture invariants ahead of action legibility; do not turn restrained behavior into regional choreography or a sequence of distinct poses;
- include explicit temporal layers, mention compact layers once, and leave implicit or omitted subthreshold layers unnamed;
- preserve exact major dwell intervals rather than merely requiring arrival by their endpoints;
- apply slow timing only to the layers marked slow while retaining normal-speed biological, compensatory, and material response;
- allow bounded subthreshold head, eye, and facial variation without changing gaze target or expression category;
- keep quiet respiration distinct from swallowing, drinking, speech, gasping, shrugging, head recoil, and mouth-shape change;
- follow the planner's motion budget instead of making every micro-cue plainly visible;
- contain no planner schema terms, internal rule IDs, Action Unit codes, unsupported additions, evaluation instructions, or claim of generation.
- avoid repeated negated motion vocabulary, long prohibition lists, and region-by-region motion chains that can become unintended generation targets.

`scene_spec.json` wins if the readable specification or model-neutral prompt disagrees with it. A disagreement that changes the result is blocking and must be resolved rather than silently compiled.

`google_flow_settings.json` must contain:

- `execution_surface`: `google_flow_web`;
- `model`: `gemini_omni_1_1`;
- `duration_seconds`: the value the user will select manually;
- `aspect_ratio`: `9:16` or `16:9`;
- `prompt_file`: `gemini_omni_1_1_prompt.txt`;
- `image_only`: `true` and `video_inputs`: an empty array;
- `image_inputs`: every supplied generation image with path, declared Flow role, width, height, and `aspect_match`;
- `postprocess`: deterministic delivery transforms, or an empty array.

Every strict first- or last-frame anchor must match the selected aspect ratio before the package is valid. The manifest records settings; it does not claim that the prompt enforces them.
