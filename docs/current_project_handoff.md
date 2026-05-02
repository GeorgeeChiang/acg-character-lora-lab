# Current Project Handoff

Maintainer note: this handoff was written by Codex / GPT-5 on 2026-05-02.

This file is the quickest entry point for the next agent. Read it after `AGENTS.md` and `README.md`.

## Current Goal

| Item | Current state |
|---|---|
| Project | Local ACG character image experiment workspace |
| Character | 朝武芳乃 / Tomotake Yoshino / Asatake Yoshino |
| Work | 千恋＊万花 / Senren Banka |
| Main goal | Use local ComfyUI workflows and SDXL/Pony checkpoints to generate character images with LoRA |
| Hardware target | Windows 11, AMD 9800X3D, 64GB RAM, RTX 5080 16GB VRAM |

## What Is Already Done

| Stage | Status | Notes |
|---|---|---|
| Project scaffold | Done | README, AGENTS, docs, configs, scripts, workflows, templates are present |
| Image collection | Done for this character | Raw images are in `data/raw/senren_banka_asatake_yoshino/` |
| Dataset review | Done for first pass | Selected and rejected sets exist under `data/selected/` and `data/rejected/` |
| Training dataset | Done for first pass | Image + caption pairs are in `data/train/senren_banka_asatake_yoshino/` |
| First LoRA training | Done | v1 was trained and installed in ComfyUI |
| Second LoRA training | Done | v2 is the preferred self-trained LoRA |
| ComfyUI workflow | Done | Workflow JSON is in `workflows/asatake_yoshino_basic_comfyui.json` |
| Knowledge documentation | Done | Main notes are in `docs/06_project_knowledge_notes.md` |
| Project cleanup | Done | Intermediate step LoRAs were removed from project outputs to save space |

## Important Local Paths

| Purpose | Path |
|---|---|
| Project root | `C:\Users\dodo\Documents\Codex\ACG_AI_picture` |
| Raw images | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\data\raw\senren_banka_asatake_yoshino` |
| Training images and captions | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\data\train\senren_banka_asatake_yoshino` |
| Project LoRA output | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\lora` |
| Project generated samples | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\samples` |
| ComfyUI root | `C:\Users\dodo\ComfyUI\ComfyUI-master` |
| ComfyUI checkpoints | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints` |
| ComfyUI LoRAs | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\loras` |
| ComfyUI output | `C:\Users\dodo\ComfyUI\ComfyUI-master\output` |
| Project workflow | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\workflows\asatake_yoshino_basic_comfyui.json` |
| ComfyUI user workflow | `C:\Users\dodo\ComfyUI\ComfyUI-master\user\default\workflows\asatake_yoshino_basic_comfyui.json` |

## Installed Checkpoints In ComfyUI

| File | Type | Notes |
|---|---|---|
| `Illustrious-XL-v0.1.safetensors` | SDXL checkpoint | Original project base model |
| `animagine-xl-4.0.safetensors` | SDXL ACG checkpoint | Downloaded for comparison |
| `ponyDiffusionV6XL_v6StartWithThisOne.safetensors` | Pony/SDXL checkpoint | Downloaded for Pony-style testing |
| `NoobAI-XL-v1.1.safetensors` | SDXL ACG checkpoint | Downloaded for comparison |
| `autismmixSDXL_autismmixPony.safetensors` | Pony/SDXL checkpoint | Used by the Civitai Yoshino LoRA examples |

## Installed LoRAs In ComfyUI

| File | Type | Trigger words / notes |
|---|---|---|
| `senren_banka_asatake_yoshino_v2.safetensors` | Self-trained character LoRA | Preferred self-trained LoRA. Use `sksgirl, asatake yoshino` plus visual tags. |
| `senren_banka_asatake_yoshino_v1.safetensors` | Self-trained character LoRA | Older self-trained version. Keep for comparison. |
| `senren_banka_asatake_yoshino_v1-step00001000.safetensors` | Self-trained step checkpoint | Kept only in ComfyUI model folder; not the preferred version. |
| `senren_banka-tomotake_yoshino-ponyxl.safetensors` | External Civitai LoRA | Use `tomotake_yoshino` and outfit trigger words. |
| `Masou_Shizuka_1_nai-000041.safetensors` | Unrelated LoRA | Not part of this character workflow. |

## How To Start ComfyUI

Use the project script:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\dodo\Documents\Codex\ACG_AI_picture\scripts\start_comfyui.ps1"
```

Default URL:

```text
http://127.0.0.1:8188/
```

If a background launch is needed, run ComfyUI from:

```text
C:\Users\dodo\ComfyUI\ComfyUI-master
```

with:

```powershell
.\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8188
```

## How To Stop ComfyUI

Check port 8188 and stop the owning Python process. Be careful to stop only ComfyUI processes, not unrelated Python work.

```powershell
Get-NetTCPConnection -LocalPort 8188 -State Listen
```

Then stop the returned owning process if it is ComfyUI.

## Workflow Notes

| Node | Use |
|---|---|
| `CheckpointLoaderSimple` | Select the base checkpoint |
| `LoraLoader` | Select the character LoRA and set strength |
| Positive `CLIPTextEncode` | Put prompt here |
| Negative `CLIPTextEncode` | Put negative prompt here |
| `KSampler` | Set seed, steps, CFG, sampler, scheduler, denoise |
| `Save Image With Seed` | Preferred save node because it writes seed into output filename |

If output filenames do not include seed, check whether the workflow is using `Save Image With Seed` instead of the default `SaveImage`.

## Prompt Starting Points

Self-trained v2 LoRA:

```text
masterpiece, best quality, very aesthetic, absurdres, sksgirl, asatake yoshino, 1girl, white hair, blue eyes, long twintails, large round blue eyes, symmetrical eyes, shrine maiden outfit, full body, shrine background, anime illustration
```

Civitai PonyXL LoRA:

```text
score_9, score_8_up, score_7_up, source_anime, tomotake_yoshino, yuzu-soft, white_hair, very_long_hair, blue_eyes, parted_bangs, tomotake_yoshino_miko_clothing, miko_clothing, twintails, hair_ornament, hair_flower, japanese_clothes, white_kimono, red_hakama, hakama_skirt, shrine background
```

Negative prompt:

```text
low quality, worst quality, bad anatomy, bad hands, extra fingers, missing fingers, distorted face, asymmetrical eyes, uneven eyes, different eye size, cross-eyed, squinting, text, watermark, logo
```

## Recommended Next Steps

| Priority | Task |
|---|---|
| 1 | Test the self-trained v2 LoRA across installed checkpoints with fixed seed and fixed prompt |
| 2 | Test the external Civitai PonyXL LoRA with `autismmixSDXL_autismmixPony.safetensors` |
| 3 | Compare identity, hair color, eye shape, outfit accuracy, hands, and background |
| 4 | Record results in `logs/` or a new evaluation CSV |
| 5 | If identity is still weak, consider improving captions or retraining with cleaner selected data |

## Do Not Delete Without User Approval

| Path / file | Reason |
|---|---|
| `data/raw/` | Original source images |
| `data/train/` | Training image + caption pairs |
| `outputs/lora/senren_banka_asatake_yoshino_v2.safetensors` | Preferred self-trained LoRA |
| `workflows/asatake_yoshino_basic_comfyui.json` | Reusable ComfyUI workflow |
| `docs/06_project_knowledge_notes.md` | Main knowledge record |
| `docs/character_ai_pipeline_sop.md` | Main SOP |

## Safety Boundary

Do not assist with generating explicit sexual images. It is fine to help with non-explicit character similarity, outfits, backgrounds, prompt structure, model setup, workflow debugging, and general generation quality.

