# Data Collection Pipeline

Goal: when the user provides an ACG work title, a character name, or both, collect candidate references, clean them, and select images suitable for a character LoRA dataset.

## Inputs

- Work title
- Character name
- Reference site, wiki URL, or search hint, if available
- Whether the user has local images/screenshots
- Intended use: local experiment only by default

## Agent-Assisted Collection

Use agents/search as a research assistant, not as an automatic mass scraper.

1. Identify canonical character details
   - Confirm original title, character spelling, aliases, romanization, and visual traits.
   - Record reliable reference sources first when available.

2. Build a candidate source list
   - Priority A: user-provided images/screenshots and high-quality reference pages.
   - Priority B: public search results and image-board/wiki references.
   - Prefer diverse poses, expressions, outfits, and angles over many near-duplicates.

3. Collect candidate images into `data/raw/<character_id>/`
   - Keep source URL or local source note per image.
   - Do not blindly scrape large archives.

4. Remove unusable images
   - Reject images with dialogue boxes, UI, watermarks, compression damage, other main characters, heavy effects, or tiny faces.
   - Reject near-duplicates unless the expression or pose meaningfully changes.

5. Crop and normalize
   - Keep the character large in frame.
   - Preserve full-body images when possible.
   - Prefer PNG/WebP lossless conversion for training copies.

6. Caption
   - Auto-caption with WD14 tagger, then manually edit.
   - Always include one trigger token, for example `sksgirl`.
   - Separate identity from variable traits such as clothing, pose, expression, and camera angle.

## Dataset Shape

Recommended local structure:

```txt
data/
  raw/<character_id>/
  selected/<character_id>/
  rejected/<character_id>/
  train/<character_id>/
    001.png
    001.txt
```

## Selection Rules

Good first dataset:

- 25-50 clean images for one character
- At least 8 face/portrait images
- At least 8 upper-body images
- At least 5 full-body or larger-pose images
- Multiple expressions if available
- Multiple angles if available

Risk signs:

- Only one standing sprite with expression variants
- Mostly screenshots with text boxes
- Character is frequently occluded
- Outfit never changes but user wants outfit changes later

## Human Review Gate

Before training, review every image with `templates/dataset_review_sheet.csv`.

Required decisions:

- Keep / reject
- Main reason
- Needed crop
- Caption quality
- Whether it looks too close to an original CG composition

## Project Scope

All datasets, trained LoRA weights, and generated images are treated as local experiment artifacts and are not intended for external publication or sharing.

