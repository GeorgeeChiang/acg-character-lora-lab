# 角色 AI 圖產生流程 SOP

適用角色：千戀＊萬花 / 朝武芳乃  
目的：從使用者提供原圖開始，整理資料、訓練角色 LoRA，最後在 ComfyUI 產生可調 prompt 的 AI 圖。

## 1. 流程總覽

| 階段 | 輸入 | 輸出 | 這階段在做什麼 | 使用技術 / 工具 |
|---|---|---|---|---|
| 1. 收集原圖 | 使用者提供圖片、網頁圖源、既有截圖 | `data/raw/senren_banka_asatake_yoshino/` | 收集角色相關圖片，先不做品質判斷，只保留原始來源 | 瀏覽器、PowerShell、檔案整理 |
| 2. 人工篩選 | `data/raw/...` | `data/selected/...`、`data/rejected/...` | 挑出確定是朝武芳乃、品質可用、角色臉與髮型清楚的圖 | 人工檢查、資料夾分類 |
| 3. 建立訓練資料 | `data/selected/...` | `data/train/...` | 將圖片整理成訓練格式，通常是一張圖片搭配一個同名 `.txt` caption | kohya_ss / sd-scripts 訓練格式 |
| 4. Caption 標註 | 訓練圖片 | 每張圖對應的 `.txt` caption | 描述圖片中的角色特徵、服裝、姿勢、背景，讓訓練知道該學什麼、不該死背什麼 | Tagger、自動 caption、人工修正 |
| 5. LoRA 訓練 | `data/train/...`、基礎模型 | `.safetensors` LoRA 檔 | 在既有 SDXL 模型上學習「朝武芳乃」這個角色特徵 | kohya_ss、sd-scripts、PyTorch、CUDA |
| 6. Checkpoint 評估 | 訓練中輸出的多個 LoRA checkpoint | 選定最佳 LoRA | 比較不同訓練步數的角色相似度、泛化能力、畫面穩定度 | ComfyUI、抽樣測試、人工評估 |
| 7. ComfyUI 工作流 | 基礎模型、LoRA、prompt | 可操作的 ComfyUI workflow | 建立可在 UI 修改 prompt、按下運行產圖的節點流程 | ComfyUI、LoraLoader、KSampler |
| 8. 產圖測試 | workflow、prompt、seed | PNG 圖片 | 依照角色、服裝、背景需求產出圖片，並觀察髮色、眼睛、服裝、構圖是否正確 | ComfyUI、SDXL、LoRA |
| 9. 回饋調整 | 產圖結果、使用者意見 | 新 prompt、負面 prompt、必要時新 LoRA | 針對錯誤修正，例如髮色錯、眼睛怪、服裝不準、背景不足 | prompt engineering、重新篩圖、再訓練 |
| 10. 最終產出 | 穩定 workflow、LoRA、prompt | 可重複產圖的本機流程 | 使用者自行打開 ComfyUI，修改 prompt 並產生新圖 | ComfyUI UI、本機 GPU |

## 2. 各階段輸入輸出意義

| 階段 | 輸入的意義 | 輸出的意義 |
|---|---|---|
| 收集原圖 | 盡量取得角色在不同角度、表情、服裝下的素材 | 原始資料池，之後可以反覆篩選 |
| 人工篩選 | 排除其他角色、低畫質、遮臉、嚴重裁切、重複圖 | 保留較乾淨的角色學習資料 |
| 建立訓練資料 | 將篩選後圖片轉成訓練程式能讀的格式 | 圖片與 caption 一一對應 |
| Caption 標註 | 告訴模型哪些元素是圖片內容 | 幫助 LoRA 分辨角色特徵、服裝、背景 |
| LoRA 訓練 | 用角色資料微調模型的一小部分權重 | 產生可插拔的角色 LoRA |
| Checkpoint 評估 | 比較不同訓練步數的結果 | 選出最像角色、但不過度死背的版本 |
| ComfyUI 工作流 | 把模型、LoRA、prompt、採樣器接成圖形流程 | 使用者可直接在 UI 操作 |
| 產圖測試 | 測試 LoRA 與 prompt 的配合程度 | 產出圖片與問題清單 |
| 回饋調整 | 使用者指出不符合角色的地方 | 改 prompt、改負面 prompt、必要時重訓 |
| 最終產出 | 穩定可用的設定 | 可長期重複使用的角色 AI 圖流程 |

## 3. 專有名詞解釋

| 名詞 | 解釋 | 在本專案中的用途 |
|---|---|---|
| AI 產圖 | 使用生成式模型依照文字或圖片條件產生新圖片 | 產生朝武芳乃風格的插畫 |
| SDXL | Stable Diffusion XL，較新的 Stable Diffusion 架構 | 作為基礎產圖模型架構 |
| Illustrious XL | 一個偏向二次元 / ACG 風格的 SDXL 模型 | 本專案使用的基礎模型 |
| Base model / 基礎模型 | 原本就會畫圖的大模型 | LoRA 需要掛在基礎模型上使用 |
| LoRA | Low-Rank Adaptation，小型微調權重檔 | 用來讓模型學會朝武芳乃角色特徵 |
| `.safetensors` | 常見的模型權重檔格式，較安全、載入快 | LoRA 與 checkpoint 的檔案格式 |
| Checkpoint | 模型或 LoRA 在某個訓練步數保存下來的版本 | 比較 250、500、750、1000、final 哪個較好 |
| Caption | 圖片的文字標註 | 告訴訓練程式圖片中有什麼元素 |
| Tag / Token | 模型能理解的短文字標籤 | 例如 `white hair`、`blue eyes`、`shrine maiden outfit` |
| Trigger word | LoRA 的觸發詞 | 本專案使用 `sksgirl, asatake yoshino` 觸發角色 |
| Prompt | 正向提示詞，描述想要產生什麼 | 控制角色、服裝、姿勢、背景、畫風 |
| Negative Prompt | 反向提示詞，描述不想要什麼 | 減少壞手、歪眼、文字、水印、低品質 |
| Seed | 隨機種子，決定圖片初始雜訊 | 固定 seed 可以重現相近構圖 |
| KSampler | ComfyUI 中負責採樣產圖的核心節點 | 控制 seed、steps、cfg、sampler、scheduler |
| Steps | 採樣步數 | 越高通常越慢，常用 25 到 35 |
| CFG | Prompt 服從度 | 太低不聽 prompt，太高可能僵硬或崩圖 |
| Sampler | 採樣演算法 | 本專案常用 `dpmpp_2m` |
| Scheduler | 採樣排程 | 本專案常用 `karras` |
| Denoise | 去雜訊強度 | 文生圖通常用 `1.0` |
| Batch size | 一次產生幾張圖 | VRAM 16GB 先用 1 最穩 |
| ComfyUI | 節點式 AI 產圖工具 | 使用者實際修改 prompt、按運行產圖的介面 |
| Node / 節點 | ComfyUI 中的一個功能方塊 | 例如載入模型、載入 LoRA、編碼 prompt、儲存圖片 |
| Workflow | ComfyUI 節點連線組成的流程 | 本專案使用 `asatake_yoshino_basic_comfyui` |
| LoraLoader | ComfyUI 載入 LoRA 的節點 | 載入 `senren_banka_asatake_yoshino_v2.safetensors` |
| CLIPTextEncode | 將 prompt 轉成模型可理解條件的節點 | 分別處理 positive 與 negative prompt |
| EmptyLatentImage | 建立初始 latent 圖像尺寸的節點 | 設定 1024 x 1024、batch size |
| VAEDecode | 將 latent 轉回可看的圖片 | KSampler 後接到 Save Image |
| Save Image With Seed | 本專案新增的 ComfyUI custom node | 儲存圖片時自動把 seed 加進檔名 |
| kohya_ss | LoRA 訓練 GUI 工具 | 訓練角色 LoRA |
| sd-scripts | kohya_ss 底層常用訓練腳本 | 實際執行 SDXL LoRA 訓練 |
| CUDA | NVIDIA GPU 運算平台 | 讓 RTX 5080 加速訓練與產圖 |
| VRAM | 顯示卡記憶體 | 影響可用解析度、batch size、訓練設定 |
| Overfitting / 過擬合 | 模型過度記住訓練圖，泛化變差 | LoRA 太像原圖、姿勢難改時可能發生 |
| Underfitting / 欠擬合 | 模型學得不夠，角色不像 | LoRA 強度不足或訓練步數不夠時可能發生 |
| Inference / 推論 | 使用已訓練模型產生圖片 | 在 ComfyUI 按「運行」產圖 |
| Training / 訓練 | 用資料調整模型權重 | 用 kohya_ss 訓練 LoRA |

## 4. 本專案使用環境

| 類別 | 內容 | 說明 |
|---|---|---|
| 作業系統 | Windows 11 | 本機執行 |
| CPU | AMD 9800X3D | 輔助資料處理 |
| RAM | 64GB | 足夠處理資料集與多工具 |
| GPU | RTX 5080 16GB VRAM | 主要用於 LoRA 訓練與 ComfyUI 產圖 |
| Python | Python 3.10 | ComfyUI / kohya_ss 常見穩定版本 |
| 訓練工具 | kohya_ss、sd-scripts | 開源工具 |
| 產圖工具 | ComfyUI | 開源節點式 UI |
| 基礎模型 | `Illustrious-XL-v0.1.safetensors` | SDXL 二次元風格模型 |
| 角色 LoRA | `senren_banka_asatake_yoshino_v2.safetensors` | 本專案訓練成果 |

## 5. 目前重要檔案位置

| 路徑 | 意義 |
|---|---|
| `data/raw/senren_banka_asatake_yoshino/` | 原始圖片 |
| `data/selected/senren_banka_asatake_yoshino/` | 已篩選可用圖片 |
| `data/rejected/senren_banka_asatake_yoshino/` | 已排除圖片 |
| `data/train/senren_banka_asatake_yoshino/` | 訓練用圖片與 caption |
| `outputs/lora/...` | LoRA 訓練輸出 |
| `outputs/samples/...` | 批次測試產圖輸出 |
| `logs/...` | 測試 prompt、訓練紀錄、交接紀錄 |
| `workflows/asatake_yoshino_basic_comfyui.json` | 專案內保存的 ComfyUI workflow |
| `comfyui_custom_nodes/save_image_with_seed/` | 自動把 seed 加進檔名的 custom node |
| `C:\Users\dodo\ComfyUI\ComfyUI-master\output` | ComfyUI UI 產圖輸出 |

## 6. 自行產圖操作流程

| 步驟 | 操作 |
|---|---|
| 1 | 開啟 ComfyUI：`http://127.0.0.1:8188/` |
| 2 | 左側工作流載入 `asatake_yoshino_basic_comfyui` |
| 3 | 確認 LoRA 節點是 `senren_banka_asatake_yoshino_v2.safetensors` |
| 4 | 修改 `Positive Prompt` |
| 5 | 必要時修改 `Negative Prompt` |
| 6 | 在 `KSampler` 調整 seed、steps、cfg |
| 7 | 按右上角「運行」 |
| 8 | 圖片輸出到 ComfyUI `output` 資料夾，檔名會包含 seed |

## 7. 建議 Prompt 起點

```text
sksgirl, asatake yoshino, white hair, blue eyes, long twintails, large round blue eyes, symmetrical eyes, centered gaze, 1girl, full body, shrine maiden outfit, shrine background, ACG illustration
```

## 8. 建議 Negative Prompt 起點

```text
low quality, worst quality, bad anatomy, extra fingers, missing fingers, distorted face, asymmetrical eyes, uneven eyes, different eye size, cross-eyed, squinting, text, watermark, logo
```

## 9. 常見問題與調整

| 問題 | 可能原因 | 調整方式 |
|---|---|---|
| 髮色不對 | prompt 權重不足或模型偏移 | 加強 `white hair`、保留 LoRA strength 1.0 |
| 眼睛怪 | 角色臉部細節不穩 | 加 `symmetrical eyes`，negative 加 `asymmetrical eyes` |
| 不像角色 | LoRA 沒觸發或強度太低 | 保留 `sksgirl, asatake yoshino`，LoRA strength 調 1.0 到 1.1 |
| 圖太僵硬 | LoRA 或 CFG 太強 | LoRA strength 降到 0.8 到 0.9，CFG 降到 5.5 |
| prompt 不聽話 | 描述太多或互相衝突 | 簡化 prompt，先固定角色再加服裝與背景 |
| 想重現某張圖 | seed 被 randomize | 記下 seed，改成 fixed，再小幅改 prompt |
| 檔名沒有 seed | 用到舊 SaveImage 節點 | 確認最後節點是 `Save Image With Seed` |

## 10. 最短流程

| 流程 |
|---|
| 收集原圖 -> 篩選 -> caption -> LoRA 訓練 -> checkpoint 評估 -> ComfyUI workflow -> 產圖 -> 回饋調整 -> 穩定產出 |
