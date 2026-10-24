# Output contract

The writer produces one UTF-8 text file named `gemini_omni_1_1_prompt.txt` in the planner output directory.

The file contains only the ready-to-paste Gemini Omni 1.1 prompt. It must:

- identify each supplied image by its declared timeline or semantic role;
- state the user-selected Gemini aspect ratio (`9:16` or `16:9`) without inferring it from the source image;
- preserve the canonical scene, subject, identity, continuity, and evidence boundaries from `scene_spec.json`;
- express the shot, camera, framing, style, lighting, location, chronological action, visible human realism, secondary physical responses, final state, and critical constraints relevant to the scene;
- use seconds-based timing only when duration or a resolved schedule supports it;
- preserve intermediate and endpoint anchor adherence without treating semantic references as frames;
- preserve loop semantics, including a settled turnaround for ping-pong playback;
- preserve every held human-behavior channel, observed limb/contact state, facial lock, quiet-region guard, suppressed physiology cue, and prohibited human-motion substitution;
- preserve behavioral intent, support topology, pelvis height, starting-posture invariants, and every prohibited pose normalization;
- enforce strict composition with one positive first-frame screen-space lock covering subject scale, crop boundaries, registered background, and visible landmarks;
- keep off-frame anatomy and causal mechanics out of the prompt unless the shot intentionally reveals them;
- express the primary action through its visible distinguishing cues, causal order, and endpoint evidence rather than its label alone;
- never claim an action more strongly than its observability and fallback permit;
- include explicit temporal layers, mention compact layers once, and leave implicit or omitted subthreshold layers unnamed;
- preserve exact major dwell intervals rather than merely requiring arrival by their endpoints;
- apply slow timing only to the layers marked slow while retaining normal-speed biological, compensatory, and material response;
- allow bounded subthreshold head, eye, and facial variation without changing gaze target or expression category;
- keep quiet respiration distinct from swallowing, drinking, speech, gasping, shrugging, head recoil, and mouth-shape change;
- follow the planner's motion budget instead of making every micro-cue plainly visible;
- contain no planner schema terms, internal rule IDs, Action Unit codes, unsupported additions, evaluation instructions, or claim of generation.
- avoid repeated negated motion vocabulary and long prohibition lists that can become unintended generation targets.

`scene_spec.json` wins if the readable specification or model-neutral prompt disagrees with it. A disagreement that changes the result is blocking and must be resolved rather than silently compiled.
