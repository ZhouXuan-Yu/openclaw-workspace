cd C:\Users\ZhouXuan\.openclaw\workspace
git add MEMORY.md memory/
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $date = Get-Date -Format 'yyyy-MM-dd HH:mm'
    git commit -m "memory: health-check + auto-sync $date"
    $remote = git remote 2>$null
    if ($remote) { git push 2>&1 }
    Write-Output "SYNCED"
} else {
    Write-Output "NO_CHANGES"
}
