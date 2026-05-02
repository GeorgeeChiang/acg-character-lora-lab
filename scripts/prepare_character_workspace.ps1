param(
    [string]$CharacterId = "senren_banka_asatake_yoshino"
)

$root = Split-Path -Parent $PSScriptRoot
$rawDir = Join-Path $root "data\raw\$CharacterId"
$selectedDir = Join-Path $root "data\selected\$CharacterId"
$rejectedDir = Join-Path $root "data\rejected\$CharacterId"
$trainDir = Join-Path $root "data\train\$CharacterId"
$reviewCsv = Join-Path $root "logs\dataset_review_sheet_$CharacterId.csv"
$intakeCsv = Join-Path $root "logs\character_intake_$CharacterId.csv"

$dirs = @($rawDir, $selectedDir, $rejectedDir, $trainDir)
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}

$imageExtensions = @(".png", ".jpg", ".jpeg", ".webp", ".bmp")
$rawImages = Get-ChildItem -Path $rawDir -File -ErrorAction SilentlyContinue |
    Where-Object { $imageExtensions -contains $_.Extension.ToLowerInvariant() } |
    Sort-Object Name

if (-not (Test-Path $reviewCsv)) {
    @("file_name,source,keep,reject_reason,crop_needed,caption_status,identity_score,pose_value,notes") |
        Set-Content -Path $reviewCsv -Encoding ASCII
}

$existingRows = @()
if (Test-Path $reviewCsv) {
    $existingRows = Import-Csv $reviewCsv
}

$known = @{}
foreach ($row in $existingRows) {
    if ($row.file_name) {
        $known[$row.file_name] = $true
    }
}

foreach ($img in $rawImages) {
    if (-not $known.ContainsKey($img.Name)) {
        Add-Content -Path $reviewCsv -Value "$($img.Name),,needs_review,,,pending,,,"
    }
}

$summary = [ordered]@{
    character_id = $CharacterId
    raw_images   = $rawImages.Count
    review_csv   = $reviewCsv
    intake_csv   = $intakeCsv
    status       = if ($rawImages.Count -gt 0) { "ready_for_triage" } else { "waiting_for_images" }
}

$summary | ConvertTo-Json -Depth 3
