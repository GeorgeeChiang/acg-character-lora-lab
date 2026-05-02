# Agent 交接指南

當使用者要請 Codex、Claude 或其他 agent 接續本 repository 的工作時，可參考本文件。

## 使用者應提供的資訊

- 作品名稱
- 角色名稱
- 可選：角色別名
- 可選：參考網址
- 使用者是否已有本機圖片
- 目前任務階段

## Agent 應該做什麼

1. 先讀 `AGENTS.md`。
2. 再讀 `README.md`、`docs/current_project_handoff.md` 與 `configs/project.yaml`。
3. 確認目前角色輸入資料。
4. 一次只產出下一個明確 artifact。
5. 如果做了重要決策，將紀錄留在 `logs/`。

## 預期 Artifact

- 來源規劃
- 候選圖片審查表
- caption 指引
- 工具候選清單
- 10 組構圖 prompt
- checkpoint 評估表

## Agent 回覆格式

任務完成時應回報：

- 改了什麼
- 檔案在哪裡
- 使用了哪些假設
- 下一步應該做什麼
