# Health check helper
$topicsDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
$dailyDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\daily"

Write-Host "=== TOPIC FILES ==="
Get-ChildItem "$topicsDir\*.md" | ForEach-Object {
    $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
    $w = $_.LastWriteTime
    $age = [math]::Floor(((Get-Date) - $w).TotalDays)
    Write-Host "$($_.Name): $lines lines, last $($w.ToString('yyyy-MM-dd')), age ${age}d"
}

Write-Host "=== PENDING MARKERS [待确认] ==="
Get-ChildItem "$topicsDir\*.md" | ForEach-Object {
    $count = (Select-String -Path $_.FullName -Pattern '待确认' | Measure-Object).Count
    Write-Host "$($_.Name): $count [待确认]"
}

Write-Host "=== RECENT DAILIES ==="
$cutoff = (Get-Date).AddDays(-7)
$files = Get-ChildItem "$dailyDir\*.md" | Where-Object { $_.LastWriteTime -ge $cutoff }
Write-Host "最近7天日志: $($files.Count) files"
$files | ForEach-Object { Write-Host "  $($_.LastWriteTime.ToString('yyyy-MM-dd')) $($_.Name)" }
