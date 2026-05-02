# Workflow 檔案

這個資料夾用來放 ComfyUI workflow JSON。

已建立的主要 workflow：

- `asatake_yoshino_basic_comfyui.json`

未來可視需求新增：

- `sdxl_lora_basic.json`
- `sdxl_lora_openpose.json`
- `sdxl_lora_inpaint.json`
- `sdxl_lora_upscale.json`

基本 workflow 應包含：

1. SDXL anime checkpoint
2. 角色 LoRA
3. Positive prompt
4. Negative prompt
5. KSampler
6. Save Image 或 Save Image With Seed

基礎 workflow 穩定後，再加入 OpenPose、inpaint 或 upscale 版本。
