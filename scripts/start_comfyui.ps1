param(
    [string]$Listen = "127.0.0.1",
    [int]$Port = 8188
)

$ComfyRoot = "C:\Users\dodo\ComfyUI\ComfyUI-master"
$Python = Join-Path $ComfyRoot "venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "ComfyUI venv python not found at $Python"
}

Set-Location $ComfyRoot
& $Python main.py --listen $Listen --port $Port
