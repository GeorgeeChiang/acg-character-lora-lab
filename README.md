# ACG 角色 LoRA 本機實驗專案

這個專案整理一套本機 ACG 角色 AI 圖流程：從角色參考圖建立資料集、撰寫 caption、訓練角色 LoRA，到使用 ComfyUI 產生新構圖。

預設範圍：所有資料集、LoRA、產圖結果都只作為本機實驗使用，不公開、不外流。

## 專案簡介

| 項目 | 說明 |
|---|---|
| 主要用途 | 訓練與測試 ACG 角色 LoRA，並在本機產生角色圖片 |
| 目前角色 | 朝武芳乃 / Tomotake Yoshino / Asatake Yoshino |
| 主要 UI | ComfyUI |
| 主要訓練工具 | kohya_ss / sd-scripts |
| 主要模型架構 | SDXL / Pony XL 系 checkpoint |
| 目標環境 | Windows 11、RTX 5080 16GB VRAM |

## 技術架構

這個專案的核心概念是：

```txt
角色參考圖
  -> 篩選與整理資料集
  -> 為每張圖撰寫 caption
  -> 使用 SDXL checkpoint 訓練角色 LoRA
  -> 在 ComfyUI 載入 checkpoint + LoRA
  -> 使用 prompt / seed / KSampler 產生圖片
  -> 評估角色相似度並調整
```

| 層級 | 技術 / 檔案 | 作用 |
|---|---|---|
| Base model | SDXL / Pony XL checkpoint | 主要產圖模型，決定整體畫風與模型能力 |
| LoRA | `.safetensors` | 補充角色外觀或風格，不是獨立模型 |
| Caption | `.txt` | 訓練時告訴模型圖片中有哪些角色特徵、服裝、姿勢 |
| Prompt | 文字提示 | 產圖時描述想要的畫面 |
| Negative prompt | 文字提示 | 產圖時描述要避免的問題 |
| Seed | 數字 | 控制隨機起點，方便重現或比較圖片 |
| Workflow | ComfyUI JSON | 保存節點式產圖流程 |

## 使用工具

| 工具 | 類型 | 本專案用途 |
|---|---|---|
| Python | 程式語言 / 執行環境 | 執行 ComfyUI、kohya_ss、資料處理腳本 |
| PyTorch CUDA | GPU 運算套件 | 讓 Python AI 工具使用 NVIDIA GPU 加速 |
| Git | 版本控制 | 管理專案文件、腳本與 workflow |
| ComfyUI | 產圖 UI | 載入 checkpoint、LoRA、prompt、workflow 並產圖 |
| kohya_ss | LoRA 訓練 GUI | 訓練角色 LoRA |
| sd-scripts | LoRA 訓練腳本 | kohya_ss 底層常用訓練工具 |
| Hugging Face | 模型來源 | 下載 checkpoint、LoRA 或相關模型 |
| Civitai | 模型來源 | 下載社群動漫 checkpoint、LoRA 與參考 prompt |
| PowerShell | Windows 命令列 | 啟動服務、檢查 port、搬移檔案、執行腳本 |

## 常見名詞

| 名詞 | 簡短說明 |
|---|---|
| Checkpoint | 主要模型檔，也常稱 base model。ComfyUI 透過 `CheckpointLoaderSimple` 載入。 |
| SDXL | Stable Diffusion XL，常見的高解析產圖模型架構。 |
| Pony XL | SDXL 生態中的社群模型分支，常用於動漫圖。 |
| LoRA | 小型附加模型，用來學角色、服裝或畫風。需要搭配 checkpoint 使用。 |
| Trigger word | 訓練 LoRA 時反覆放在 caption 裡的觸發詞，例如 `sksgirl`。 |
| Caption | 訓練圖片旁的文字描述，通常是一張圖對一個 `.txt`。 |
| Prompt | 產圖時輸入的正向描述。 |
| Negative prompt | 產圖時輸入的反向描述，用來減少壞手、壞臉、浮水印等問題。 |
| Seed | 產圖的隨機起點；固定 seed 可更容易比較不同模型或 prompt。 |
| KSampler | ComfyUI 中實際執行擴散採樣的節點，控制 steps、CFG、sampler、scheduler 等參數。 |
| VAE | 影像編碼/解碼模型，多數 checkpoint 內建可用 VAE。 |
| Workflow | ComfyUI 的節點流程檔，通常是 JSON。 |

## 專案階段

1. 資料收集與整理
   - 輸入：作品名稱、角色名稱、參考網址、使用者提供圖片或截圖。
   - 輸出：乾淨、已篩選、適合訓練的角色圖片資料集。

2. Caption 與訓練準備
   - 為圖片撰寫 caption。
   - 將角色身分、服裝、姿勢、表情等資訊分開描述。

3. LoRA 訓練
   - 使用 kohya_ss / sd-scripts。
   - 以 SDXL 或 Pony XL 系 checkpoint 作為訓練基底。

4. ComfyUI 產圖
   - 載入 checkpoint 與 LoRA。
   - 修改 prompt、negative prompt、seed、KSampler 參數。

5. 評估與迭代
   - 比較角色相似度、髮色、眼睛、服裝、背景、手部品質與 prompt 遵循度。
   - 視結果調整 prompt、換 checkpoint、調整 LoRA strength 或重新訓練。

## 重要文件

- `AGENTS.md`：後續 agent 接手本專案時的入口規則。
- `docs/current_project_handoff.md`：目前專案狀態、模型位置、啟動方式與下一步。
- `docs/06_project_knowledge_notes.md`：本專案累積的知識整理。
- `docs/character_ai_pipeline_sop.md`：從提供原圖到產生 AI 圖的完整 SOP。
- `docs/01_data_collection_pipeline.md`：資料收集與篩選流程。
- `docs/02_open_source_tool_survey.md`：開源工具調查。
- `docs/03_tool_setup_plan.md`：工具安裝與設定規劃。
- `docs/04_generation_test_plan.md`：10 組構圖測試與評估方式。
- `docs/05_agent_handoff.md`：通用 agent 交接格式。
- `configs/project.yaml`：專案預設設定。
- `templates/character_intake.csv`：角色資訊輸入模板。
- `templates/dataset_review_sheet.csv`：圖片審查模板。
- `templates/composition_tests.csv`：構圖測試模板。
- `templates/evaluation_sheet.csv`：產圖評估模板。
- `templates/agent_task_brief.md`：給下一個 agent 的任務描述模板。
- `workflows/`：放 ComfyUI workflow JSON。

## 資料夾結構

```txt
data/raw/        原始候選圖片
data/selected/   已篩選可用圖片
data/rejected/   被剔除圖片
data/train/      最終訓練圖片與 caption
outputs/lora/    訓練完成的 LoRA
outputs/samples/ 產圖測試樣本
configs/         專案與訓練設定
workflows/       ComfyUI workflow JSON
logs/            筆記、訓練 log、評估紀錄
```

## 第一次閱讀建議

如果你是第一次接手：

1. 先讀 `AGENTS.md`。
2. 再讀 `docs/current_project_handoff.md`，了解目前狀態。
3. 想理解整套流程，讀 `docs/character_ai_pipeline_sop.md`。
4. 想查名詞與操作背景，讀 `docs/06_project_knowledge_notes.md`。

目前本專案已完成朝武芳乃的第一輪資料整理、LoRA 訓練與 ComfyUI workflow。後續請先閱讀 `docs/current_project_handoff.md`。
