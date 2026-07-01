# Quick security check script
Write-Host "=== PROCESSES (Top 15 by CPU) ==="
Get-Process | Sort-Object CPU -Descending | Select-Object Name, Id, CPU -First 15 | Format-Table -AutoSize

Write-Host "=== Ollama Check ==="
try {
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 3 -ErrorAction Stop
    Write-Host "Ollama OK on 127.0.0.1 - Models: $($r.models.Count)"
} catch {
    Write-Host "Ollama: FAIL - $($_.Exception.Message)"
}
