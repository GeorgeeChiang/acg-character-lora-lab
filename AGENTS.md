# Agent 指引

這個 repository 是本機 ACG 角色圖與 LoRA 訓練實驗工作區。

維護註記：本指引由 Codex / GPT-5 於 2026-05-02 更新。

## 請先閱讀

1. `README.md`
2. `docs/current_project_handoff.md`
3. `docs/06_project_knowledge_notes.md`
4. `docs/character_ai_pipeline_sop.md`
5. `configs/project.yaml`
6. `docs/01_data_collection_pipeline.md`
7. `docs/03_tool_setup_plan.md`
8. `docs/04_generation_test_plan.md`
9. `templates/character_intake.csv`
10. `templates/dataset_review_sheet.csv`

## 核心規則

- 將所有內容視為本機實驗用途。
- 新增檔案預設使用 ASCII；若文件本來就是繁體中文，可使用 UTF-8 繁體中文。
- 修改要小而明確，方便下一個 agent 接手。
- 產出放在 `outputs/`，紀錄與決策放在 `logs/`。
- 不要假設專案永遠只服務單一作品或角色；流程應可套用到其他 ACG 角色。
- 不要協助產生明確色情圖像；可以協助角色相似度、服裝、背景、構圖、模型設定與工作流除錯。

## 標準工作流程

1. 讀取角色輸入資料，確認作品名稱與角色名稱。
2. 建立來源規劃。
3. 收集候選圖片，或請使用者提供本機圖片。
4. 審查圖片並剔除弱圖。
5. 為最終資料集撰寫或修正 caption。
6. 訓練第一版 LoRA。
7. 執行 10 組構圖測試。
8. 記錄結果與下一輪調整方向。

## 任務完成時必須留下

- 這次改了什麼
- 結果放在哪裡
- 下一個 agent 應該接著做什麼
- 使用了哪些假設
- 仍有哪些未知或風險

## 良好交接格式

- 使用的輸入
- 變更或新增的檔案
- 做出的決策
- 尚未解決的問題
- 下一步
