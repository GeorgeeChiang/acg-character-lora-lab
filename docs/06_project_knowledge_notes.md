# ACG 角色 AI 圖專案知識整理

本文整理本專案從「提供角色原圖」到「訓練 LoRA、在 ComfyUI 產圖」期間累積的概念、工具、檔案位置與操作知識。這份文件偏向查詢筆記；完整 SOP 請搭配 `docs/character_ai_pipeline_sop.md`。

## 1. 專案目標與目前狀態

| 項目 | 內容 |
|---|---|
| 目標 | 建立本機 ACG 角色圖生成流程，從角色原圖整理、caption、LoRA 訓練，到 ComfyUI 產圖 |
| 角色 | 朝武芳乃 / Tomotake Yoshino / Asatake Yoshino |
| 作品 | 千恋＊万花 / Senren Banka |
| 硬體 | Windows 11、AMD 9800X3D、64GB RAM、RTX 5080 16GB VRAM |
| 主要產圖工具 | ComfyUI |
| 主要訓練工具 | kohya_ss / sd-scripts |
| 目前自訓 LoRA | `senren_banka_asatake_yoshino_v2.safetensors` |
| 目前外部 LoRA | `senren_banka-tomotake_yoshino-ponyxl.safetensors` |

## 2. 整體流程概念

| 階段 | 輸入 | 輸出 | 意義 | 主要技術 |
|---|---|---|---|---|
| 收集圖片 | 官方圖、截圖、使用者提供圖片 | 原始圖片集 | 建立角色特徵來源 | 手動整理、圖片下載、資料夾管理 |
| 篩選圖片 | 原始圖片集 | 可訓練圖片集 | 排除非目標角色、低品質、重複或干擾太強的圖片 | 人工審查、檔案分類 |
| Caption | 可訓練圖片 | 圖片旁的 `.txt` 說明檔 | 告訴訓練器每張圖包含哪些角色特徵、服裝、構圖 | WD tagger、BLIP、手動修正 |
| LoRA 訓練 | 圖片 + caption + base model | `.safetensors` LoRA | 學到「這個角色」的外觀概念 | kohya_ss、sd-scripts、LoRA |
| 產圖 | checkpoint + LoRA + prompt + seed | PNG 圖片 | 依照文字提示生成新圖 | ComfyUI、Stable Diffusion、KSampler |
| 評估與調整 | 產出的圖片 | 下一輪參數或 prompt | 比較角色相似度、服裝、眼睛、髮色、背景、手部等問題 | 固定 seed 對照、換 checkpoint、調整 LoRA strength |

## 2-1. 需要安裝的軟體與程式語言

這個專案分成「只產圖」與「重新訓練 LoRA」兩種使用情境。若你已經有 checkpoint 和 LoRA，只要開 ComfyUI 產圖，安裝項目會少很多；若要重新訓練，才需要 kohya_ss 與訓練相關套件。

### 必裝：只要產圖就需要

| 項目 | 類型 | 用途 | 本專案狀態 / 備註 |
|---|---|---|---|
| Windows 11 | 作業系統 | 本機執行環境 | 本專案以 Windows 11 規劃 |
| NVIDIA 顯示卡驅動 | GPU 驅動 | 讓 PyTorch / ComfyUI 使用 RTX 5080 | 需要支援目前顯卡與 CUDA |
| Python | 程式語言 / 執行環境 | 執行 ComfyUI、kohya_ss、資料處理腳本 | 建議穩定版 Python 3.10.x；ComfyUI 目前使用 venv |
| Git | 版本控制 / 下載工具 | 下載 ComfyUI、kohya_ss、custom nodes | 開源工具常用 GitHub 發布 |
| ComfyUI | 產圖 UI | 載入 checkpoint、LoRA、prompt、workflow 產生圖片 | 主要產圖工具，網址通常是 `http://127.0.0.1:8188/` |
| PyTorch CUDA 版 | Python 深度學習套件 | 實際使用 GPU 推論 | 通常由 ComfyUI 安裝流程處理 |
| Checkpoint 檔案 | AI 模型檔 | 主要產圖模型 | 放在 `ComfyUI\models\checkpoints\` |
| LoRA 檔案 | AI 模型附加檔 | 套用角色或風格 | 放在 `ComfyUI\models\loras\` |

### 訓練 LoRA 才需要

| 項目 | 類型 | 用途 | 備註 |
|---|---|---|---|
| kohya_ss | LoRA 訓練 GUI | 設定訓練參數並啟動 LoRA 訓練 | 只產圖不需要開 |
| sd-scripts | 訓練腳本 | kohya_ss 底層常用訓練工具 | Python 專案 |
| accelerate | Python 套件 | 管理訓練加速與 GPU 設定 | kohya_ss 會用到 |
| bitsandbytes / xformers / triton 類套件 | Python / CUDA 加速套件 | 降低 VRAM 或加速訓練 | Windows 上相容性要以實際安裝版本為準 |
| Caption 工具 | 圖片標註工具 | 自動產生圖片 tag 或描述 | 可用 WD tagger、BLIP 類工具，再人工修正 |
| 訓練資料資料夾 | 圖片 + `.txt` caption | LoRA 訓練輸入 | 每張圖旁邊要有對應 caption |

### 可選工具

| 項目 | 類型 | 用途 | 什麼時候需要 |
|---|---|---|---|
| Hugging Face CLI / `hf` | 模型下載工具 | 從 Hugging Face 下載 checkpoint、LoRA | 大檔案或需要登入時好用 |
| Civitai API / 網頁下載 | 模型下載來源 | 下載 Civitai 上的 ACG checkpoint 或 LoRA | 有些模型需要登入或 API key |
| 7-Zip | 壓縮工具 | 解壓縮資料集或工具包 | 下載壓縮檔時需要 |
| VS Code | 編輯器 | 看 Markdown、JSON、設定檔、caption | 可選，但很方便 |
| PowerShell | 命令列 | 啟動服務、檢查 port、搬檔案 | Windows 內建 |
| ComfyUI Manager | ComfyUI custom node 管理器 | 安裝/管理 custom nodes | 可選，手動安裝也可以 |
| Upscale model | 放大模型 | 例如 `4xUltrasharp_4xUltrasharpV10.pt` | 只有需要放大流程時才需要 |

### 本專案實際用到的程式語言 / 檔案格式

| 名稱 | 用在哪裡 | 你需要會到什麼程度 |
|---|---|---|
| Python | ComfyUI、kohya_ss、訓練腳本、自訂 ComfyUI node | 基本上由工具執行；除錯時會看錯誤訊息 |
| PowerShell | 啟動/停止 ComfyUI、檢查服務、下載檔案、搬檔案 | 會複製指令執行即可 |
| JSON | ComfyUI workflow | workflow 檔案格式；通常用 UI 編輯 |
| Markdown | 專案文件與 SOP | 用來記錄流程、知識與交接 |
| YAML | 專案設定 | `configs/project.yaml` 這類設定檔 |
| TXT caption | LoRA 訓練標註 | 每張訓練圖對應一份 caption |
| CSV | 圖片審查表、測試表 | 用來整理資料集與評估結果 |

### 最小安裝組合

| 目標 | 最少需要 |
|---|---|
| 只用現有 LoRA 產圖 | Python、Git、ComfyUI、PyTorch CUDA、checkpoint、LoRA |
| 換不同 checkpoint 產圖 | 上述項目 + 新 checkpoint 檔案 |
| 使用外部 LoRA | 上述項目 + 外部 LoRA 檔案 + 該 LoRA 的 trigger words |
| 重新訓練角色 LoRA | Python、Git、NVIDIA 驅動、kohya_ss、sd-scripts、PyTorch CUDA、訓練圖片、caption、base checkpoint |
| 重建整個專案流程 | ComfyUI、kohya_ss、模型檔、資料夾結構、SOP、workflow JSON、訓練/產圖紀錄 |

## 3. 重要名詞

| 名詞 | 解釋 |
|---|---|
| Checkpoint | 主要的生成模型，也叫 base model。ComfyUI 的 `CheckpointLoaderSimple` 會載入它。 |
| SDXL checkpoint | 以 Stable Diffusion XL 架構為基礎的 checkpoint。LoRA 必須跟模型架構相容。 |
| LoRA | 小型附加模型，用來補強角色、畫風、服裝或特定概念。它不是完整模型，需要搭配 checkpoint 使用。 |
| `.safetensors` | 常見模型檔格式，比舊式 pickle 類型安全，checkpoint 和 LoRA 都可能是這個副檔名。 |
| Caption | 訓練圖片旁的文字描述，通常是 `.txt`。LoRA 會從「圖片 + caption」學習。 |
| Trigger word | 在 caption 中反覆出現、用來喚起 LoRA 概念的詞。例如本專案自訓 LoRA 使用 `sksgirl`。 |
| Prompt | 產圖時輸入的正向描述，告訴模型想要什麼畫面。 |
| Negative prompt | 產圖時輸入的反向描述，告訴模型避免什麼錯誤或風格。 |
| Seed | 產圖起始雜訊的編號。同模型、同 LoRA、同 prompt、同參數、同 seed 時，結果通常可接近重現。 |
| KSampler | ComfyUI 中負責實際擴散採樣的節點，控制 seed、steps、CFG、sampler、scheduler、denoise。 |
| VAE | 負責 latent 與圖片之間的轉換。多數 SDXL checkpoint 已內建可用 VAE。 |
| Upscaler | 放大圖片的模型或方法，不是基礎產圖必需，但高解析輸出會用到。 |

## 4. Checkpoint 與 LoRA 的關係

| 類型 | 作用 | 放置資料夾 | 例子 |
|---|---|---|---|
| Checkpoint | 主要模型，決定整體知識、畫風、架構 | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints\` | `Illustrious-XL-v0.1.safetensors`、`ponyDiffusionV6XL_v6StartWithThisOne.safetensors` |
| LoRA | 疊加在 checkpoint 上，補強角色或風格 | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\loras\` | `senren_banka_asatake_yoshino_v2.safetensors` |
| VAE | 圖像編碼/解碼 | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\vae\` | 可選，多數 checkpoint 可先用內建 |
| Embedding | 文字反轉概念檔 | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\embeddings\` | 本專案目前不依賴 |
| Upscale model | 放大圖用 | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\upscale_models\` | `4xUltrasharp_4xUltrasharpV10.pt` |

重點：LoRA 不是獨立模型。產圖時一定是「checkpoint + LoRA + prompt」一起作用。

## 5. 本專案使用過或討論過的模型

| 模型 | 類型 | 來源定位 | 用途 |
|---|---|---|---|
| `Illustrious-XL-v0.1.safetensors` | SDXL checkpoint | 下載回來的 ACG base model | 原本訓練與產圖用底模 |
| `animagine-xl-4.0.safetensors` | SDXL checkpoint | Hugging Face | ACG 產圖比較用 |
| `ponyDiffusionV6XL_v6StartWithThisOne.safetensors` | Pony/SDXL checkpoint | Hugging Face | Pony 系產圖比較用 |
| `NoobAI-XL-v1.1.safetensors` | SDXL checkpoint | Hugging Face | ACG 產圖比較用 |
| `autismmixSDXL_autismmixPony.safetensors` | Pony/SDXL checkpoint | Civitai / Hugging Face 可見 | Civitai 芳乃 LoRA 範例使用底模 |
| `senren_banka_asatake_yoshino_v2.safetensors` | LoRA | 本專案自訓 | 使用 `sksgirl` 觸發自訓芳乃概念 |
| `senren_banka-tomotake_yoshino-ponyxl.safetensors` | LoRA | Civitai 版本 658019 | 外部 PonyXL 芳乃 LoRA |

## 6. 官方模型與社群模型

| 問題 | 答案 |
|---|---|
| Animagine XL、Pony XL、NoobAI XL 是官方 SDXL 嗎？ | 不是 Stability AI 官方模型，而是社群基於 SDXL 或相關架構再訓練、合併或微調的 checkpoint。 |
| 那它們可以用 SDXL LoRA 嗎？ | 通常 SDXL/Pony/Illustrious 生態的 LoRA 可以互相嘗試，但效果不保證相同。 |
| SD3.5、FLUX、Qwen Image 之類可以直接用目前 LoRA 嗎？ | 通常不行。架構不同時 LoRA 需要重新訓練或使用對應架構的 LoRA。 |
| 想換底模麻煩嗎？ | 若仍是 SDXL/Pony/Illustrious 類 checkpoint，通常只是下載到 checkpoints 資料夾，ComfyUI 改選 checkpoint，再測 prompt。 |

## 7. Trigger word 與 `sksgirl`

`sksgirl` 不是特殊參數，也不是 LoRA 檔案裡的開關。它是在訓練 caption 中放進去的自訂 trigger word。

訓練 caption 可能像這樣：

```text
sksgirl, asatake yoshino, 1girl, white hair, blue eyes, long twintails, shrine maiden outfit
```

模型在訓練時多次看到 `sksgirl` 和芳乃圖片一起出現，就會把這個詞與角色外觀綁在一起。

| 詞 | 來源 | 作用 |
|---|---|---|
| `sksgirl` | 自訓 LoRA caption 中的人造 trigger | 穩定喚起本專案自訓 LoRA 的角色概念 |
| `asatake yoshino` | caption 中可放的角色名稱 | 輔助語意，但可能被 tokenizer 切開，穩定性較差 |
| `tomotake_yoshino` | Civitai PonyXL LoRA 的 trigger | 喚起外部 LoRA 的芳乃概念 |
| `white hair, blue eyes, twintails` | 一般 prompt 特徵詞 | 補強模型能理解的外觀特徵 |

本專案自訓 LoRA 建議：

```text
sksgirl, asatake yoshino, white hair, blue eyes, long twintails
```

Civitai 外部 LoRA 建議：

```text
tomotake_yoshino, yuzu-soft, white_hair, very_long_hair, blue_eyes, parted_bangs
```

## 8. Prompt 語言與寫法

| 問題 | 結論 |
|---|---|
| Prompt 必須英文嗎？ | 不一定，但 SDXL ACG 模型通常對英文與 Danbooru tag 風格最穩。 |
| 中文可以嗎？ | 可以試，但角色、服裝、構圖通常英文 tag 更準。 |
| 為什麼 prompt 不一定完全照做？ | 產圖是機率模型，不是繪圖指令執行器。模型知識、LoRA 強度、seed、CFG、底模和訓練資料都會影響結果。 |
| 同角色不同服裝會影響嗎？ | 會。訓練資料服裝越混雜，LoRA 越容易把角色特徵和服裝混在一起。caption 要把服裝寫清楚。 |

## 9. Prompt 範例

### 自訓 LoRA：巫女服

```text
masterpiece, best quality, very aesthetic, absurdres, sksgirl, asatake yoshino, 1girl, white hair, blue eyes, long twintails, large round blue eyes, symmetrical eyes, shrine maiden outfit, full body, shrine background, anime illustration
```

### 自訓 LoRA：學生服

```text
masterpiece, best quality, very aesthetic, absurdres, sksgirl, asatake yoshino, 1girl, white hair, blue eyes, high ponytail, large round blue eyes, symmetrical eyes, school uniform, green jacket, red ribbon, pleated skirt, classroom background, anime illustration
```

### Pony 系 LoRA：巫女服

```text
score_9, score_8_up, score_7_up, source_anime, tomotake_yoshino, yuzu-soft, white_hair, very_long_hair, blue_eyes, parted_bangs, tomotake_yoshino_miko_clothing, miko_clothing, twintails, hair_ornament, hair_flower, japanese_clothes, white_kimono, red_hakama, hakama_skirt, shrine background
```

### Pony 系 LoRA：學生服

```text
score_9, score_8_up, score_7_up, source_anime, tomotake_yoshino, yuzu-soft, white_hair, very_long_hair, blue_eyes, parted_bangs, tomotake_yoshino_school_uniform, school_uniform, ponytail, high_ponytail, bow, hair_bow, white_sailor_collar, blue_jacket, red_ribbon, blue_skirt, black_pantyhose, classroom background
```

### Negative prompt

```text
low quality, worst quality, bad anatomy, bad hands, extra fingers, missing fingers, distorted face, asymmetrical eyes, uneven eyes, different eye size, cross-eyed, squinting, text, watermark, logo
```

Pony 系可以額外加：

```text
score_4, score_3, score_2, score_1, source_pony, source_furry, source_cartoon, 3d, monochrome
```

## 10. KSampler 參數

| 參數 | 意義 | 建議 |
|---|---|---|
| Seed | 初始雜訊編號，用來重現或比較結果 | 比較模型時固定 seed；想多樣化時 randomize |
| Steps | 去雜訊迭代次數 | 通常 20-35；太低細節不足，太高不一定更好 |
| CFG | prompt 服從程度 | 常用 5-7；太高可能僵硬或破圖 |
| Sampler | 採樣演算法 | `euler_ancestral`、`dpmpp_2m` 常用 |
| Scheduler | 採樣排程 | `normal`、`karras` 常用 |
| Denoise | 影像改動強度 | txt2img 用 1.0；img2img 或修圖可用 0.3-0.6 |

固定 seed 的意思：如果你喜歡某張圖的構圖，可以把 seed 固定，之後只微調 prompt、LoRA strength 或 checkpoint，觀察差異。

## 11. ComfyUI 基本操作

| 動作 | 說明 |
|---|---|
| 開 ComfyUI | 執行 ComfyUI 的 `main.py`，預設本專案使用 `http://127.0.0.1:8188/` |
| 載入 workflow | 在 ComfyUI 左側工作流清單載入 `asatake_yoshino_basic_comfyui` |
| 選 checkpoint | 在 `CheckpointLoaderSimple` 節點選主模型 |
| 選 LoRA | 在 `LoraLoader` 節點選角色 LoRA |
| 寫 prompt | 在正向 `CLIPTextEncode` 節點填入 |
| 寫 negative | 在負向 `CLIPTextEncode` 節點填入 |
| 設 seed | 在 `KSampler` 節點設定 |
| 產圖 | 按 Queue / 執行 |
| 看輸出 | 圖片會進 ComfyUI 的 `output` 資料夾 |

本專案工作流位置：

```text
C:\Users\dodo\Documents\Codex\ACG_AI_picture\workflows\asatake_yoshino_basic_comfyui.json
```

ComfyUI 使用者工作流位置：

```text
C:\Users\dodo\ComfyUI\ComfyUI-master\user\default\workflows\asatake_yoshino_basic_comfyui.json
```

## 12. 檔名包含 seed

本專案新增過一個自訂 ComfyUI node：

```text
Save Image With Seed
```

它會讀取 KSampler 的 seed，並把 seed 加到輸出檔名中，例如：

```text
asatake_yoshino_manual_seed12345_00001_.png
```

如果產出的圖沒有 seed，通常是以下原因：

| 可能原因 | 處理 |
|---|---|
| 最後節點仍是內建 `SaveImage` | 換成 `Save Image With Seed` |
| 載到舊 workflow | 重新載入 `asatake_yoshino_basic_comfyui` |
| ComfyUI 沒重啟 | 重啟 ComfyUI 讓 custom node 載入 |

## 13. 目前常用檔案位置

| 類型 | 位置 |
|---|---|
| 專案根目錄 | `C:\Users\dodo\Documents\Codex\ACG_AI_picture` |
| 原始圖片 | `data\raw\` |
| 訓練資料 | `data\train\` |
| 訓練輸出 LoRA | `outputs\lora\` |
| 產圖樣本 | `outputs\samples\` |
| 訓練 log | `logs\training\` |
| ComfyUI checkpoint | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints\` |
| ComfyUI LoRA | `C:\Users\dodo\ComfyUI\ComfyUI-master\models\loras\` |
| ComfyUI output | `C:\Users\dodo\ComfyUI\ComfyUI-master\output\` |

## 14. ComfyUI 與 kohya_ss 差異

| 工具 | 用途 | 什麼時候需要開 |
|---|---|---|
| ComfyUI | 產圖、測試 checkpoint、套 LoRA、調 prompt | 只要產圖就開它 |
| kohya_ss | 訓練 LoRA、重新訓練、調訓練參數 | 只有要訓練或重訓 LoRA 才開 |

如果你已經有模型和 LoRA，只要產圖，通常只需要開 ComfyUI。

## 15. LoRA 訓練時間與訓練經驗

| 版本 | 大約時間 | 備註 |
|---|---|---|
| v1 | 約 27 分鐘 | 第一輪訓練 |
| v2 | 約 19 分鐘 | 後續選定版本 |

訓練時間會受以下因素影響：

| 因素 | 影響 |
|---|---|
| 圖片數量 | 越多越久 |
| resolution | 1024 比 768 慢 |
| batch size | 越大越吃 VRAM |
| network dim / rank | 越大 LoRA 容量越大，也可能更慢 |
| epoch / steps | 訓練越久越慢，也可能過擬合 |

## 16. 使用外部 LoRA 的判斷方式

以下以 Civitai `Tomotake Yoshino (朝武芳乃) - Senren * Banka` 版本 658019 為例。

| 項目 | 該 LoRA 資訊 |
|---|---|
| 檔名 | `senren_banka-tomotake_yoshino-ponyxl.safetensors` |
| 類型 | LoRA |
| Base model | Pony / SDXL |
| 主要 trigger | `tomotake_yoshino` |
| 範例底模 | `autismmixSDXL_autismmixPony.safetensors` |
| LoRA strength | 範例多為 1.0 |

若 ComfyUI 缺東西，通常看三個地方：

| 檢查項目 | 資料夾 | 判斷 |
|---|---|---|
| LoRA 是否存在 | `models\loras\` | 沒有就下載 LoRA |
| 範例 checkpoint 是否存在 | `models\checkpoints\` | 沒有也可先用同生態替代模型 |
| Upscaler 是否存在 | `models\upscale_models\` | 只有高解析放大流程需要 |

## 17. 模型下載來源

| 來源 | 適合下載 | 備註 |
|---|---|---|
| Hugging Face | checkpoint、LoRA、資料集 | 來源較容易追蹤，常可用 CLI 或直接連結下載 |
| Civitai | ACG checkpoint、LoRA、範例圖與 prompt | 常見動漫模型來源，有些模型可能需要登入或 API key |
| Tensor.Art / SeaArt | 線上模型與 LoRA 展示 | 有些是轉載，下載與來源要再確認 |

下載後通常不用安裝，只要放進 ComfyUI 對應資料夾並重新整理或重啟。

## 18. 成人內容與限制

本專案可以記錄一般模型使用概念，但不把流程設計成產生明確色情內容。若 prompt 涉及成人或性行為，模型、介面或平台可能因為訓練資料、過濾器、模型傾向、negative prompt、checkpoint 風格而不照做。

可安全處理的方向包括：

| 方向 | 說明 |
|---|---|
| 角色相似度改善 | 髮色、眼睛、髮型、服裝、臉型 |
| 一般服裝 | 巫女服、學生服、休閒服、睡衣 |
| 背景與構圖 | 神社、教室、夜景、全身、半身、坐姿 |
| 品質修正 | 眼睛不對稱、手指錯誤、臉部變形、浮水印 |

## 19. 常見問題

| 問題 | 可能原因 | 處理 |
|---|---|---|
| 髮色不對 | LoRA 沒吃到、prompt 權重不足、底模偏移 | 確認 LoRA 已載入，加強 `white hair`，換 seed 或 checkpoint |
| 眼睛怪 | 模型常見臉部錯誤、解析度不足、negative 不夠 | 加 `symmetrical eyes`、`large round blue eyes`，negative 加 `asymmetrical eyes` |
| 服裝不準 | 訓練資料服裝混雜或 prompt 不完整 | 使用該 LoRA 的服裝 trigger，例如 `tomotake_yoshino_miko_clothing` |
| prompt 沒照做 | 模型機率性、LoRA 和 checkpoint 知識衝突 | 降低/提高 LoRA strength，換 seed，拆短 prompt |
| 換 checkpoint 後角色不像 | LoRA 與該底模相容性差 | 用同生態模型，或針對新底模重訓 |
| 圖片介面看不到舊輸出 | ComfyUI 只顯示目前節點/當前 session 產物 | 到 `ComfyUI-master\output` 或專案 `outputs\samples` 找 |

## 20. 推薦的測試方式

比較 checkpoint 或 LoRA 時，不要一次改太多東西。

| 測試項目 | 固定 | 只改 |
|---|---|---|
| 比較 checkpoint | prompt、seed、LoRA、尺寸、KSampler | checkpoint |
| 比較 LoRA strength | prompt、seed、checkpoint、尺寸 | LoRA strength |
| 比較 prompt | checkpoint、LoRA、seed、KSampler | prompt |
| 找好構圖 | checkpoint、LoRA、prompt | seed |

建議每次測試建立一個資料夾，資料夾名稱包含角色、時間與序號，方便回查。

```text
朝武芳乃_20260502153045_001
```

## 21. 一句話心智模型

| 概念 | 記法 |
|---|---|
| Checkpoint | 會畫圖的大腦 |
| LoRA | 補充記憶或專門技能 |
| Prompt | 這次要畫什麼 |
| Negative prompt | 這次不要畫什麼 |
| Seed | 這次圖的隨機起點 |
| KSampler | 把雜訊一步步變成圖片的引擎 |
| Caption | 訓練時告訴模型圖片裡有什麼 |
| Trigger word | 訓練後喚起特定 LoRA 概念的暗號 |
