# Generic motion scheduling contract

The motion scheduler turns selected scene behavior into a model-independent temporal plan. When motion-reference video exists, analyze it before scheduling: record what motion and timing it controls, exclude its identity and setting unless requested, and preserve its real-time rhythm.

## Time model

All canonical windows use normalized clip time:

- `0.0` is the opening generated frame;
- `1.0` is the ending generated frame;
- a window `[0.25, 0.5]` occupies the second quarter of any selected duration.

When a destination duration is known, run `scripts/resolve_motion_schedule.py` to add second-based windows. Normalized timing remains authoritative.

## Scheduling procedure

1. **Motion evidence:** Add each source clip to `motion_sources`, including duration, role, observations, excluded attributes, and confidence. Describe actual travel, rotation, contact, rebound, and rest instead of reducing the clip to milestone poses.
2. **Primary phases:** Map every beat involving a subject exactly once and preserve beat order. Mark each phase kind. Split each phase into `active_motion_windows` and `dwell_windows`; these may alternate inside a phase but never overlap. Clip duration is a container, not permission to stretch a short action across the whole phase.
3. **Tempo and velocity:** State the tempo source, descriptor, slow-motion status, and evidence. Default unspecified human motion to natural real-time speed. For every phase, describe onset, acceleration, peak, deceleration, and arrival. When a reference controls timing, use `reference_matched` and retain its bursts, holds, recoil, and follow-through.
   Also populate `performance_control.temporal_layers`. A slow voluntary action does not slow biological events, active balance corrections, or material response unless the user requests slow-motion footage.
4. **Articulated actions:** Define the ordered kinematic chain, path, contact progression, counterbalance, and release. A reach normally propagates through torso or scapula, shoulder, upper arm, elbow, forearm, wrist, hand, and fingers with overlaps and small lags; do not represent it as one rigid endpoint translation.
5. **Bounded variation:** Treat the first group member as the baseline. Every later member names its changed dimensions and describes the difference. Differences must come from `realism_selection.repetition_variation.dimensions`.
6. **Vitality tracks:** Schedule all five baseline cues and assign each a priority. Required and conditional cues need windows, a phase relationship, and variability. Continuous tracks span ongoing behavior; event tracks use candidate windows, a count range, and a physically plausible event-duration range in seconds; windowed tracks depend on particular phases.
7. **Secondary tracks:** Include only material visible responses. Name the driver, response, windows, lag, damping, and settling. A secondary track never becomes an independent decorative loop.
8. **Protected windows:** Use only a span already identified as a dwell. State the purpose and continuing motion. Never invent a pause, brake an active transition, or suppress source-defined follow-through merely to expose a subtle cue.
9. **Priority, coordination, and anti-synchrony:** Preserve the primary performance first, keep regions causally connected, and prevent biological or secondary events from recurring at one mechanical phase point.

## Quiet-performance scheduling

For idle or restrained behavior, do not use the timeline as a sequence of whole-body target poses. Preserve a continuous center-of-mass path and overlap the initiator, connected anatomy, passive response, and settling with small nonuniform delays. Explicitly state which regions remain quiet during each phase.

Keep plainly legible concurrency within the scene's motion budget: the primary action plus no more than one or two additional salient cues unless physiology requires more. Multiple subthreshold cues may coexist when they are causal, independent in phase, and individually below deliberate-performance amplitude. Candidate vitality windows provide opportunities, not obligations. Do not stack a blink, breath reversal, head-tilt apex, shoulder arrival, soft-tissue response, and facial change at one boundary.

For quiet respiration, schedule low-amplitude lower-rib/upper-abdominal motion while holding mouth aperture, jaw, throat, chin, head height, and shoulder elevation. A swallow, gasp, sigh, speech breath, or exertion breath is a different action and requires its own explicit disposition.

A dwell is not a rigid freeze or a reset pose. Maintain only the residual balance and below-performance-threshold vitality selected by the plan. Do not make every region arrive at zero velocity on the same frame except at an explicitly requested fully settled loop boundary.

Preserve every major dwell as an explicit interval. Adapters must not replace “hold from 8.0 to 10.0 seconds” with “settled by the end,” because the latter permits continued motion through the planned hold.

## Event windows

An event window is an allowed interval rather than an exact firing time. `count_range: [2, 3]` with four blink windows means that two or three windows may contain a blink. It does not request four blinks. This gives a video model temporal freedom while preventing a completely omitted cue or a metronomic event at every action boundary.

An event-duration range is measured in real seconds because biological event speed does not scale proportionally with clip length. It constrains the event itself, while normalized windows retain portability across destination durations. Model adapters may select an exact count and placement from the allowed range when stronger adherence requires it; that selection belongs in the model handoff and does not rewrite the canonical scene plan.

## Protected windows

Use protected windows only for required, visually subtle behavior such as a blink, a readable breath reversal, or a small contact change, and only inside an existing dwell. Keep the source performance's residual balance, recoil, fixation, tonus, and breathing alive. Do not add a new low-motion span, stack protected windows, or convert a dwell into a freeze.

## Multi-subject scenes

Create one schedule per subject. Each schedule contains only beats whose `subject_ids` include that subject. Use coordination rules to express contact, gaze, dialogue response, shared balance, or object handoff across subjects. Do not force unrelated subjects onto one biological rhythm.

## Adapter contract

Every model adapter must preserve:

- the primary action's observable completion criterion, distinguishing cues, causal order, endpoint evidence, and fallback;
- primary-phase order and relative duration;
- active travel versus dwell, real-time tempo, velocity shape, and articulated kinematic chains;
- the selected differences among repeated phases;
- active vitality modes, candidate windows, and count ranges;
- vitality priority, event-duration bounds, protected windows, and the scene priority order;
- driver-to-response relationships, lag, damping, and settling;
- coordination and anti-synchrony rules.
- support state, posture invariants, behavioral reading, independent temporal layers, concurrency class, bounded variability, and reverse-sensitive loop handling.
- composition authority and the visibility boundary; hidden support mechanics stay out of prompt text unless they become visible.
- temporal-layer prompt exposure: explicit layers are stated, compact layers appear once, and implicit or omitted layers are not named.

Adapters translate this plan into natural language suited to the destination. They do not expose JSON field names, require every candidate event, invent per-frame noise, or discard the schedule merely to shorten a prompt.

## Validation boundary

The validator checks structure, subject and beat coverage, window order and range, cue-status agreement, event counts, selected variation dimensions, secondary-track identity, and required anti-synchrony. It cannot prove that a generated video follows the plan.
