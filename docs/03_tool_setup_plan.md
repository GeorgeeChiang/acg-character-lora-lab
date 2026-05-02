# 工具安裝規劃

目標機器：Windows + NVIDIA RTX 5080。

## 必要基礎工具

先安裝：

- NVIDIA 驅動：從 NVIDIA 官方驅動頁下載。
- Git for Windows：https://git-scm.com/download/win
- Python：依各工具需求選版本；A1111 常見需求為 Python 3.10.x。
- 7-Zip：用於解壓縮模型或工具包。

## 產圖工具

推薦：

- ComfyUI Desktop 或 Windows Portable
  - 來源：https://github.com/Comfy-Org/ComfyUI
  - 用途：載入 LoRA、ControlNet/OpenPose、inpaint，以及可重現的節點式測試。

替代：

- AUTOMATIC1111 stable-diffusion-webui
  - 來源：https://github.com/AUTOMATIC1111/stable-diffusion-webui
  - 用途：如果分頁式 UI 比 ComfyUI 節點更容易理解，可改用它。

## 訓練工具

推薦：

- kohya_ss GUI
  - 來源：https://github.com/bmaltais/kohya_ss
  - 用途：第一版 SDXL LoRA 訓練。

進階：

- kohya-ss/sd-scripts
  - 來源：https://github.com/kohya-ss/sd-scripts
  - 用途：需要可重現的命令列訓練時使用。

## Caption 與資料集工具

- ComfyUI-WD14-Tagger
  - 來源：https://github.com/pythongosssss/ComfyUI-WD14-Tagger
  - 放入 ComfyUI 的 `custom_nodes`。

- Dataset Tag Editor
  - 來源：https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor
  - 適合批次編輯大量 caption 檔。

- 試算表審查
  - 使用 `templates/dataset_review_sheet.csv`。
  - 最適合做保留/剔除決策與備註。

## 模型來源

依實驗目標與 UI 選擇模型。

- Hugging Face：常見官方或開源模型檔來源。
- Civitai：常見社群動漫 SDXL 模型與 LoRA 來源。
- ComfyUI 模型資料夾：
  - Checkpoints：`ComfyUI/models/checkpoints/`
  - LoRA：`ComfyUI/models/loras/`
  - ControlNet：`ComfyUI/models/controlnet/`
  - VAE：`ComfyUI/models/vae/`

## 第一次本機設定順序

1. 安裝 NVIDIA 驅動、Git、Python、7-Zip。
2. 安裝 ComfyUI Desktop 或 Windows Portable。
3. 下載一個動漫 SDXL checkpoint 做本機測試。
4. 確認 ComfyUI 能成功產出一張圖。
5. 安裝 ComfyUI-WD14-Tagger。
6. 安裝 kohya_ss GUI。
7. 用小型已整理資料集訓練一個測試 LoRA。
8. 在 ComfyUI 載入 LoRA，執行 10 組 prompt 測試。

## 建議初始 LoRA 設定

以下只是起點，不是最終答案：

- 模型家族：SDXL anime checkpoint
- 解析度：穩定時用 1024，不穩時用 768
- Network dim/rank：16 或 32
- Batch size：1-2
- Learning rate：約 `1e-4`
- Save every：200-300 steps
- Total steps：800-2000
- 測試 checkpoint：800、1000、1200、1500
