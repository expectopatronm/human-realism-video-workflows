# Gemini Omni 1.1 image-to-video prompting guide

This repository targets manual generation in Google Flow: the user uploads images, pastes one prompt, and selects duration and aspect ratio in the interface. Do not require a video input. A video may be analyzed outside Flow, but only its written motion evidence or user-approved still frames may enter this workflow.

## Control layers

Do not collapse every requirement into prose. Use the strongest available control layer:

- **Google Flow setting:** duration and aspect ratio.
- **Image slot:** first, intermediate, last, identity, appearance, or other semantic reference.
- **Prompt:** visible action, timing, expression, gaze, camera intent, and preservation language.
- **Postprocess:** deterministic trimming, retiming, or playback behavior requested for the delivered asset.

The Flow selections are authoritative. Confirm them before compiling exact seconds. Never infer aspect ratio from an uploaded image or claim that prompt text changes an incorrectly selected setting.

## Input-image preparation

For strict composition, prepare first and last frames at the exact selected output aspect ratio before upload. A square image with extra border is still square and leaves portrait or landscape recomposition unresolved. Extend the canvas deterministically without rescaling or repositioning the subject pixels, then use that aspect-matched image in the corresponding Flow frame slot.

Treat every image according to its declared role. Timeline anchors define exact states at particular times. Semantic references guide only their assigned identity, appearance, object, or environment property and must not become chronological frames.

## Prompt construction

Use one continuous shot when the scene must not cut. Begin with the duration, continuous-shot intent, and a concise positive composition lock. Describe the requested action chronologically and use exact seconds only after the Flow duration is confirmed.

Keep the prompt proportional to the action. More anatomical or diagnostic detail can activate more motion. Prefer one holistic visible result over a chain of independently named body regions unless that articulation is itself the requested performance.

Separate these controls:

- subject motion from camera motion;
- head pose from facial expression;
- gaze from head orientation;
- eyelid events from brows, cheeks, lips, and jaw;
- slow voluntary travel from normal-speed blinks and material response;
- behavioral meaning from the exact visible channels that communicate it.

## Semantic activation audit

Social, affective, cinematic, and spatial language can imply extra behavior. Terms such as greeting, acknowledgment, curiosity, confidence, sensuality, reveal, settle, or center are not automatically safe. Evaluate each term in context, identify likely bundled behaviors, and replace it with the smallest visible description the scene actually needs.

For example, a social response may be expressed only as a small head inclination and gaze change while the reference expression remains unchanged. Do not use emotional prose when no emotional transition is requested. Disambiguate whether `center` means screen position, body orientation, gaze direction, or balance.

## Facial-state preservation

“Preserve the expression” is often too broad. When the expression is strict, state the retained expression category and the few regions that matter most. Permit only the requested facial changes. A head tilt, gaze engagement, or blink must not authorize a smile, brow performance, cheek lift, jaw motion, or mouth-shape change.

Use one concise shot-critical prohibition when a likely substitution cannot be expressed positively. Gemini Omni has no separate negative-prompt field in the documented API; ordinary prompt text carries negative instructions. Avoid long catalogs of negatives.

## Camera and composition

Use `static`, `fixed`, or `tripod-locked` for a stationary shot, but do not rely on that phrase alone. Bind an aspect-matched first frame and preserve two or three visible landmarks at the same apparent scale and screen position. Keep regions that begin outside frame outside frame unless the action intentionally reveals them.

If exact endpoint composition, pose, or expression is critical, prefer a last-frame image. When no endpoint anchor exists, record reduced control confidence rather than pretending prose guarantees the endpoint.

Composition checks must cover motion, not only the opening still. Estimate the complete screen-space envelope of every action-critical hand, wrist, forearm, elbow, foot, hair section, prop, and garment contact. Keep required elements fully inside the frame with clear edge margin for all active frames. Preserve deliberately cropped anatomy, but do not allow a moving element to be accidentally chopped by a frame boundary. If the planned path is too tight, constrain it or prepare a wider aspect-matched first frame before generation. Never ask Omni to zoom out, pan, change depth, or reframe in order to recover missing clearance.

## Timing and Flow handoff

The prompt writer must produce a separate `google_flow_settings.json` containing the duration and aspect ratio the user must select, plus every image-to-slot mapping. This prevents a correct prompt from being paired with incorrect interface settings.

Use the selected duration to resolve the planner schedule. The prompt may include natural-language timestamps such as `[0–1.5s]`, but the settings manifest remains the source of truth for total duration.

## Current official capability notes

Google’s current Gemini Omni documentation supports image-to-video generation, first-and-last-frame interpolation, explicit image roles, 9:16 and 16:9 aspect ratios, and an `image_to_video` task in API usage. The official documentation also says that negative prompts are not a separate supported control and that simple, precise prompts reduce unintended changes. This repository uses the equivalent manual image slots and settings in Google Flow rather than constructing an API request.

Sources, checked 2026-10-24:

- https://ai.google.dev/gemini-api/docs/omni
- https://ai.google.dev/gemini-api/docs/veo
