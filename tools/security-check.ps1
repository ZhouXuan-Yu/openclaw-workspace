# Security check script for cron job
# Avoids $_ escaping issues with exec -Command

$results = @()

# 1. Defender status
try {
    $mp = Get-MpComputerStatus
    $results += @{
        Check = "Defender"
        Status = if ($mp.RealTimeProtectionEnabled) { "OK" } else { "FAIL" }
        Detail = "RealTime=$($mp.RealTimeProtectionEnabled) Antivirus=$($mp.AntivirusEnabled)"
    }
} catch {
    $results += @{ Check = "Defender"; Status = "ERROR"; Detail = $_.Exception.Message }
}

# 2. 0.0.0.0 listening ports
try {
    $ports = netstat -an | Select-String '0.0.0.0.*LISTENING'
    $portCount = ($ports | Measure-Object).Count
    $portList = ($ports -replace '\s+', ' ' | ForEach-Object { $_.Trim() }) -join '; '
    $results += @{
        Check = "0.0.0.0 Ports"
        Status = if ($portCount -gt 10) { "WARN" } else { "OK" }
        Detail = "$portCount ports: $portList"
    }
} catch {
    $results += @{ Check = "0.0.0.0 Ports"; Status = "ERROR"; Detail = $_.Exception.Message }
}

# 3. Get-Process top CPU
try {
    $procs = Get-Process | Where-Object { $_.CPU -gt 0 } | Sort-Object CPU -Descending | Select-Object -First 12
    $procList = ($procs | ForEach-Object { "$($_.Name) (CPU:$([math]::Round($_.CPU,1)) MEM:$([math]::Round($_.WorkingSet64/1MB,1))MB)" }) -join ', '
    $results += @{
        Check = "Top Processes"
        Status = "OK"
        Detail = $procList
    }
} catch {
    $results += @{ Check = "Top Processes"; Status = "ERROR"; Detail = $_.Exception.Message }
}

# 4. Ollama binding
try {
    $ollama = netstat -ano | Select-String "11434.*LISTENING"
    $ollamaDetail = ($ollama -replace '\s+', ' ' | ForEach-Object { $_.Trim() }) -join ' | '
    $results += @{
        Check = "Ollama Binding"
        Status = "CHECK"
        Detail = $ollamaDetail
    }
} catch {
    $results += @{ Check = "Ollama Binding"; Status = "ERROR"; Detail = $_.Exception.Message }
}

# 5. Git recent commits
try {
    Push-Location "C:\Users\ZhouXuan\.openclaw\workspace"
    $commits = git log --oneline -5 2>&1
    Pop-Location
    $commitStr = ($commits -join '; ')
    $results += @{
        Check = "Git Commits"
        Status = "OK"
        Detail = $commitStr
    }
} catch {
    $results += @{ Check = "Git Commits"; Status = "ERROR"; Detail = $_.Exception.Message }
}

# Output as JSON for easy parsing
$results | ConvertTo-Json -Compress
