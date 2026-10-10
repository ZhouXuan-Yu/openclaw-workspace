$ws = 'C:\Users\ZhouXuan\.openclaw\workspace'
$m = Join-Path $ws 'MEMORY.md'
$lines = (Get-Content $m).Count
Write-Output ("MEMORY.md lines: " + $lines)

Write-Output '--- topic item counts ---'
Get-ChildItem (Join-Path $ws 'memory\topics') -Filter *.md | ForEach-Object {
    $c = (Get-Content $_.FullName | Where-Object { $_ -match '^\s*[-*] |^\s*\d+\. ' }).Count
    "{0}: {1}" -f $_.Name, $c
}

Write-Output '--- pending markers ---'
$mark = [char]0x5F85 + [char]0x786E + [char]0x8BA4
$p = (Select-String -Path (Join-Path $ws 'memory\topics\*.md'), $m -Pattern $mark -SimpleMatch -ErrorAction SilentlyContinue).Count
Write-Output ("pending: " + $p)

Write-Output '--- dailies in last 7 days ---'
$cut = (Get-Date).AddDays(-7)
$d = Get-ChildItem (Join-Path $ws 'memory\daily') -Filter *.md | Where-Object { $_.LastWriteTime -ge $cut }
Write-Output ("recent_dailies_7d: " + $d.Count)

Write-Output '--- topics stale >7d ---'
$stale7 = Get-ChildItem (Join-Path $ws 'memory\topics') -Filter *.md | Where-Object { $_.LastWriteTime -lt $cut }
Write-Output ("stale_7d: " + $stale7.Count)
$stale7 | ForEach-Object { "  " + $_.Name + " " + $_.LastWriteTime.ToString('yyyy-MM-dd') }
