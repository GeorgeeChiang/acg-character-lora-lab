# Windows Local Setup

This repository is now set up for a local-only LoRA workflow on Windows 11.

## Completed

- Python 3.10.11 installed
- 7-Zip installed
- ComfyUI installed with a working CUDA venv
- kohya_ss installed with a working CUDA venv
- Illustrious-XL-v0.1 SDXL checkpoint downloaded to ComfyUI models

## Remaining

- Start both GUIs once and verify they open
- Run the first LoRA training pass
- Run the 10 composition tests
- Fine-tune captioning or dataset size if the first pass overfits

## Launch Helpers

- `scripts/start_comfyui.ps1`
- `scripts/start_kohya_gui.ps1`

## Suggested Working Paths

| Tool | Path |
|---|---|
| Python | `%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe` |
| 7-Zip | `%ProgramFiles%\\7-Zip\\7z.exe` |
| ComfyUI | `C:\\Users\\dodo\\ComfyUI\\ComfyUI-master` |
| kohya_ss | `C:\\Users\\dodo\\kohya_ss\\kohya_ss-master` |
| Base checkpoint | `C:\\Users\\dodo\\ComfyUI\\ComfyUI-master\\models\\checkpoints\\Illustrious-XL-v0.1.safetensors` |
