$files = Get-ChildItem 'C:\Users\ZhouXuan\.openclaw\workspace\memory\daily\*.md' -ErrorAction SilentlyContinue
$recent = $files | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
Write-Output "Total:$($files.Count)"
Write-Output "Recent:$($recent.Count)"
$recent | ForEach-Object { Write-Output $_.Name }
$old = $files | Where-Object { $_.LastWriteTime -le (Get-Date).AddDays(-7) }
if ($old.Count -gt 0) {
    Write-Output "Stale:"
    $old | ForEach-Object { Write-Output "  $($_.Name) ($($_.LastWriteTime.ToString('yyyy-MM-dd')))" }
}
