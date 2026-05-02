# Open-Source Tool Survey

Checked on 2026-05-01. Star counts are approximate and can change.

## Recommended Stack

| Purpose | Project | Stars | Why use it | Link |
|---|---:|---:|---|---|
| Generation workflow | ComfyUI | 111k | Node-based workflows, strong ControlNet/LoRA/inpaint ecosystem | https://github.com/Comfy-Org/ComfyUI |
| Simpler generation UI | AUTOMATIC1111 WebUI | 162k | Mature UI, many extensions, easier for beginners | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| LoRA training scripts | kohya-ss/sd-scripts | 7k | Core SD/SDXL/FLUX LoRA training scripts | https://github.com/kohya-ss/sd-scripts |
| LoRA training GUI | bmaltais/kohya_ss | star count varies by GitHub page; high-usage GUI | Beginner-friendly GUI over kohya scripts | https://github.com/bmaltais/kohya_ss |
| Image downloading utility | gallery-dl | 18k | Broad gallery downloader; use only for allowed sources | https://github.com/mikf/gallery-dl |
| ControlNet reference | lllyasviel/ControlNet | 33.8k | Original ControlNet implementation and concepts | https://github.com/lllyasviel/ControlNet |
| A1111 ControlNet extension | Mikubill/sd-webui-controlnet | 17.8k | Plug-in ControlNet support for A1111 | https://github.com/Mikubill/sd-webui-controlnet |
| ComfyUI WD14 captioning | ComfyUI-WD14-Tagger | 1.2k | Auto booru-style tags inside ComfyUI | https://github.com/pythongosssss/ComfyUI-WD14-Tagger |
| A1111 WD14 captioning | stable-diffusion-webui-wd14-tagger | 1.4k | Useful but archived; prefer maintained alternatives when possible | https://github.com/toriato/stable-diffusion-webui-wd14-tagger |
| Dataset caption editing | stable-diffusion-webui-dataset-tag-editor | 729 | Batch-edit caption `.txt` files in A1111 | https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor |
| Standalone caption editing | dataset-tag-editor-standalone | 166 | Caption editing without A1111 | https://github.com/toshiaki1729/dataset-tag-editor-standalone |
| Colab trainer fallback | hollowstrawberry/kohya-colab | 797 | Simple cloud notebooks if local setup is inconvenient | https://github.com/hollowstrawberry/kohya-colab |

## Tool Choice

Use this default path:

1. ComfyUI for generation, workflow testing, LoRA loading, ControlNet/OpenPose, and inpainting.
2. kohya_ss GUI for first LoRA training because it is easier to operate than raw scripts.
3. ComfyUI-WD14-Tagger or A1111 tagger for first-pass captions.
4. Dataset Tag Editor or spreadsheet review for manual caption cleanup.

Use AUTOMATIC1111 instead of ComfyUI if the user wants a simpler screen with tabs rather than a node graph.

## Notes

- `gallery-dl` is powerful but should only be used on sources that allow downloading and for material the user is allowed to use.
- Archived tools can still work, but avoid making them the primary recommendation unless needed for compatibility.
- Star counts are not a quality guarantee; prefer active maintenance and compatibility with the user's chosen UI.

