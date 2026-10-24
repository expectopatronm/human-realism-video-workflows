# Idle neck and hem action — behavior specification

Scene ID: `idle_neck_hem_ping_pong`. The sole reference is [first frame](../../Human%20Realism%20Behavior%20Planner/images/first_frame/1.png), a 2662×2662 square image. It is the opening timeline anchor at 0 seconds. There is no last-frame or intermediate anchor. The 10-second source reverses to form a 20-second ping-pong cycle; its ending is a different, settled idle state, not a match to the opening pose.

## Observed image and evidence limits

The adult woman is already standing, facing the camera with direct gaze, a reserved unsmiling expression, rose-red hair and a braid on image right. Both arms recede behind her back. She wears a pale pink short-sleeve top and light bottoms against a plain gray background. The frame crops the lower body; the hands, feet, and most of the back are not visible. Her anatomical right arm appears on image left. The braid leaves her right/back neck as the clearer, shorter route for that arm. This handedness is a reasoned choice, not an observed hand position.

Preserve facial proportions, amber patterned eyes, hairline, braid, skin and body proportions, clothing, original hem coverage, and the visible amount of skin. Hidden support is treated conservatively as planted standing support. No new back, leg, foot, or body region should be revealed.

## Action timeline

| Source time | Primary phase |
| --- | --- |
| 0–0.8 s | Short living hold in the supplied standing pose. |
| 0.8–2.4 s | Right arm emerges slowly from behind her back along the near right side toward the right/back neck. |
| 2.4–3.7 s | Fingertips give one quiet small-area neck massage. Head yields only minimally to actual contact. |
| 3.7–4.8 s | The same hand releases and descends continuously toward the lower hem. |
| 4.8–5.6 s | One brief fingertip adjustment of the hem, with no lift or coverage change. |
| 5.6–7.6 s | The same hand returns behind her back on an anatomically continuous path. |
| 7.6–10 s | A stable turnaround hold with slightly different quiet weight distribution and all driven secondary movement settled. |

The action is one connected hand/arm/shoulder sequence, not a set of full-body poses. The voluntary motion is slow and restrained. Balance correction, blinks, fabric and hair response happen at ordinary speed and low amplitude. The hand remains the only dominant action.

## Held behavior and physics

Gaze stays directly at the camera. The reference expression and mouth shape remain; sparse ordinary blinks may occur. Brows, cheeks, lip corners, jaw, throat, and speech are held. No smile, staged head tilt, swallowing, or new emotional cue occurs. Quiet breathing may appear at nearly imperceptible lower-rib/upper-abdomen amplitude. It produces no throat bob, mouth change, shoulder shrug, head recoil, or whole-body vertical pulse.

The standing height, opening lean, frontal orientation, subject scale, visible boundaries and gray background registration remain stable. The camera is stationary. There is no stand-up, sit-down, canonical straightening, approach, retreat, or additional revealed body. Only a tiny, physically connected redistribution of weight is allowed at the endpoint. Hair responds only to nearby contact; the top responds only to the single fingertip adjustment, with fast settling and unchanged coverage.

The interaction sequence is approach → small neck contact → release → hem contact → release → behind-back return. The hand's hidden portions are inferred only to preserve anatomical continuity. The stable endpoint and absence of a last-frame image limit exact endpoint control.

## Image and output decision

The user chose to upload the original square image into Flow while selecting 9:16 output. This does not determine Flow's exact portrait crop. The plan therefore treats the in-video composition lock as a requested invariant with an acknowledged source-aspect limitation. It does not claim guaranteed pixel-matched framing. The chosen output uses a 10-second source clip, then deterministic forward–reverse playback to 20 seconds.

Selected anatomy includes hair `01.03`, eyelids `03.02`, eyeballs `03.05`, iris `03.06`, lip corners `07.03`, oral opening `07.05`, neck `08.02` and `08.04`, shoulders `09.03`, ribcage `10.03`, right arm `12.01` and `12.04`, forearm `13.01`, hand `14.01`, fingertips `14.10`, upper abdomen `15.01`, waist `15.05`, and pelvis `16.01`. Global rules and component-level preservation, motion, physics, and traceability are in `scene_spec.json`. There are no unresolved intent conflicts.
