# Prompt compilation notes

Use these notes when compiling a structured human realism plan for Gemini Omni. They are a field map and decision guide, not text to paste verbatim into the output.

| Scene specification source | Include in the Omni prompt when relevant |
| --- | --- |
| `references`, `subjects` | Name the attached image roles and preserve subject identity, stable appearance, wardrobe, and intentional changes. |
| `intent.initial_state`, `beats`, `final_state` | Describe the visible beginning, actions in order, causally linked reactions, and the ending. |
| `intent.camera`, `duration` | Use requested framing, camera movement, shot continuity, and duration. If null, do not invent an exact lens, move, or timecode. |
| `intent.setting` | Preserve the stated location and lighting; where unspecified, keep reference-established surroundings without inventing a new place. |
| High-priority `global_rules` and `components` | Express the few physical and anatomical constraints that matter to this action, such as connected gaze, weight support, hair response, or hand–object contact. |
| `appearance_changes`, `allowed_changes` | State intentional changes while retaining the remaining identity constraints. |
| `negative_constraints` | Select specific likely failures and phrase them briefly, preferably alongside the desired positive behavior. |
| `assumptions`, `unresolved_conflicts` | Include only assumptions needed for rendering; block on material unresolved conflicts. Never present inferred details as reference facts. |

## Reference handling

- With one attached image, plain language such as “Use the attached image as the identity and appearance reference” is usually sufficient.
- With multiple images, state each image's role and keep one person's views connected. For example, “Use the first attached image for facial identity and the second for the same person's side proportions.” This is a mapping from the actual attachment order, not a guess from `R1`/`R2` labels.
- If the user specifies a Gemini API workflow and the upload order is confirmed, supported tags such as `<IMAGE_REF_0>` may be useful. Check current official documentation before choosing tag syntax. Do not insert a placeholder tag without a corresponding media input.
- When media are not available at compilation time, produce the prompt and list what must be attached. Do not claim the model has seen them.

## Prompt shape

Prefer one coherent paragraph or a few short natural-language sentences. A useful order is: reference role and identity; shot and visual setting; initial pose; ordered action and ending; causally important secondary motion/contact; concise preservation and exclusion constraints. Include audio, dialogue, text, exact timestamps, resolution, or aspect ratio only when the specification or an explicit user instruction calls for them. Keep creative wording natural rather than copying the local guide's example scene or dumping the full anatomy inventory.

If the planned action must remain one continuous shot, say so explicitly. If the specification calls for cuts, preserve their order. Gemini Omni can interpret high-level complex actions; describe the cause and result clearly without assigning every frame a technical command.

## Example transformation

For a valid specification whose attached `R1` shows a woman with shoulder-length wavy hair, and whose beats request a slow head turn followed by a gentle smile in a light breeze, a suitable prompt is:

> Use the attached image as the woman's identity and appearance reference. In one continuous, naturally lit portrait shot, begin with her facing the camera. She slowly turns her head to her left; her eyes follow coherently and her shoulder-length wavy hair responds subtly to the turn and a light breeze, then settles. As the turn finishes, she forms a gentle smile and holds it. Preserve her facial structure, hairstyle, and visible clothing. Keep the neck movement comfortable and the smile restrained; avoid identity drift, disconnected gaze, and hair motion without a cause.

This example illustrates phrasing only. A real prompt must follow its own JSON and confirmed media mapping, including any different camera, timing, action, or preservation constraints.
