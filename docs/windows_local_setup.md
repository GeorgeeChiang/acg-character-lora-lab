# Windows 本機設定

本 repository 已設定為 Windows 11 本機 LoRA 工作流程。

## 已完成

- 已安裝 Python 3.10.11
- 已安裝 7-Zip
- 已安裝 ComfyUI，並有可使用 CUDA 的 venv
- 已安裝 kohya_ss，並有可使用 CUDA 的 venv
- 已將 `Illustrious-XL-v0.1` SDXL checkpoint 下載到 ComfyUI models 資料夾

## 仍可繼續確認

- 啟動 ComfyUI 並確認可開啟
- 啟動 kohya_ss GUI 並確認可開啟
- 執行或重跑 LoRA 訓練
- 執行 10 組構圖測試
- 若第一版結果過擬合，再調整 caption 或資料集大小

## 啟動輔助腳本

- `scripts/start_comfyui.ps1`
- `scripts/start_kohya_gui.ps1`

## 建議工作路徑

| 工具 | 路徑 |
|---|---|
| Python | `%LOCALAPPDATA%\\Programs\\Python\\Python310\\python.exe` |
| 7-Zip | `%ProgramFiles%\\7-Zip\\7z.exe` |
| ComfyUI | `C:\\Users\\dodo\\ComfyUI\\ComfyUI-master` |
| kohya_ss | `C:\\Users\\dodo\\kohya_ss\\kohya_ss-master` |
| Base checkpoint | `C:\\Users\\dodo\\ComfyUI\\ComfyUI-master\\models\\checkpoints\\Illustrious-XL-v0.1.safetensors` |
