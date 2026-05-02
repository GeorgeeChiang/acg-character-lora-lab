# 開源工具調查

調查日期：2026-05-01。GitHub stars 為約略數字，會隨時間變動。

## 推薦工具組合

| 用途 | 專案 | Stars | 使用理由 | 連結 |
|---|---:|---:|---|---|
| 產圖 workflow | ComfyUI | 111k | 節點式流程，LoRA、ControlNet、inpaint 生態完整 | https://github.com/Comfy-Org/ComfyUI |
| 較簡單的產圖 UI | AUTOMATIC1111 WebUI | 162k | 成熟、擴充多，對初學者較直覺 | https://github.com/AUTOMATIC1111/stable-diffusion-webui |
| LoRA 訓練腳本 | kohya-ss/sd-scripts | 7k | SD/SDXL/FLUX LoRA 訓練核心腳本 | https://github.com/kohya-ss/sd-scripts |
| LoRA 訓練 GUI | bmaltais/kohya_ss | GitHub 頁面顯示不同，屬高使用量 GUI | kohya scripts 的圖形介面，較容易操作 | https://github.com/bmaltais/kohya_ss |
| 圖片下載工具 | gallery-dl | 18k | 支援多種圖庫來源；只用於允許下載的來源 | https://github.com/mikf/gallery-dl |
| ControlNet 參考 | lllyasviel/ControlNet | 33.8k | 原始 ControlNet 實作與概念來源 | https://github.com/lllyasviel/ControlNet |
| A1111 ControlNet 外掛 | Mikubill/sd-webui-controlnet | 17.8k | AUTOMATIC1111 的 ControlNet 外掛 | https://github.com/Mikubill/sd-webui-controlnet |
| ComfyUI WD14 caption | ComfyUI-WD14-Tagger | 1.2k | 在 ComfyUI 內產生 booru 風格 tag | https://github.com/pythongosssss/ComfyUI-WD14-Tagger |
| A1111 WD14 caption | stable-diffusion-webui-wd14-tagger | 1.4k | 可用但已封存；若可行，優先找維護中替代品 | https://github.com/toriato/stable-diffusion-webui-wd14-tagger |
| Caption 批次編輯 | stable-diffusion-webui-dataset-tag-editor | 729 | 在 A1111 中批次編輯 caption `.txt` | https://github.com/toshiaki1729/stable-diffusion-webui-dataset-tag-editor |
| 獨立 caption 編輯器 | dataset-tag-editor-standalone | 166 | 不依賴 A1111 的 caption 編輯器 | https://github.com/toshiaki1729/dataset-tag-editor-standalone |
| Colab 訓練備案 | hollowstrawberry/kohya-colab | 797 | 本機設定不方便時，可用雲端 notebook 備案 | https://github.com/hollowstrawberry/kohya-colab |

## 工具選擇

預設路線：

1. 使用 ComfyUI 做產圖、workflow 測試、LoRA 載入、ControlNet/OpenPose 與 inpaint。
2. 使用 kohya_ss GUI 做第一版 LoRA 訓練，因為比純命令列腳本容易操作。
3. 使用 ComfyUI-WD14-Tagger 或 A1111 tagger 做第一版 caption。
4. 使用 Dataset Tag Editor 或試算表做 caption 人工修正。

如果使用者想要比節點圖更簡單的分頁式 UI，可以用 AUTOMATIC1111 取代 ComfyUI。

## 注意事項

- `gallery-dl` 很強，但只應用於允許下載的來源，且只下載使用者有權使用的素材。
- 已封存工具仍可能可用，但除非相容性需要，不要把它設為主要推薦。
- Stars 不是品質保證；應優先考慮維護狀態與和目前 UI 的相容性。
