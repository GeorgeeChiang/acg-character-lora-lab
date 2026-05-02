# Generation Test Plan

Purpose: test whether a character LoRA can preserve identity while allowing different compositions.

Use the same seed set, base model, sampler, LoRA strength, and negative prompt when comparing checkpoints.

## Default Prompt Pieces

Trigger placeholder:

```txt
<trigger>, 1girl
```

Quality/style baseline:

```txt
ACG illustration, anime style, detailed eyes, clean lineart, soft shading
```

Negative baseline:

```txt
low quality, worst quality, bad anatomy, extra fingers, missing fingers, distorted face, text, watermark, logo
```

Start LoRA strength:

```txt
0.70
```

## 10 Composition Tests

1. Portrait identity
   - Prompt: `<trigger>, 1girl, close-up portrait, looking at viewer, gentle smile`
   - Purpose: face, eyes, hair, baseline similarity.

2. Upper-body character pose
   - Prompt: `<trigger>, 1girl, upper body, standing in classroom, one hand on chest, soft morning light`
   - Purpose: standard ACG character composition usability.

3. Full-body standing
   - Prompt: `<trigger>, 1girl, full body, standing, simple background, neutral pose`
   - Purpose: outfit and silhouette consistency.

4. Side view
   - Prompt: `<trigger>, 1girl, side view, looking away, wind blowing hair, outdoor walkway`
   - Purpose: identity under non-front angle.

5. Looking back
   - Prompt: `<trigger>, 1girl, looking back over shoulder, three-quarter view, evening street`
   - Purpose: flexible camera angle.

6. Sitting by window
   - Prompt: `<trigger>, 1girl, sitting by window, knees together, soft backlight, quiet room`
   - Purpose: seated pose and mood scene.

7. Dynamic motion
   - Prompt: `<trigger>, 1girl, running, dynamic pose, hair flowing, school courtyard`
   - Purpose: pose flexibility and motion artifacts.

8. Emotional close-up
   - Prompt: `<trigger>, 1girl, close-up, teary eyes, sad expression, night lighting`
   - Purpose: expression range without losing identity.

9. Outfit variation
   - Prompt: `<trigger>, 1girl, casual hoodie, city cafe, relaxed smile`
   - Purpose: whether identity survives clothing changes.

10. Inpaint repair test
   - Prompt: generate any failed hand/face image, then inpaint only the bad area.
   - Purpose: confirm repair workflow, not just raw generation.

## Optional ControlNet Tests

After raw prompt tests, repeat tests 3, 5, 6, and 7 with OpenPose.

Evaluation:

- Does the pose follow the reference?
- Does identity remain at LoRA strength 0.60-0.85?
- Does ControlNet make the image too stiff?

## Score Sheet

Rate each output from 1-5:

- Identity similarity
- Prompt following
- Pose/composition
- Face quality
- Hand/body quality
- Outfit flexibility
- Original-image overfit risk

Preferred checkpoint:

- Identity average >= 4
- Pose/composition average >= 3
- Overfit risk <= 2
- Does not require LoRA strength above 0.9

