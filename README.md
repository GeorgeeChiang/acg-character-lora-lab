# ACG 角色 LoRA 本機實驗專案

這個專案用來整理「從 ACG 角色參考圖建立資料集、訓練角色 LoRA、再用 ComfyUI 產生新構圖」的本機流程。

預設範圍：所有資料集、LoRA、產圖結果都只作為本機實驗使用，不公開、不外流。

## 專案階段

1. 資料收集與整理
   - 輸入：作品名稱、角色名稱、參考網址、使用者提供圖片或截圖。
   - 輸出：乾淨、已篩選、適合訓練的角色圖片資料集。

2. 工具選擇
   - 優先使用活躍、開源、可本機執行的工具。
   - 將資料整理、caption、LoRA 訓練、產圖、姿勢控制與修圖流程分開處理。

3. 訓練準備
   - 建議方向：SDXL 動漫 checkpoint + 每個角色一個 LoRA。
   - 建議訓練工具：kohya_ss GUI 或 kohya-ss/sd-scripts。

4. 產圖流程
   - 建議 UI：ComfyUI。
   - 使用 LoRA 控制角色識別度，prompt 控制場景/表情/服裝，必要時再用 ControlNet/OpenPose 或 inpaint 修正。

5. 評估
   - 用固定 prompt、固定 seed、固定參數比較不同 checkpoint 或 LoRA。
   - 評估角色相似度、構圖彈性、姿勢控制、破圖、過擬合等問題。

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

## 推薦第一次執行方式

先在 `templates/character_intake.csv` 填入一個角色。從 30-80 張候選圖片開始，篩到 25-50 張乾淨圖片，訓練第一版 SDXL LoRA，再用 4-6 個 checkpoint 做比較。

目前本專案已完成朝武芳乃的第一輪資料整理、LoRA 訓練與 ComfyUI workflow。後續請先閱讀 `docs/current_project_handoff.md`。
