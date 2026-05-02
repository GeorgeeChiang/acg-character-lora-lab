param(
    [string]$ComfyUrl = "http://127.0.0.1:8188",
    [string]$BaseCheckpointPath = "C:\Users\dodo\ComfyUI\ComfyUI-master\models\checkpoints\Illustrious-XL-v0.1.safetensors",
    [string]$PromptCsv = "C:\Users\dodo\Documents\Codex\ACG_AI_picture\logs\composition_tests_senren_banka_asatake_yoshino.csv",
    [string]$OutputRoot = "C:\Users\dodo\Documents\Codex\ACG_AI_picture\outputs\samples\senren_banka_asatake_yoshino",
    [string]$CharacterName = "朝武芳乃",
    [string]$RunSerial = "01",
    [string]$LoraName = "senren_banka_asatake_yoshino_v2.safetensors",
    [double]$LoraStrength = 1.0,
    [int]$MaxTestId = 10,
    [int]$Steps = 30,
    [double]$Cfg = 6.0,
    [int]$Seed = 12345,
    [int]$Width = 1024,
    [int]$Height = 1024,
    [int]$BatchSize = 1,
    [string]$SamplerName = "dpmpp_2m",
    [string]$Scheduler = "karras"
)

$ErrorActionPreference = "Stop"

function ConvertTo-ComfyNodeRef {
    param([int]$NodeId, [int]$OutputIndex)
    return @($NodeId.ToString(), $OutputIndex)
}

function New-ComfyWorkflow {
    param(
        [string]$Prompt,
        [string]$NegativePrompt,
        [string]$CheckpointName,
        [string]$LoraFileName,
        [string]$FilenamePrefix,
        [int]$SeedValue,
        [int]$StepCount,
        [double]$CfgScale,
        [int]$ImageWidth,
        [int]$ImageHeight,
        [int]$BatchCount,
        [double]$LoraScale,
        [string]$Sampler,
        [string]$Sched
    )

    $workflow = [ordered]@{
        "1" = @{
            class_type = "CheckpointLoaderSimple"
            inputs = @{
                ckpt_name = $CheckpointName
            }
        }
        "2" = @{
            class_type = "LoraLoader"
            inputs = @{
                model = (ConvertTo-ComfyNodeRef 1 0)
                clip = (ConvertTo-ComfyNodeRef 1 1)
                lora_name = $LoraFileName
                strength_model = $LoraScale
                strength_clip = $LoraScale
            }
        }
        "3" = @{
            class_type = "CLIPTextEncode"
            inputs = @{
                text = $Prompt
                clip = (ConvertTo-ComfyNodeRef 2 1)
            }
        }
        "4" = @{
            class_type = "CLIPTextEncode"
            inputs = @{
                text = $NegativePrompt
                clip = (ConvertTo-ComfyNodeRef 2 1)
            }
        }
        "5" = @{
            class_type = "EmptyLatentImage"
            inputs = @{
                width = $ImageWidth
                height = $ImageHeight
                batch_size = $BatchCount
            }
        }
        "6" = @{
            class_type = "KSampler"
            inputs = @{
                seed = $SeedValue
                steps = $StepCount
                cfg = $CfgScale
                sampler_name = $Sampler
                scheduler = $Sched
                denoise = 1
                model = (ConvertTo-ComfyNodeRef 2 0)
                positive = (ConvertTo-ComfyNodeRef 3 0)
                negative = (ConvertTo-ComfyNodeRef 4 0)
                latent_image = (ConvertTo-ComfyNodeRef 5 0)
            }
        }
        "7" = @{
            class_type = "VAEDecode"
            inputs = @{
                samples = (ConvertTo-ComfyNodeRef 6 0)
                vae = (ConvertTo-ComfyNodeRef 1 2)
            }
        }
        "8" = @{
            class_type = "SaveImage"
            inputs = @{
                filename_prefix = $FilenamePrefix
                images = (ConvertTo-ComfyNodeRef 7 0)
            }
        }
    }

    return $workflow
}

function Invoke-ComfyPrompt {
    param(
        [string]$ServerUrl,
        [hashtable]$Workflow
    )

    $payload = @{
        prompt = $Workflow
        client_id = "codex-senren-banka"
    } | ConvertTo-Json -Depth 20

    return Invoke-RestMethod -Method Post -Uri "$ServerUrl/prompt" -ContentType "application/json" -Body $payload
}

function Wait-ComfyHistory {
    param(
        [string]$ServerUrl,
        [string]$PromptId,
        [int]$TimeoutSeconds = 1800
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $history = Invoke-RestMethod -Method Get -Uri "$ServerUrl/history/$PromptId"
            if ($history.PSObject.Properties.Name -contains $PromptId) {
                return $history.$PromptId
            }
        } catch {
            Start-Sleep -Seconds 3
            continue
        }
        Start-Sleep -Seconds 3
    }

    throw "Timed out waiting for ComfyUI history for prompt $PromptId"
}

function Get-ComfyOutputImages {
    param(
        [object]$HistoryItem
    )

    $images = @()
    if ($HistoryItem.outputs) {
        foreach ($node in $HistoryItem.outputs.PSObject.Properties.Value) {
            if ($node.images) {
                $images += @($node.images)
            }
        }
    }
    return $images
}

if (-not (Test-Path $BaseCheckpointPath)) { throw "Checkpoint not found: $BaseCheckpointPath" }
if (-not (Test-Path $PromptCsv)) { throw "Prompt CSV not found: $PromptCsv" }

$server = $ComfyUrl.TrimEnd("/")
$checkpointName = Split-Path $BaseCheckpointPath -Leaf
$runStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$runName = "{0}_{1}_{2}" -f $CharacterName, $runStamp, $RunSerial
$runOutputRoot = Join-Path $OutputRoot $runName
New-Item -ItemType Directory -Force -Path $runOutputRoot | Out-Null

$negativePrompt = "low quality, worst quality, bad anatomy, extra fingers, missing fingers, distorted face, asymmetrical eyes, uneven eyes, different eye size, cross-eyed, squinting, text, watermark, logo"
$rows = Import-Csv $PromptCsv | Where-Object { $_.test_id -and [int]$_.test_id -le $MaxTestId }

$results = @()

foreach ($row in $rows) {
    $testId = [int]$row.test_id
    $prompt = $row.prompt
    $seedValue = $Seed + $testId
    $filenamePrefix = "senren_banka_asatake_yoshino_{0:00}_seed{1}" -f $testId, $seedValue
    $workflow = New-ComfyWorkflow -Prompt $prompt -NegativePrompt $negativePrompt -CheckpointName $checkpointName -LoraFileName $LoraName -FilenamePrefix $filenamePrefix -SeedValue $seedValue -StepCount $Steps -CfgScale $Cfg -ImageWidth $Width -ImageHeight $Height -BatchCount $BatchSize -LoraScale $LoraStrength -Sampler $SamplerName -Sched $Scheduler

    Write-Host ("Queueing test {0}: {1}" -f $testId, $row.name)
    $response = Invoke-ComfyPrompt -ServerUrl $server -Workflow $workflow
    $promptId = $response.prompt_id
    if (-not $promptId) { throw "ComfyUI did not return a prompt_id for test $testId" }

    $historyItem = Wait-ComfyHistory -ServerUrl $server -PromptId $promptId
    $images = Get-ComfyOutputImages -HistoryItem $historyItem
    if (-not $images -or $images.Count -eq 0) {
        throw "No output images returned for test $testId (prompt $promptId)"
    }

    $copied = @()
    foreach ($img in $images) {
        $url = "$server/view?filename=$([uri]::EscapeDataString($img.filename))&subfolder=$([uri]::EscapeDataString($img.subfolder))&type=$([uri]::EscapeDataString($img.type))"
        $ext = [IO.Path]::GetExtension($img.filename)
        if (-not $ext) { $ext = ".png" }
        $dest = Join-Path $runOutputRoot ("{0}{1}" -f $filenamePrefix, $ext)
        Invoke-WebRequest -Uri $url -OutFile $dest
        $copied += $dest
    }

    $results += [pscustomobject]@{
        test_id = $testId
        name = $row.name
        prompt_id = $promptId
        seed = $seedValue
        output_files = ($copied -join ";")
    }
}

$resultsFileName = "{0}_results.csv" -f $runName
$resultsPath = Join-Path $runOutputRoot $resultsFileName
$results | Export-Csv -NoTypeInformation -Path $resultsPath -Encoding UTF8
Write-Host "Saved results to $resultsPath"
