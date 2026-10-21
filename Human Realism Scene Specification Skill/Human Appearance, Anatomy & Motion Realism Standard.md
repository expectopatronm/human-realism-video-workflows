# Human Appearance, Anatomy & Motion Realism Standard

**Version:** 1.0  
**Subject:** Adult Female Human  
**Application:** Photorealistic image-to-video and multi-image-to-video generation  
**Coverage:** Levels 1 and 2  
**Status:** Proposed working specification

---

# 0. Purpose and Scope

## 0.1 Purpose

This guideline defines the requirements for preserving and realistically animating a human subject when converting one or more reference images into a video sequence.

The generated person must remain anatomically believable, visually consistent, physically plausible, and recognizable throughout the sequence.

The standard applies to:

- Stationary subjects and subtle idle motion.
- Facial close-ups and portrait animation.
- Full-body and partial-body movement.
- Walking, running, turning, sitting, and other actions.
- Human interactions with objects, clothing, and surroundings.
- Changing camera angles, perspective, and lighting.
- Single-person and multi-person scenes.

## 0.2 Core principles

1. Preserve the reference subject unless an intentional change is specified.
2. Maintain correct anatomy and physical relationships between body parts.
3. Produce natural movement appropriate to the intended action.
4. Preserve appearance, identity, and continuity across all frames.
5. Respect gravity, momentum, contact, and anatomical movement limitations.
6. Maintain realistic materials, textures, lighting, and shadows.
7. Avoid spontaneous or unexplained changes to visible anatomy.
8. Keep coordinated bodily actions synchronized.
9. Preserve intentional stillness; movement is not mandatory.
10. Do not invent unsupported details as if they were established reference facts.

## 0.3 Terminology

**MUST:** Mandatory requirement wherever applicable.

**SHOULD:** Recommended requirement, subject to creative and contextual considerations.

**MAY:** Optional feature that can be included when appropriate.

**N/A:** Not applicable because a region or behavior is absent, hidden, or outside the intended action.

**Primary motion:** Deliberate movement of the body, such as rotating the head or lifting an arm.

**Secondary motion:** Movement resulting from another movement, such as hair continuing to move after the head stops.

**Deformation:** Changes in shape caused by movement, expression, forces, or contact.

**Temporal consistency:** Stability of the subject's characteristics and the scene's causal progression over time.

**Reference fidelity:** Preservation of identifiable properties established by the source images.

---

# LEVEL 1 — GLOBAL HUMAN REALISM

Level 1 defines universal constraints. These apply across all anatomical regions and should not need to be repeated in every Level 2 entry.

## G01. Identity Preservation

**Objective:** Maintain the identity of the reference person throughout the video.

Requirements:

- Preserve recognizable facial features and facial structure.
- Maintain consistent apparent age and individual characteristics.
- Preserve hairline, hairstyle, and hair color unless intentionally modified.
- Maintain facial proportions and distinguishing marks.
- Preserve skin characteristics and visible identifying features.
- Maintain consistent body shape and proportions.
- Keep left-side and right-side characteristics stable.
- Preserve appearance through camera movement, facial expression, and changing illumination.
- Avoid unexplained changes to facial identity between frames.
- Preserve consistent identity when the subject becomes partially or temporarily occluded.

**Unacceptable outcomes:** Face replacement, identity drift, changing facial structure, disappearing distinguishing features, unexplained body changes.

## G02. Anatomical Integrity

**Objective:** Ensure that the human body remains structurally plausible.

Requirements:

- Maintain correct body-part counts and anatomical connections.
- Preserve the relationship between the head, neck, spine, torso, and limbs.
- Preserve plausible bone and joint structures.
- Maintain consistent limb lengths.
- Maintain plausible body proportions without imposing one idealized body type.
- Allow natural individual anatomical variation and asymmetry.
- Prevent detached, merged, duplicated, or missing body parts.
- Keep internal anatomical relationships plausible during complex poses.
- Preserve body structure when partially obscured.

**Unacceptable outcomes:** Extra fingers, duplicated limbs, disconnected shoulders, malformed joints, unstable body proportions.

## G03. Body Proportion and Volume Consistency

**Objective:** Preserve the person's size, proportions, and physical volume.

Requirements:

- Maintain consistent relative body-part dimensions.
- Preserve limb thickness and length unless perspective explains the apparent change.
- Preserve body mass distribution.
- Maintain plausible soft-tissue volume during motion.
- Allow perspective-based size variation and realistic compression.
- Prevent spontaneous enlargement, shrinking, or distortion.
- Ensure changes in posture produce plausible changes in silhouette.

## G04. Skeletal Movement and Joint Constraints

**Objective:** Ensure body movement follows plausible joint mechanics.

Requirements:

- Maintain correct parent-child relationships between connected joints.
- Respect the anatomical movement capabilities of each joint.
- Coordinate shoulder, elbow, wrist, hip, knee, ankle, and spinal movement.
- Prevent unintended hyperextension, twisting, and dislocation.
- Maintain consistent limb connections during rotations.
- Ensure connected body parts affect one another appropriately.
- Permit individual variation in flexibility and joint mobility.

## G05. Primary Motion

**Objective:** Produce intentional movement that accurately follows the desired action.

Requirements:

- Maintain coherent movement direction.
- Use plausible speed, acceleration, and deceleration.
- Avoid unintended jumps in body position or orientation.
- Coordinate all body regions participating in an action.
- Maintain meaningful movement initiation and completion.
- Preserve the intended movement sequence.
- Avoid unnecessary actions unrelated to the source or prompt.
- Allow deliberately abrupt motion when the action demands it.

## G06. Secondary Motion

**Objective:** Reproduce the natural response of deformable body structures to primary motion.

Requirements:

- Apply movement inertia to hair and other deformable structures.
- Allow soft tissues to respond to body acceleration.
- Maintain plausible delays between primary and secondary motion.
- Account for elasticity and damping.
- Allow secondary motion to settle naturally.
- Avoid continuous oscillation without an ongoing driving force.
- Ensure secondary motion remains proportional to the triggering movement.

## G07. Gravity, Mass, and Momentum

**Objective:** Ensure the person responds naturally to physical forces.

Requirements:

- Respect a consistent gravity direction.
- Represent believable body mass and weight.
- Preserve motion momentum.
- Maintain plausible acceleration under applied forces.
- Allow natural deceleration after movement.
- Coordinate physical forces with posture and support.
- Avoid unintended hovering, sliding, or weightless behavior.

## G08. Posture, Balance, and Weight Distribution

**Objective:** Maintain believable body alignment and stability.

Requirements:

- Preserve plausible spinal alignment.
- Maintain a realistic center of mass relative to support and movement.
- Coordinate pelvic alignment with torso and leg positions.
- Shift weight naturally between supporting limbs.
- Maintain stable contact during static standing.
- Allow appropriate balance corrections during movement.
- Maintain plausible seated, leaning, crouching, and reclining postures.
- Distinguish stable, unstable, and intentionally falling poses.

## G09. Surface Texture and Skin Integrity

**Objective:** Preserve natural human surface characteristics.

Requirements:

- Maintain coherent skin tone and pigmentation.
- Preserve plausible pores and fine surface detail at appropriate resolution.
- Represent natural folds, creases, and wrinkles where visible.
- Maintain consistent freckles, scars, moles, and other reference features.
- Preserve texture placement during movement.
- Avoid surface flickering, crawling textures, or artificial smoothing.
- Represent realistic differences in skin appearance across anatomical areas.
- Respect individual variation in skin texture, age, and appearance.

## G10. Skin and Soft-Tissue Deformation

**Objective:** Produce plausible tissue behavior during movement and contact.

Requirements:

- Allow skin stretching and compression.
- Preserve continuity between neighboring body regions.
- Maintain plausible muscle-related surface movement.
- Allow soft tissue to deform under gravity and contact.
- Preserve anatomical volume within reasonable physical limits.
- Produce natural folds during bending or compression.
- Prevent clipping, tearing, stretching artifacts, and abrupt geometry changes.
- Distinguish rigid anatomical structures from flexible tissue.

## G11. Lighting and Shadow Consistency

**Objective:** Ensure the human subject responds coherently to scene illumination.

Requirements:

- Maintain consistent light direction within the scene.
- Preserve plausible brightness and color temperature relationships.
- Produce anatomical self-shadowing.
- Maintain natural contact shadows.
- Update shadows coherently as the person moves.
- Preserve dimensional facial and body contours.
- Allow lighting changes when justified by camera movement or environmental changes.
- Avoid unexplained illumination flicker.

## G12. Material and Reflectance Behavior

**Objective:** Ensure body surfaces respond plausibly to light.

Requirements:

- Distinguish the optical characteristics of skin, hair, nails, teeth, and eyes.
- Maintain plausible surface roughness and gloss.
- Represent skin's soft light-scattering appearance.
- Preserve appropriate eye reflections and moisture.
- Represent plausible hair highlights and directional reflection.
- Preserve natural fingernail and toenail reflectance.
- Avoid plastic-like, metallic, or excessively smooth skin unless intentionally styled.
- Maintain consistent material behavior across frames.

## G13. Color and Pigmentation Consistency

**Objective:** Preserve intrinsic colors independently of environmental illumination.

Requirements:

- Maintain reference skin, hair, eye, lip, and nail colors.
- Preserve natural color variation.
- Allow apparent color changes caused by illumination and camera exposure.
- Prevent unexplained pigmentation changes.
- Maintain consistent makeup color and distribution when present.
- Avoid unintended hue flickering or color patches.

## G14. Facial Expression Integrity

**Objective:** Produce recognizable expressions through anatomically coordinated facial movements.

Requirements:

- Coordinate eyebrow, eyelid, eye, cheek, nose, lip, and jaw movements.
- Support neutral, subtle, and expressive facial states.
- Allow natural asymmetry.
- Maintain plausible transitions between expressions.
- Prevent detached or isolated facial movements that contradict the intended expression.
- Avoid exaggerated deformation in otherwise realistic scenes.
- Preserve the reference identity during expression changes.
- Coordinate expression with gaze, head posture, and intended behavior.

## G15. Eye and Gaze Coordination

**Objective:** Ensure the eyes behave as a coordinated visual system.

Requirements:

- Maintain plausible gaze direction.
- Coordinate eye movement with head orientation.
- Maintain binocular coordination when both eyes are visible.
- Represent natural fixation and gaze transitions.
- Permit rapid eye shifts and subtle gaze corrections.
- Coordinate eyelids with relevant eye movement.
- Avoid unintended crossed eyes, drifting pupils, or inconsistent focus.
- Avoid mandatory constant eye movement when the person should remain focused.

## G16. Breathing and Biological Micro-Movement

**Objective:** Represent subtle biological activity where contextually appropriate.

Requirements:

- Coordinate breathing-related chest, ribcage, and abdominal movement.
- Permit subtle nostril movement when visible.
- Maintain plausible respiratory rhythm.
- Adjust breathing behavior to exertion, speech, and emotional state.
- Support natural swallowing and other contextual micro-movements.
- Avoid arbitrary blinking, twitching, or repetitive bodily movement.
- Preserve intentional stillness when demanded by the scene.
- Do not impose fixed biological timing on every individual or situation.

## G17. Speech and Oral Coordination

**Objective:** Ensure visible speaking and mouth actions remain plausible.

Requirements:

- Coordinate lips, jaw, tongue, and teeth.
- Match mouth shapes to speech when audio or dialogue is provided.
- Maintain synchronization between mouth movement and sound.
- Produce coherent opening, closing, and transitional mouth shapes.
- Maintain plausible visibility of teeth and tongue.
- Coordinate speaking with breathing and facial expression.
- Avoid unnecessary mouth movement during intended silence.
- Preserve jaw and facial geometry during speech.

## G18. Contact and Collision Behavior

**Objective:** Ensure body parts interact naturally with other surfaces.

Requirements:

- Prevent body parts from passing through one another unintentionally.
- Preserve plausible contact between hands and objects.
- Represent appropriate pressure and compression.
- Maintain realistic foot-to-ground contact.
- Preserve contact when supporting body weight.
- Coordinate movement between interacting body parts.
- Support contact with furniture, walls, clothing, and other people.
- Allow intentional separation, sliding, and release at appropriate times.

## G19. Movement Synchronization and Coordination

**Objective:** Maintain coordinated actions across the body.

Requirements:

- Synchronize connected joint movements.
- Coordinate arm swing with walking when contextually appropriate.
- Coordinate pelvis, spine, shoulders, and head movement.
- Maintain plausible sequencing of actions.
- Preserve appropriate reaction timing.
- Coordinate hands with arms during object interactions.
- Ensure facial, bodily, and environmental reactions do not contradict one another.

## G20. Temporal and Frame-to-Frame Consistency

**Objective:** Maintain continuous and believable appearance over the entire video.

Requirements:

- Preserve anatomical structure between frames.
- Prevent geometry morphing and identity drift.
- Maintain coherent surface texture placement.
- Prevent flickering of skin, eyes, hair, and clothing.
- Preserve movement trajectories.
- Maintain natural acceleration and deceleration.
- Keep anatomical details stable during occlusion and reappearance.
- Avoid unmotivated object or body-part appearance and disappearance.
- Preserve continuity across camera motion and scene transitions unless an intentional edit is specified.

## G21. Perspective, Depth, and Occlusion

**Objective:** Maintain realistic spatial relationships.

Requirements:

- Respect perspective projection and foreshortening.
- Preserve consistent anatomical volume during rotation.
- Maintain correct relative depth relationships.
- Occlude body parts appropriately.
- Reveal previously hidden surfaces plausibly.
- Preserve the correct order of overlapping objects and body regions.
- Avoid flattened or incorrectly layered anatomy.
- Maintain coherent scale relative to the environment.

## G22. Camera and Subject Relationship

**Objective:** Preserve anatomical and visual consistency across camera changes.

Requirements:

- Distinguish camera movement from subject movement.
- Maintain consistent spatial orientation.
- Preserve the subject's identity during angle changes.
- Account for camera perspective and lens effects.
- Maintain coherent visibility of body regions.
- Avoid unexplained subject scaling or repositioning.
- Preserve continuity through pans, tilts, zooms, and tracking movements.

## G23. Clothing, Footwear, and Accessories

**Objective:** Maintain realistic interaction between the human body and worn items.

Requirements:

- Preserve the fit and placement of clothing.
- Coordinate clothing movement with body motion.
- Represent appropriate fabric tension, compression, and folds.
- Prevent unintended body-clothing intersections.
- Maintain consistent coverage and layering.
- Allow footwear to follow foot movement.
- Apply plausible motion to earrings, jewelry, and accessories.
- Preserve accessory identity, color, and placement.
- Avoid unintended appearance or disappearance of garments and accessories.

## G24. Environmental Interaction

**Objective:** Ensure the person responds plausibly to the surrounding scene.

Requirements:

- Maintain a consistent relationship with the ground and nearby objects.
- Respond appropriately to visible wind, water, and environmental forces.
- Preserve human-object scale.
- Represent natural contact and support.
- Maintain plausible shadows and reflections on nearby surfaces.
- Coordinate human movement with environmental changes.
- Avoid environmental effects unsupported by the scene.

## G25. Behavioral Coherence

**Objective:** Ensure the subject's movements collectively express the intended action or state.

Requirements:

- Maintain coherence between posture, gesture, facial expression, and gaze.
- Produce gestures appropriate to the specified action.
- Preserve plausible body language.
- Allow subtle variation without random behavior.
- Avoid contradictory simultaneous actions.
- Preserve coherent action progression.
- Respect deliberate restraint, stillness, or minimal movement.

## G26. Reference Fidelity and Multi-Image Reconciliation

**Objective:** Preserve reliable source information without inventing contradictory characteristics.

Requirements:

- Identify reference-established appearance and anatomical characteristics.
- Use multiple images to resolve pose, angle, and visible detail.
- Distinguish genuine reference differences from lighting or perspective differences.
- Maintain consistent interpretation of the same person across images.
- Do not average incompatible facial or body characteristics indiscriminately.
- Treat unobserved regions as uncertain rather than definitively known.
- Generate plausible unseen geometry when required without implying reference verification.
- Prioritize explicit creative instructions over incidental reference variation where appropriate.

## G27. Frame-Rate and Motion Presentation

**Objective:** Preserve believable motion at the intended video playback rate.

Requirements:

- Maintain coherent movement between sampled frames.
- Avoid unintended temporal jumps and duplicate-frame stutter.
- Represent fast movement with plausible motion blur where appropriate.
- Avoid excessive blur that destroys recognizable anatomy.
- Maintain consistent speed across frame interpolation.
- Prevent abrupt movement resets.
- Respect intentional slow-motion and accelerated-motion effects.

## G28. Artifact Prevention and Error Control

**Objective:** Prevent visible failures that undermine human realism.

Requirements:

- Prevent duplicated or disappearing anatomy.
- Prevent unintended limb fusion and body-part merging.
- Prevent inconsistent finger and toe counts.
- Prevent face and body morphing.
- Prevent texture swimming and edge tearing.
- Prevent floating hands, feet, or accessories.
- Prevent unintended clothing-body penetration.
- Prevent sudden lighting or color changes.
- Prevent implausible deformations or unexplained changes in proportions.
- Detect recurring and intermittent failures across the sequence.

## G29. Contextual Applicability

**Objective:** Apply the right realism rules to the right situations.

Requirements:

- Do not require motion when stillness is intentional.
- Do not require visibility of concealed body parts.
- Do not enforce bilateral symmetry where natural asymmetry exists.
- Do not impose one standardized body shape on all women.
- Do not require every expression, reflex, or biological action to occur.
- Account for differences in age, body proportions, movement ability, and individual anatomy.
- Apply environmental physics according to the actual scene.
- Respect the intended shot duration, camera framing, and action.
- Treat non-applicable requirements as N/A rather than failed.

---

# LEVEL 2 — ANATOMICAL REGIONS AND COMPONENTS

Level 2 is a complete anatomical inventory arranged from the top of the body to the bottom.

All Level 1 rules apply to each listed body part wherever relevant.

**For every Level 2 component, evaluate:**

- **A — Anatomy:** Shape, structure, dimensions, position, and connection to adjacent body parts.
- **B — Appearance:** Color, texture, surface detail, lighting, shadows, and reflections.
- **C — Motion:** Primary movement, secondary movement, and movement timing.
- **D — Deformation:** Stretching, compression, elasticity, and changes in shape.
- **E — Interaction:** Contact with nearby body parts, clothing, objects, and the environment.
- **F — Continuity:** Identity, proportions, detail preservation, and temporal stability.

Specific requirements differ by region; not every dimension applies equally.

## Region 01 — Hair and Scalp

### 01.01 Scalp
- Scalp shape and contour
- Skin texture and coloration
- Hair-root attachment and distribution
- Scalp visibility through hair
- Head movement correspondence

### 01.02 Hairline
- Hairline shape and placement
- Hairline density and natural irregularity
- Transition between forehead and scalp
- Hair-root continuity
- Stability through head rotations

### 01.03 Head Hair
- Strand definition and distribution
- Length, volume, and density
- Straight, wavy, curly, or coiled texture
- Color variation and highlights
- Hair growth direction
- Gravity response
- Inertia and secondary motion
- Strand-group interaction
- Wind response
- Contact with face, shoulders, and clothing
- Hairstyle preservation

### 01.04 Hair Parting, Fringes, and Styled Sections
- Parting placement
- Fringe and bang positioning
- Section separation and layering
- Consistent styling
- Natural movement of separated hair regions

### 01.05 Fine and Flyaway Hair
- Fine-strand visibility
- Natural hairline irregularity
- Soft edge appearance
- Light interaction
- Subtle movement
- Temporal stability

## Region 02 — Forehead and Brows

### 02.01 Forehead
- Shape and curvature
- Skin texture and pigmentation
- Muscle-related deformation
- Expression lines and folds
- Lighting and contour preservation

### 02.02 Brow Ridges
- Underlying bone contour
- Relationship with eye sockets
- Shadow formation
- Apparent volume during facial expressions

### 02.03 Eyebrows
- Position and alignment
- Shape, arch, and length
- Hair density and thickness
- Strand direction and color
- Inner and outer brow elevation
- Lowering, compression, and asymmetry
- Coordination with facial expressions
- Forehead skin deformation

### 02.04 Glabella (Area Between Eyebrows)
- Skin texture and contour
- Brow contraction
- Frowning and compression
- Expression-related skin folds

## Region 03 — Eyes and Surrounding Structures

### 03.01 Eye Sockets and Orbital Area
- Orbital shape and depth
- Eye position within the socket
- Surrounding contour and volume
- Shadowing
- Perspective consistency

### 03.02 Upper Eyelids
- Shape and thickness
- Eyelid crease
- Skin texture
- Blinking and closure
- Squinting and widening
- Skin folding during eye movement

### 03.03 Lower Eyelids
- Shape and thickness
- Skin texture and subtle folds
- Squinting movement
- Interaction with cheeks
- Tear-line appearance

### 03.04 Eyelashes
- Root attachment
- Length and curl
- Strand count and density appearance
- Color and highlights
- Movement with eyelids
- Upper and lower eyelash distinction

### 03.05 Eyeballs
- Position and geometry
- Coordinated movement
- Rotation within eye sockets
- Gaze orientation
- Binocular alignment

### 03.06 Iris
- Iris diameter and shape
- Color and radial pattern
- Visible detail
- Perspective deformation
- Consistent placement

### 03.07 Pupils
- Circular appearance under perspective
- Pupil size
- Light-dependent changes when appropriate
- Position within the iris
- Gaze stability

### 03.08 Sclera
- Visible eye-white geometry
- Natural color and shading
- Subtle visible surface detail
- Exposure changes with gaze and eyelids

### 03.09 Cornea and Tear Film
- Transparent appearance
- Surface reflections
- Catchlight placement
- Natural moisture and gloss
- Continuity during eye motion

### 03.10 Tear Ducts and Eye Corners
- Inner and outer eye-corner anatomy
- Tear-duct positioning
- Skin coloration and moisture
- Eyelid connection

### 03.11 Under-Eye Areas
- Under-eye contour and volume
- Skin texture and pigmentation
- Fine lines and folds
- Lighting and shadows
- Expression-related deformation

### 03.12 Temples
- Side-of-face contour
- Skin texture
- Eye and cheek transitions
- Lighting and perspective behavior

## Region 04 — Nose

### 04.01 Nasal Bridge
- Shape and profile
- Width and anatomical contour
- Skin texture and lighting
- Perspective stability

### 04.02 Nose Tip
- Shape and projection
- Skin texture and color
- Highlight behavior
- Subtle expression-related movement

### 04.03 Nostrils
- Shape and opening geometry
- Visibility from different angles
- Natural asymmetry
- Breathing-related expansion when appropriate

### 04.04 Nasal Wings (Alae)
- Shape and thickness
- Soft-tissue deformation
- Flaring behavior
- Connection to cheeks

### 04.05 Nasal Septum and Columella
- Anatomical positioning
- Shape and proportions
- Visibility from below
- Consistent geometry

### 04.06 Nasolabial Region
- Nose-to-cheek transition
- Nasolabial folds
- Smile-related movement
- Skin compression and stretching

## Region 05 — Midface and Cheeks

### 05.01 Cheekbones
- Bone contour
- Facial width and projection
- Highlight and shadow behavior
- Volume continuity

### 05.02 Cheeks
- Soft-tissue volume
- Skin texture and color
- Smiling and laughing deformation
- Compression and relaxation
- Interaction with eyes and mouth

### 05.03 Midface Soft Tissue
- Volume distribution
- Natural asymmetry
- Expression-driven movement
- Skin elasticity
- Transitions to nose, ears, and jaw

## Region 06 — Ears

### 06.01 Outer Ear (Auricle)
- Overall shape and size
- Position and angle
- Cartilage folds
- Skin texture and lighting
- Hair interaction

### 06.02 Ear Rim (Helix)
- Curvature and thickness
- Consistent silhouette
- Lighting and occlusion

### 06.03 Inner Ear Structures
- Antihelix, concha, tragus, and antitragus contours
- Depth and natural shadowing
- Stable structure during head movement

### 06.04 Earlobes
- Shape and volume
- Soft-tissue behavior
- Skin texture
- Earring attachment when present

### 06.05 Ear Canal Opening
- Visible opening position
- Shading and depth
- Perspective-dependent visibility

## Region 07 — Mouth and Lower Face

### 07.01 Upper Lip
- Shape and volume
- Cupid's bow
- Lip texture and pigmentation
- Moisture and reflections
- Speech and expression movement

### 07.02 Lower Lip
- Shape and volume
- Natural surface lines
- Moisture and highlights
- Opening and closure
- Compression and protrusion

### 07.03 Lip Corners
- Position and symmetry
- Smiling and frowning movement
- Stretching and compression
- Interaction with cheeks

### 07.04 Philtrum
- Upper-lip-to-nose anatomy
- Contour and skin texture
- Deformation during speech

### 07.05 Oral Opening
- Aperture size and shape
- Mouth opening and closure
- Interior visibility
- Natural shadowing
- Speech coordination

### 07.06 Teeth
- Tooth count and arrangement where visible
- Size and alignment
- Color and natural gloss
- Stable tooth identity
- Correct occlusion and bite alignment

### 07.07 Gums
- Gingival shape
- Color and texture
- Visibility when speaking or smiling
- Connection to teeth

### 07.08 Tongue
- Shape and volume
- Surface color and texture
- Articulation during speech
- Contact with teeth and palate
- Natural occlusion

### 07.09 Inner Mouth and Palate
- Anatomical depth
- Soft palate and hard palate where visible
- Mouth cavity coloration
- Lighting and shadowing
- Stable geometry

### 07.10 Jaw and Mandible
- Lower-face proportions
- Jawline shape
- Opening and closing
- Forward and lateral jaw movement
- Coordination with facial muscles

### 07.11 Chin
- Shape and projection
- Skin texture and creases
- Mentalis-region muscle movement
- Lower-lip connection
- Expression-related deformation

### 07.12 Jawline and Jowls
- Facial contour
- Muscle and soft-tissue distribution
- Age- and individual-specific appearance
- Skin deformation
- Head-rotation consistency

## Region 08 — Neck and Throat

### 08.01 Front Neck
- Neck length and circumference
- Skin texture and pigmentation
- Muscle and tendon visibility
- Stretching and compression
- Head-motion coordination

### 08.02 Sides of Neck
- Sternocleidomastoid contours
- Rotation and tilting
- Muscle-related changes
- Skin folds and shadows

### 08.03 Back of Neck
- Neck-to-spine connection
- Muscle contour
- Bending and extension
- Hair and clothing contact

### 08.04 Throat and Laryngeal Region
- Anatomical contour
- Speech-related subtle movement
- Swallowing
- Skin and tissue behavior

### 08.05 Neck-to-Shoulder Transition
- Muscle geometry
- Head-support posture
- Shoulder elevation and rotation
- Surface continuity

## Region 09 — Shoulders and Clavicular Area

### 09.01 Clavicles
- Placement and visible shape
- Upper-torso connection
- Shoulder-motion relationship
- Lighting and shadowing

### 09.02 Trapezius Region
- Muscle contour
- Shoulder and neck motion
- Postural tension
- Surface deformation

### 09.03 Shoulder Joints
- Shoulder positioning
- Flexion, extension, and rotation
- Arm-to-torso attachment
- Joint movement limitations

### 09.04 Deltoid Areas
- Shape and volume
- Muscle-related deformation
- Skin texture
- Arm-raising movement

### 09.05 Armpits (Axillae)
- Anatomical folds
- Shoulder and torso connection
- Compression during arm lowering
- Stretching during arm elevation
- Skin and clothing interaction

## Region 10 — Chest and Breasts

### 10.01 Upper Chest
- Chest width and contour
- Skin texture and color
- Ribcage movement
- Breathing expansion
- Lighting and shadows

### 10.02 Sternum
- Central chest anatomy
- Bone-related surface contour
- Chest symmetry and asymmetry
- Breathing-related movement

### 10.03 Ribcage
- Structural proportions
- Expansion and contraction
- Torso rotation
- Posture-dependent geometry

### 10.04 Pectoral Region
- Upper-chest muscle contour
- Shoulder connection
- Arm-motion-related deformation
- Surface and volume preservation

### 10.05 Left and Right Breasts
- Individual shape and proportions
- Volume distribution
- Natural asymmetry
- Soft-tissue and gravitational behavior
- Posture-dependent shape
- Primary and secondary movement
- Tissue settling
- Clothing compression and support
- Collision with torso and arms

### 10.06 Nipples and Areolae (When Visible)
- Position and anatomical proportion
- Color and texture
- Surface contour
- Consistent attachment to surrounding tissue
- Movement with breast deformation

### 10.07 Under-Breast and Chest Folds
- Tissue contact and compression
- Shadow behavior
- Postural deformation
- Clothing interaction

## Region 11 — Back and Spine

### 11.01 Upper Back
- Shape and curvature
- Muscle distribution
- Skin texture
- Shoulder coordination

### 11.02 Shoulder Blades (Scapulae)
- Bone positioning
- Shoulder movement
- Scapular rotation and translation
- Surface contour changes

### 11.03 Thoracic Spine Region
- Upper-back curvature
- Torso rotation and flexion
- Postural variation
- Skin and muscle deformation

### 11.04 Mid-Back
- Muscle and soft-tissue contour
- Twisting and bending
- Skin folds
- Lighting and shadows

### 11.05 Lower Back
- Lumbar curvature
- Pelvis connection
- Forward and backward bending
- Rotation and lateral flexion
- Skin and soft-tissue deformation

### 11.06 Sacral Region
- Lower spine to pelvis transition
- Surface contour
- Postural deformation
- Stable anatomical connection

## Region 12 — Upper Arms and Elbows

### 12.01 Upper Arms
- Arm length and circumference
- Muscle and adipose-tissue distribution
- Skin texture and color
- Shoulder-driven movement
- Soft-tissue behavior

### 12.02 Front Upper Arm
- Biceps-region contour
- Flexion-related muscle shape
- Skin and soft-tissue deformation

### 12.03 Back Upper Arm
- Triceps-region contour
- Extension-related movement
- Gravity-dependent tissue behavior

### 12.04 Elbows
- Joint shape and alignment
- Bending and extension
- Skin folds and compression
- Bone prominence
- Natural movement range

### 12.05 Inner Elbow
- Skin creases
- Compression during flexion
- Texture and lighting
- Connection to forearm

## Region 13 — Forearms and Wrists

### 13.01 Forearms
- Length and tapered proportions
- Muscle and tendon contour
- Skin texture
- Rotation and flexion
- Arm-hand coordination

### 13.02 Inner Forearms
- Skin texture and pigmentation
- Vein visibility where appropriate
- Muscle-related movement

### 13.03 Outer Forearms
- Bone and muscle contour
- Tendon definition
- Lighting and shadow consistency

### 13.04 Wrists
- Joint proportions
- Flexion and extension
- Side-to-side movement
- Anatomical range constraints
- Connection to the hands

### 13.05 Wrist Tendons and Creases
- Visible contour
- Skin folds
- Motion-related changes
- Stable placement

## Region 14 — Hands and Fingers

### 14.01 Hands — General
- Correct anatomy and proportions
- Hand orientation
- Surface geometry
- Skin appearance
- Gesture coordination
- Object interactions

### 14.02 Palms
- Palm shape and volume
- Palm creases
- Skin texture
- Compression and stretching
- Grip contact

### 14.03 Back of Hands
- Knuckle geometry
- Vein and tendon visibility
- Skin texture
- Lighting and shadow behavior

### 14.04 Thumbs
- Correct thumb placement
- Two phalanges and associated joint mechanics
- Opposition and rotation
- Grip participation
- Contact behavior

### 14.05 Index Fingers
- Finger length and shape
- Joint articulation
- Pointing and gripping
- Independent movement

### 14.06 Middle Fingers
- Proportions
- Joint articulation
- Coordination with neighboring fingers

### 14.07 Ring Fingers
- Proportions
- Joint articulation
- Coordination with other fingers
- Ring interaction when present

### 14.08 Little Fingers
- Proportions
- Joint articulation
- Grip stabilization
- Natural movement

### 14.09 Finger Joints and Knuckles
- Correct joint positions
- Natural joint limits
- Skin folds
- Bending-related geometry

### 14.10 Fingertips and Finger Pads
- Shape and volume
- Surface texture
- Contact compression
- Grip pressure
- Fine gesture control

### 14.11 Fingernails
- Nail shape and curvature
- Thickness and translucency
- Nail-bed connection
- Cuticle region
- Natural reflections
- Nail polish consistency when present

### 14.12 Interdigital Webbing
- Skin between fingers
- Natural stretching
- Stable anatomical connections
- Movement-related deformation

## Region 15 — Abdomen and Waist

### 15.01 Upper Abdomen
- Surface contour
- Muscle and soft-tissue distribution
- Breathing movement
- Skin texture and lighting

### 15.02 Central Abdomen
- Shape and volume
- Posture-dependent deformation
- Abdominal tension and relaxation
- Breathing coordination

### 15.03 Lower Abdomen
- Skin and soft-tissue contour
- Compression during bending and sitting
- Gravity response
- Pelvic transition

### 15.04 Navel
- Position and shape
- Depth and shading
- Skin texture
- Stable positioning during deformation

### 15.05 Waist
- Circumference and contour
- Natural individual variation
- Torso rotation
- Bending and compression
- Clothing contact

### 15.06 Sides of Torso and Flanks
- Surface contour
- Muscle and soft-tissue distribution
- Lateral bending
- Skin folds
- Breathing-related movement

## Region 16 — Pelvis, Hips, and Buttocks

### 16.01 Pelvis
- Anatomical alignment
- Relationship with spine and femurs
- Tilt and rotation
- Weight distribution
- Locomotion coordination

### 16.02 Hip Joints
- Flexion and extension
- Rotation and abduction
- Joint movement limits
- Pelvis-leg connection

### 16.03 Hip Surfaces
- Hip width and silhouette
- Skin and soft-tissue contours
- Posture-dependent changes
- Clothing interaction

### 16.04 Groin and Inguinal Creases
- Leg-to-pelvis transition
- Natural surface folds
- Bending and compression
- Occlusion and clothing interaction

### 16.05 External Genital Region (When Visible)
- Anatomical positioning and external contour
- Skin and soft-tissue characteristics
- Natural variation
- Stable pelvic attachment
- Contextual visibility and occlusion
- Anatomical continuity during hip and leg movement

### 16.06 Pubic Region
- Lower abdominal transition
- Surface shape and contour
- Skin and hair appearance when visible
- Clothing interaction

### 16.07 Buttocks
- Shape, volume, and individual asymmetry
- Muscle and soft-tissue distribution
- Gravity and secondary movement
- Walking and running behavior
- Sitting-related compression
- Clothing pressure and deformation

### 16.08 Gluteal Fold
- Natural fold positioning
- Tissue contact
- Posture-dependent deformation
- Lighting and shadows

## Region 17 — Thighs

### 17.01 Front Thighs
- Femur-related anatomy
- Quadriceps-region contour
- Skin texture and pigmentation
- Muscle-driven movement
- Hip and knee coordination

### 17.02 Back Thighs
- Hamstring-region contour
- Muscle deformation
- Hip and knee movement
- Buttock-to-thigh transition

### 17.03 Inner Thighs
- Shape and soft-tissue distribution
- Leg-to-leg contact
- Friction and compression
- Skin folds and lighting

### 17.04 Outer Thighs
- Lateral contour
- Hip connection
- Muscle and soft-tissue movement
- Proportion consistency

### 17.05 Thigh-to-Knee Transition
- Anatomical taper
- Muscle and tendon contour
- Skin deformation
- Joint continuity

## Region 18 — Knees

### 18.01 Kneecaps (Patellae)
- Position and shape
- Surface contour
- Movement during knee bending
- Lighting and shadows

### 18.02 Front Knee Structures
- Bone and tendon definition
- Skin texture
- Flexion and extension
- Anatomical alignment

### 18.03 Back of Knees
- Skin folds
- Tissue compression during bending
- Joint contour
- Movement continuity

### 18.04 Knee Joints
- Flexion and extension
- Rotation within anatomical limits
- Leg alignment
- Weight-bearing stability
- Locomotion coordination

## Region 19 — Lower Legs

### 19.01 Calves
- Gastrocnemius and soleus-region contours
- Muscle contraction
- Shape changes during movement
- Soft-tissue consistency
- Skin texture and lighting

### 19.02 Shins
- Tibial contour
- Skin texture and pigmentation
- Muscle and tendon visibility
- Perspective stability

### 19.03 Inner Lower Legs
- Anatomical curvature
- Surface texture
- Tendon and muscle contours
- Alignment

### 19.04 Outer Lower Legs
- Fibular-side contour
- Muscle distribution
- Skin texture
- Motion-related deformation

### 19.05 Achilles Tendons
- Position and thickness
- Tendon movement
- Connection to heel
- Shape changes during ankle motion

## Region 20 — Ankles

### 20.01 Ankle Joints
- Joint positioning and alignment
- Dorsiflexion and plantarflexion
- Complex foot-ankle movement
- Weight-bearing stability

### 20.02 Inner Ankles
- Medial malleolus contour
- Skin texture and lighting
- Joint movement consistency

### 20.03 Outer Ankles
- Lateral malleolus contour
- Surface geometry
- Joint alignment

### 20.04 Ankle Tendons and Creases
- Tendon visibility
- Skin folds
- Movement-related contour changes
- Foot-leg continuity

## Region 21 — Feet

### 21.01 Feet — General
- Foot length, width, and proportions
- Left-right anatomical consistency
- Ground contact
- Weight distribution
- Balance
- Footwear interaction

### 21.02 Tops of Feet
- Bone and tendon contours
- Skin texture
- Lighting and shadows
- Movement-related deformation

### 21.03 Foot Arches
- Natural arch shape
- Individual anatomical variation
- Load-dependent behavior
- Ground support

### 21.04 Soles
- Sole contours
- Skin texture
- Contact compression
- Friction with surfaces
- Weight-bearing behavior

### 21.05 Heels
- Shape and volume
- Contact mechanics
- Skin texture
- Heel strike and lift
- Compression under load

### 21.06 Balls of Feet
- Forefoot geometry
- Contact pressure
- Weight transfer
- Push-off movement

### 21.07 Side Edges of Feet
- Natural contours
- Contact variation
- Surface pressure
- Alignment and balance

## Region 22 — Toes and Toenails

### 22.01 Big Toes
- Correct structure and proportions
- Joint movement
- Balance and push-off
- Ground contact

### 22.02 Second Toes
- Length and proportions
- Joint articulation
- Ground contact

### 22.03 Middle Toes
- Shape and spacing
- Joint articulation
- Coordinated movement

### 22.04 Fourth Toes
- Proportions
- Joint articulation
- Foot-balance participation

### 22.05 Little Toes
- Shape and placement
- Joint movement
- Natural contact behavior

### 22.06 Toe Joints
- Bending and extension
- Joint positioning
- Skin folds
- Natural mobility

### 22.07 Toe Pads
- Surface texture
- Ground contact
- Soft-tissue compression
- Grip-related behavior

### 22.08 Toenails
- Shape and curvature
- Nail-bed connection
- Color and translucency
- Lighting and reflections
- Nail polish stability when present

### 22.09 Interdigital Toe Spaces
- Natural spacing and webbing
- Skin texture
- Compression during contact
- Anatomical consistency

---

# LEVEL 1 AND LEVEL 2 RELATIONSHIP

All anatomical components are governed by relevant global requirements.

Examples:

**Eyebrows:** Identity preservation, anatomical integrity, skin deformation, facial expression, lighting, temporal consistency.

**Eyes:** Anatomy, material behavior, gaze coordination, expression, biological movement, temporal consistency.

**Hair:** Identity preservation, texture, material appearance, gravity, secondary motion, environmental response, temporal consistency.

**Breasts:** Anatomical integrity, volume consistency, soft-tissue deformation, gravity, contact, clothing interaction, temporal consistency.

**Hands:** Anatomy, joint movement, movement synchronization, interaction, perspective, temporal consistency, artifact prevention.

**Feet:** Anatomy, joint movement, balance, weight distribution, ground contact, locomotion coordination, temporal consistency.

## Final rule

The generated human must remain the same recognizable person, retain believable anatomy, and exhibit physically and behaviorally coherent motion throughout the sequence.

The requirements are conditional on visibility, action, context, and reference evidence. Quality should be assessed across the entire video, not solely on individual frames.

**End of Level 1 and Level 2 specification.**