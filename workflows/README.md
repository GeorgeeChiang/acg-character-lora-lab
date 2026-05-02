# Workflow Files

Put ComfyUI workflow JSON files here.

Suggested workflow files to create later:

- `sdxl_lora_basic.json`
- `sdxl_lora_openpose.json`
- `sdxl_lora_inpaint.json`
- `sdxl_lora_upscale.json`

The first real workflow should load:

1. SDXL anime checkpoint
2. Character LoRA
3. Positive prompt
4. Negative prompt
5. KSampler
6. Save Image

After the basic workflow is stable, add OpenPose and inpaint variants.
