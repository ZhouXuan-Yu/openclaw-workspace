$cut = (Get-Date).AddDays(-7)
$files = Get-ChildItem "C:\Users\ZhouXuan\.openclaw\workspace\memory\daily\*.md" | Sort-Object LastWriteTime -Descending
Write-Host "---RECENT-7D---"
$files | Where-Object { $_.LastWriteTime -gt $cut } | ForEach-Object { Write-Host ("{0}  {1}" -f $_.Name, $_.LastWriteTime) }
Write-Host "---TOTAL---"
Write-Host $files.Count
