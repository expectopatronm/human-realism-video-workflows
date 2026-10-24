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
- keep quiet respiration distinct from swallowing, drinking, speech, gasping, shrugging, head recoil, and mouth-shape change;
- follow the planner's motion budget instead of making every micro-cue plainly visible;
- contain no planner schema terms, internal rule IDs, Action Unit codes, unsupported additions, evaluation instructions, or claim of generation.

`scene_spec.json` wins if the readable specification or model-neutral prompt disagrees with it. A disagreement that changes the result is blocking and must be resolved rather than silently compiled.
