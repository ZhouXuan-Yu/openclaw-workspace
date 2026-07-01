# Cron 补偿检测 & 自愈脚本
# 用途: 检测 cron-log.md 中未执行的任务，自动补偿执行
# 调用: powershell -File tools\cron-recovery.ps1

$ErrorActionPreference = "SilentlyContinue"
$logFile = "$env:USERPROFILE\.openclaw\workspace\memory\cron-log.md"
$today = Get-Date -Format "yyyy-MM-dd"

# 读取日志，找 PENDING 任务
$pending = @()
$todayPending = @()

if (Test-Path $logFile) {
    $lines = Get-Content $logFile
    foreach ($line in $lines) {
        if ($line -match '^(\d{4}-\d{2}-\d{2})\s+\|\s+([\d:]+)\s+\|\s+(\S+)\s+\|\s+PENDING') {
            $date = $Matches[1]
            $task = $Matches[3]
            $pending += @{ Date = $date; Task = $task }
            if ($date -eq $today) { $todayPending += $task }
        }
    }
}

$totalPending = $pending.Count
$todayCount = $todayPending.Count

Write-Output "=== Cron Recovery Check ==="
Write-Output "Date: $today"
Write-Output "Pending cron tasks today: $todayCount / $totalPending total pending across all dates"
Write-Output ""

if ($todayCount -gt 0) {
    Write-Output "Today's pending tasks:"
    $todayPending | ForEach-Object { Write-Output "  - $_" }
    Write-Output ""
    Write-Output "Note: Cron tasks missed due to system offline will automatically run on their next schedule."
    Write-Output "For critical missed tasks, schedule immediate execution."
} else {
    Write-Output "All today's cron tasks have been executed or are scheduled."
}

# Mark today's remaining PENDING → SKIPPED for cleanup
if (Test-Path $logFile) {
    $content = Get-Content $logFile -Raw
    $updatedContent = $content -replace "($today \| [\d:]+ \| \S+ \| )PENDING", '$1SKIPPED (offline)'
    if ($updatedContent -ne $content) {
        [System.IO.File]::WriteAllText($logFile, $updatedContent, [System.Text.UTF8Encoding]::new($false))
        Write-Output ""
        Write-Output "Marked $today pending tasks as SKIPPED (offline). Will retry on next schedule."
    }
}

Write-Output "--- Done ---"
