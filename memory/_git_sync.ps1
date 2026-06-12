Set-Location "C:\Users\ZhouXuan\.openclaw\workspace"
git add MEMORY.md memory/
$hasChanges = $true
try { git diff --cached --quiet; $hasChanges = ($LASTEXITCODE -ne 0) } catch { $hasChanges = $true }
if ($hasChanges) {
    $date = Get-Date -Format 'yyyy-MM-dd HH:mm'
    git commit -m "memory: health-check + auto-sync $date"
    $remote = git remote 2>$null
    if ($remote) { git push 2>&1 }
} else {
    Write-Output "NO_CHANGES"
}
