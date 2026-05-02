param(
    [string]$Listen = "127.0.0.1",
    [int]$Port = 7860
)

$KohyaRoot = "C:\Users\dodo\kohya_ss\kohya_ss-master"
$GuiScript = Join-Path $KohyaRoot "gui.ps1"

if (-not (Test-Path $GuiScript)) {
    throw "kohya_ss gui script not found at $GuiScript"
}

Set-Location $KohyaRoot
& $GuiScript --listen $Listen --server_port $Port
