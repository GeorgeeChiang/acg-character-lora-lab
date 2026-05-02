# Tool Setup Plan

Target machine: Windows + NVIDIA RTX 5080.

## Required Base Tools

Install first:

- NVIDIA driver: from NVIDIA official driver page.
- Git for Windows: https://git-scm.com/download/win
- Python: use the version required by each tool; A1111 commonly expects Python 3.10.x.
- 7-Zip: useful for model/tool archives.

## Generation Tools

Recommended:

- ComfyUI Desktop or Windows Portable
  - Source: https://github.com/Comfy-Org/ComfyUI
  - Use for LoRA loading, ControlNet/OpenPose workflows, inpaint, and repeatable graph-based tests.

Alternative:

- AUTOMATIC1111 stable-diffusion-webui
  - Source: https://github.com/AUTOMATIC1111/stable-diffusion-webui
  - Use if a tabbed UI feels easier than ComfyUI nodes.

## Training Tools

Recommended:

- kohya_ss GUI
  - Source: https://github.com/bmaltais/kohya_ss
  - Use for first SDXL LoRA training.

Advanced:

- kohya-ss/sd-scripts
  - Source: https://github.com/kohya-ss/sd-scripts
  - Use when you want reproducible command-line training.

## Captioning and Dataset Tools

- ComfyUI-WD14-Tagger
  - Source: https://github.com/pythongosssss/ComfyUI-WD14-Tagger
  - Put into ComfyUI `custom_nodes`.

- Dataset Tag Editor
  - Source: https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor
  - Good for editing many caption files.

- Spreadsheet review
  - Use `templates/dataset_review_sheet.csv`.
  - Best for keep/reject decisions and notes.

## Model Sources

Use models that fit the experiment goal and the selected UI.

- Hugging Face: common source for official/open model files.
- Civitai: common source for community anime SDXL models and LoRAs.
- ComfyUI model folders:
  - Checkpoints: `ComfyUI/models/checkpoints/`
  - LoRA: `ComfyUI/models/loras/`
  - ControlNet: `ComfyUI/models/controlnet/`
  - VAE: `ComfyUI/models/vae/`

## First Local Setup Order

1. Install NVIDIA driver, Git, Python, and 7-Zip.
2. Install ComfyUI Desktop or Windows Portable.
3. Download one anime SDXL checkpoint for local testing.
4. Confirm ComfyUI can generate one image.
5. Install ComfyUI-WD14-Tagger.
6. Install kohya_ss GUI.
7. Train one test LoRA from a small curated dataset.
8. Load the LoRA in ComfyUI and run the 10-prompt test plan.

## Suggested Initial LoRA Settings

Use these as starting points, not final truth:

- Model family: SDXL anime checkpoint
- Resolution: 1024 if stable, otherwise 768
- Network dim/rank: 16 or 32
- Batch size: 1-2
- Learning rate: around `1e-4`
- Save every: 200-300 steps
- Total steps: 800-2000
- Test checkpoints: 800, 1000, 1200, 1500

