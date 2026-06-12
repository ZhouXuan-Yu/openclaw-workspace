[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$topicDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
$dailyDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\daily"

# MEMORY.md line count
$memLines = (Get-Content "C:\Users\ZhouXuan\.openclaw\workspace\MEMORY.md" -Encoding UTF8).Count
Write-Output "MEMORY_LINES:$memLines"

# Topic files
$files = Get-ChildItem "$topicDir\*.md"
$pendingTotal = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw -Encoding UTF8
    $entries = ([regex]::Matches($content, '(?m)^[\-\*]\s|^\d+\.\s')).Count
    $pending = ([regex]::Matches($content, '\u5F85\u786E\u8BA4')).Count
    $pendingTotal += $pending
    $age = ((Get-Date) - $f.LastWriteTime).Days
    $ts = $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm')
    Write-Output "TOPIC:$($f.Name)|$entries|$pending|$age|$ts"
}
Write-Output "PENDING_TOTAL:$pendingTotal"

# Daily logs in last 7 days
$dailyFiles = Get-ChildItem "$dailyDir\*.md" -ErrorAction SilentlyContinue
$recentCount = 0
if ($dailyFiles) {
    $recentCount = ($dailyFiles | Where-Object { $_.LastWriteTime -ge (Get-Date).AddDays(-7) }).Count
}
$totalDaily = 0
if ($dailyFiles) { $totalDaily = $dailyFiles.Count }
Write-Output "DAILY:$recentCount|$totalDaily"
