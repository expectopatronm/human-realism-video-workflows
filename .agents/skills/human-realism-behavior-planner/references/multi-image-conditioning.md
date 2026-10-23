# Model-neutral image conditioning

Resolve every supplied image into a timeline role or a semantic role before planning behavior. Folder placement is authoritative in the repository workflow; filenames are not. A timeline frame constrains *when the video must look like an image*. A semantic reference constrains *what a subject, object, environment, or style should look like* without assigning that image to a time.

## Repository inputs

Read `generation_artefacts/input/content.txt` as scene intent and scan `generation_artefacts/input/images/`:

| Folder | Planner meaning |
| --- | --- |
| `first_frame/` | Zero or one exact opening anchor at normalized time 0.0. |
| `last_frame/` | Zero or one exact closing anchor at normalized time 1.0. |
| `intermediate_frames/` | Zero or more interior anchors with explicit times. |
| `reference_frames/` | Unpinned semantic evidence for identity, face, body, clothing, accessories, objects, environment, lighting, style, pose, or composition. |

Use `scripts/resolve_image_inputs.py` to inventory the folders before visual analysis. Intermediate timing belongs in `intermediate_frames/timings.json`. A value can be seconds or an object with `value` and `unit` set to `seconds` or `normalized`:

```json
{
  "turn.png": {"value": 0.35, "unit": "normalized"},
  "hold.png": {"value": 6.5, "unit": "seconds"}
}
```

Seconds require a confirmed duration. Times must be unique and strictly inside the clip. Never infer timing from filename order or distribute frames evenly unless the user explicitly asks for even spacing.

Optional `reference_frames/roles.json` may state the user's intended semantic roles and target hints:

```json
{
  "face.png": {
    "roles": ["face_identity"],
    "targets": ["woman"],
    "notes": "Use for facial identity, not pose or framing."
  }
}
```

The planner must still inspect every image. A sidecar records intent; it does not turn an invisible detail into observed evidence.

## The fifteen supported combinations

The four input classes produce fifteen non-empty combinations. All are valid planner inputs even when a particular downstream model cannot consume them natively.

| First | Last | Intermediate | References | Configuration | Planning consequence |
| --- | --- | --- | --- | --- | --- |
| yes | no | no | no | `first_frame_only` | Continue plausibly from a fixed opening. |
| no | yes | no | no | `last_frame_only` | Construct a plausible lead-in to a fixed ending. |
| no | no | yes | no | `intermediate_frames_only` | Plan around timed interior states with generated ends. |
| no | no | no | yes | `reference_frames_only` | Generate the whole timeline while preserving assigned semantics. |
| yes | yes | no | no | `first_and_last` | Interpolate a coherent action between fixed endpoints. |
| yes | no | yes | no | `first_and_intermediate` | Preserve the opening and pass through timed interior states. |
| yes | no | no | yes | `first_and_references` | Continue from the opening while applying unpinned identity or scene evidence. |
| no | yes | yes | no | `last_and_intermediate` | Connect timed interior states into the fixed ending. |
| no | yes | no | yes | `last_and_references` | Lead into the ending while applying semantic evidence. |
| no | no | yes | yes | `intermediate_and_references` | Generate both ends around timed anchors and preserve assigned semantics. |
| yes | yes | yes | no | `first_last_and_intermediate` | Interpolate each anchor-to-anchor segment. |
| yes | yes | no | yes | `first_last_and_references` | Interpolate endpoints while preserving independent semantic evidence. |
| yes | no | yes | yes | `first_intermediate_and_references` | Continue through interior anchors with semantic preservation. |
| no | yes | yes | yes | `last_intermediate_and_references` | Approach the endpoint through interior anchors with semantic preservation. |
| yes | yes | yes | yes | `first_last_intermediate_and_references` | Fully anchored timeline plus independent semantic evidence. |

Do not collapse these configurations into “multiple references.” Their authority differs.

## Authority and segmentation

Treat an endpoint or intermediate frame as an exact requested visual state, while recognizing that a downstream model may only approximate it. Treat semantic references as evidence bounded to their declared roles. A reference assigned to face identity does not also define body shape, clothing, pose, camera, or chronology unless the user declares those roles or the image is independently assigned as a timeline anchor.

Sort anchors by normalized time and split the clip into consecutive interpolation segments. Each segment needs a transition intent, its covered beats, continuity constraints, and a feasibility disposition. Reconcile all anchor boundaries with the behavior plan:

- contact, support, grip, handedness, and object state must have plausible transitions;
- identity, anatomy, wardrobe, accessories, scene geometry, lighting, and camera continuity must not jump silently;
- large pose or viewpoint changes need enough duration and intermediate mechanics;
- facial identity must remain expressive rather than frozen;
- an intermediate frame is a state to pass through, not evidence that the subject should stop there;
- the first and last anchors govern the exact endpoint states even when prose describes a nearby pose;
- a semantic pose reference guides a movement or pose without becoming a hidden keyframe.

The same image may intentionally serve as both a timeline anchor and semantic evidence, but record that dual role explicitly. Matching first and last images may mean a seamless loop or a ping-pong loop; ask which one the user intends because their velocity and endpoint requirements differ.

## Clarification rules

Ask a targeted question before final output when any of these choices are unresolved:

- an intermediate frame lacks a timestamp or the duration needed to interpret seconds;
- the desired chronological order conflicts with supplied times;
- it is unclear whether an image is a fixed frame or an unpinned reference;
- a semantic image could control more than one person, object, wardrobe, or scene element;
- references disagree about identity, anatomy, clothing, accessories, setting, lighting, camera, or age/state;
- adjacent anchors require an unexplained teleport, contact change, object state change, camera cut, or anatomical discontinuity;
- matching endpoints could mean a seamless loop, a ping-pong loop, or simply the same composition;
- a requested appearance transformation has no stated point or interval;
- an anchor exposes an identity-critical view unsupported by the available evidence.

Do not ask the user to describe details that can be observed directly. Group related questions. If the user explicitly delegates a reversible choice, record the conservative resolution in `intent_resolutions`.

## Research basis

- [Veo 3.1 documentation](https://ai.google.dev/gemini-api/docs/veo) distinguishes an initial image, a paired final frame, and unpinned asset references.
- [Gemini Omni video documentation](https://ai.google.dev/gemini-api/docs/omni) explicitly separates source frames from image and video references and supports combined roles.
- [Grok Imagine Video 1.5 documentation](https://docs.x.ai/developers/model-capabilities/video/generation) supports first, last, timed interior keyframes, and semantic references in combinations. This validates the four-role taxonomy without making its limits part of the model-neutral schema.
- [Versatile Transition Generation (ICCV 2025)](https://openaccess.thecvf.com/content/ICCV2025/html/Yang_Versatile_Transition_Generation_with_Image-to-Video_Diffusion_ICCV_2025_paper.html) shows that coherent first-to-last transitions require bidirectional treatment and identity-aware alignment rather than ordinary one-sided continuation.
- [Video Motion Graphs (ICCV 2025)](https://openaccess.thecvf.com/content/ICCV2025/html/Liu_Video_Motion_Graphs_ICCV_2025_paper.html) motivates explicit human-motion interpolation between discontinuous states.
- [Movie Weaver (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/html/Liang_Movie_Weaver_Tuning-Free_Multi-Concept_Video_Personalization_with_Anchored_Prompts_CVPR_2025_paper.html) and [Gloria (CVPR 2026)](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Gloria_Consistent_Character_Video_Generation_via_Content_Anchors_CVPR_2026_paper.html) motivate explicit reference-to-concept assignment and conflict handling for multiple anchors.
- [IPRO (CVPR 2026)](https://openaccess.thecvf.com/content/CVPR2026/html/Shen_Identity-Preserving_Image-to-Video_Generation_via_Reward-Guided_Optimization_CVPR_2026_paper.html) documents identity drift under large motion and expression change; its supplemental results also caution against identity preservation that freezes facial behavior.
