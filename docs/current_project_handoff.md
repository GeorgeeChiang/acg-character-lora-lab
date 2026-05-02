# 目前專案交接文件

維護註記：本交接文件由 Codex / GPT-5 於 2026-05-02 撰寫。

這份文件是下一個 agent 接手時最快的入口。請在閱讀 `AGENTS.md` 與 `README.md` 後接著閱讀本文件。

## 目前目標

| 項目 | 目前狀態 |
|---|---|
| 專案 | 本機 ACG 角色圖片實驗工作區 |
| 角色 | 朝武芳乃 / Tomotake Yoshino / Asatake Yoshino |
| 作品 | 千恋＊万花 / Senren Banka |
| 主要目標 | 使用本機 ComfyUI workflow 與 SDXL/Pony checkpoint，搭配 LoRA 產生角色圖片 |
| 目標硬體 | Windows 11、AMD 9800X3D、64GB RAM、RTX 5080 16GB VRAM |

## 已完成事項

| 階段 | 狀態 | 備註 |
|---|---|---|
| 專案骨架 | 已完成 | 已有 README、AGENTS、docs、configs、scripts、workflows、templates |
| 圖片收集 | 此角色第一輪已完成 | 原始圖片在 `data/raw/senren_banka_asatake_yoshino/` |
| 資料集審查 | 第一輪已完成 | 已有 selected / rejected 資料夾 |
| 訓練資料集 | 第一輪已完成 | 圖片與 caption 在 `data/train/senren_banka_asatake_yoshino/` |
| 第一版 LoRA 訓練 | 已完成 | v1 已訓練並安裝到 ComfyUI |
| 第二版 LoRA 訓練 | 已完成 | v2 是目前偏好的自訓 LoRA |
| ComfyUI workflow | 已完成 | workflow JSON 在 `workflows/asatake_yoshino_basic_comfyui.json` |
| 知識文件 | 已完成 | 主要筆記在 `docs/06_project_knowledge_notes.md` |
| 專案清理 | 已完成 | 專案 outputs 中的中間 step LoRA 已刪除以節省空間 |

## 重要本機路徑

| 用途 | 路徑 |
|---|---|
| 專案根目錄 | `C:\Users\dodo\Documents\Codex\ACG_AI_picture` |
| 原始圖片 | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\data\raw\senren_banka_asatake_yoshino` |
| 訓練圖片與 caption | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\data\train\senren_banka_asatake_yoshino` |
| 專案 LoRA 輸出 | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\lora` |
| 專案產圖樣本 | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\samples` |
| ComfyUI 根目錄 | `C:\Users\dodo\ComfyUI\ComfyUI-master` |
| ComfyUI checkpoints | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints` |
| ComfyUI LoRAs | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\loras` |
| ComfyUI output | `C:\Users\dodo\ComfyUI\ComfyUI-master\output` |
| 專案 workflow | `C:\Users\dodo\Documents\Codex\ACG_AI_picture\workflows\asatake_yoshino_basic_comfyui.json` |
| ComfyUI 使用者 workflow | `C:\Users\dodo\ComfyUI\ComfyUI-master\user\default\workflows\asatake_yoshino_basic_comfyui.json` |

## ComfyUI 已安裝 Checkpoint

| 檔案 | 類型 | 備註 |
|---|---|---|
| `Illustrious-XL-v0.1.safetensors` | SDXL checkpoint | 專案原本使用的底模 |
| `animagine-xl-4.0.safetensors` | SDXL ACG checkpoint | 已下載，用於比較 |
| `ponyDiffusionV6XL_v6StartWithThisOne.safetensors` | Pony/SDXL checkpoint | 已下載，用於 Pony 風格測試 |
| `NoobAI-XL-v1.1.safetensors` | SDXL ACG checkpoint | 已下載，用於比較 |
| `autismmixSDXL_autismmixPony.safetensors` | Pony/SDXL checkpoint | Civitai 芳乃 LoRA 範例使用的底模 |

## ComfyUI 已安裝 LoRA

| 檔案 | 類型 | Trigger word / 備註 |
|---|---|---|
| `senren_banka_asatake_yoshino_v2.safetensors` | 自訓角色 LoRA | 目前偏好的自訓 LoRA。使用 `sksgirl, asatake yoshino` 加上外觀 tag。 |
| `senren_banka_asatake_yoshino_v1.safetensors` | 自訓角色 LoRA | 較舊版本，保留作比較。 |
| `senren_banka_asatake_yoshino_v1-step00001000.safetensors` | 自訓中間 checkpoint | 只留在 ComfyUI model 資料夾中，不是目前偏好版本。 |
| `senren_banka-tomotake_yoshino-ponyxl.safetensors` | 外部 Civitai LoRA | 使用 `tomotake_yoshino` 與服裝 trigger words。 |
| `Masou_Shizuka_1_nai-000041.safetensors` | 無關 LoRA | 不屬於本角色流程。 |

## 如何啟動 ComfyUI

使用專案腳本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\dodo\Documents\Codex\ACG_AI_picture\scripts\start_comfyui.ps1"
```

預設網址：

```text
http://127.0.0.1:8188/
```

若需要手動啟動，請到：

```text
C:\Users\dodo\ComfyUI\ComfyUI-master
```

執行：

```powershell
.\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8188
```

## 如何關閉 ComfyUI

先檢查 8188 port，再停止對應的 Python 程序。請只停止 ComfyUI 程序，不要關掉其他無關 Python 工作。

```powershell
Get-NetTCPConnection -LocalPort 8188 -State Listen
```

確認 owning process 是 ComfyUI 後，再停止該程序。

## Workflow 注意事項

| 節點 | 用途 |
|---|---|
| `CheckpointLoaderSimple` | 選擇 base checkpoint |
| `LoraLoader` | 選擇角色 LoRA 並設定 strength |
| Positive `CLIPTextEncode` | 放正向 prompt |
| Negative `CLIPTextEncode` | 放 negative prompt |
| `KSampler` | 設定 seed、steps、CFG、sampler、scheduler、denoise |
| `Save Image With Seed` | 建議使用，因為會把 seed 寫入輸出檔名 |

如果輸出檔名沒有 seed，請確認 workflow 是否使用 `Save Image With Seed`，而不是 ComfyUI 內建的 `SaveImage`。

## Prompt 起手式

自訓 v2 LoRA：

```text
masterpiece, best quality, very aesthetic, absurdres, sksgirl, asatake yoshino, 1girl, white hair, blue eyes, long twintails, large round blue eyes, symmetrical eyes, shrine maiden outfit, full body, shrine background, anime illustration
```

Civitai PonyXL LoRA：

```text
score_9, score_8_up, score_7_up, source_anime, tomotake_yoshino, yuzu-soft, white_hair, very_long_hair, blue_eyes, parted_bangs, tomotake_yoshino_miko_clothing, miko_clothing, twintails, hair_ornament, hair_flower, japanese_clothes, white_kimono, red_hakama, hakama_skirt, shrine background
```

Negative prompt：

```text
low quality, worst quality, bad anatomy, bad hands, extra fingers, missing fingers, distorted face, asymmetrical eyes, uneven eyes, different eye size, cross-eyed, squinting, text, watermark, logo
```

## 建議下一步

| 優先度 | 任務 |
|---|---|
| 1 | 用固定 seed 與固定 prompt，測試自訓 v2 LoRA 在不同 checkpoint 上的表現 |
| 2 | 用 `autismmixSDXL_autismmixPony.safetensors` 測試外部 Civitai PonyXL LoRA |
| 3 | 比較角色識別度、髮色、眼型、服裝準確度、手部與背景 |
| 4 | 將結果記錄到 `logs/` 或新增評估 CSV |
| 5 | 若角色識別仍弱，再考慮改善 caption 或用更乾淨的 selected data 重訓 |

## 未經使用者同意不要刪除

| 路徑 / 檔案 | 原因 |
|---|---|
| `data/raw/` | 原始來源圖片 |
| `data/train/` | 訓練圖片與 caption |
| `outputs/lora/senren_banka_asatake_yoshino_v2.safetensors` | 目前偏好的自訓 LoRA |
| `workflows/asatake_yoshino_basic_comfyui.json` | 可重用的 ComfyUI workflow |
| `docs/06_project_knowledge_notes.md` | 主要知識紀錄 |
| `docs/character_ai_pipeline_sop.md` | 主要 SOP |

## 安全邊界

不要協助產生明確色情圖片。可以協助非明確色情的角色相似度、服裝、背景、prompt 結構、模型設定、workflow 除錯與一般產圖品質改善。
