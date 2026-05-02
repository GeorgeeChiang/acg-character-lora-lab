param(
    [string]$OutputDir = "C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\lora\senren_banka_asatake_yoshino_v2",
    [string]$LogDir = "C:\Users\dodo\Documents\Codex\ACG_AI_picture\logs\training\senren_banka_asatake_yoshino_v2"
)

$ErrorActionPreference = "Stop"

$KohyaRoot = "C:\Users\dodo\kohya_ss\kohya_ss-master"
$Python = Join-Path $KohyaRoot "venv\Scripts\python.exe"
$Accelerate = Join-Path $KohyaRoot "venv\Scripts\accelerate.exe"
$TrainScript = Join-Path $KohyaRoot "sd-scripts\sdxl_train_network.py"
$DatasetConfig = "C:\Users\dodo\Documents\Codex\ACG_AI_picture\configs\dataset_senren_banka_asatake_yoshino.toml"
$BaseModel = "C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints\Illustrious-XL-v0.1.safetensors"
$OutputName = "senren_banka_asatake_yoshino_v2"

if (-not (Test-Path $Python)) { throw "Missing kohya python: $Python" }
if (-not (Test-Path $Accelerate)) { throw "Missing accelerate launcher: $Accelerate" }
if (-not (Test-Path $TrainScript)) { throw "Missing SDXL train script: $TrainScript" }
if (-not (Test-Path $DatasetConfig)) { throw "Missing dataset config: $DatasetConfig" }
if (-not (Test-Path $BaseModel)) { throw "Missing base model: $BaseModel" }

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

$StdOutLog = Join-Path $LogDir "train.out.log"
$StdErrLog = Join-Path $LogDir "train.err.log"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$Args = @(
    "launch",
    "--num_cpu_threads_per_process", "1",
    $TrainScript,
    "--pretrained_model_name_or_path=$BaseModel",
    "--dataset_config=$DatasetConfig",
    "--output_dir=$OutputDir",
    "--output_name=$OutputName",
    "--save_model_as=safetensors",
    "--network_module=networks.lora",
    "--network_dim=16",
    "--network_alpha=16",
    "--learning_rate=1e-4",
    "--unet_lr=1e-4",
    "--text_encoder_lr=5e-5",
    "--optimizer_type=AdamW8bit",
    "--lr_scheduler=cosine",
    "--max_train_steps=1200",
    "--save_every_n_steps=250",
    "--mixed_precision=fp16",
    "--gradient_checkpointing",
    "--cache_latents",
    "--sdpa",
    "--no_half_vae",
    "--logging_dir=$LogDir"
)

Set-Location $KohyaRoot
Start-Process -WindowStyle Hidden -FilePath $Accelerate -ArgumentList $Args -RedirectStandardOutput $StdOutLog -RedirectStandardError $StdErrLog
