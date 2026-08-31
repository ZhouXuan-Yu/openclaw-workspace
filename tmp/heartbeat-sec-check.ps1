$ErrorActionPreference = 'SilentlyContinue'
$d = Get-MpComputerStatus
Write-Output ("Defender RealTime=" + $d.RealTimeProtectionEnabled + " AV=" + $d.AntivirusEnabled)
Write-Output "---0.0.0.0 LISTEN---"
netstat -ano | Select-String '0.0.0.0:.*LISTENING' | ForEach-Object { (($_ -split '\s+') | Where-Object { $_ -match '^0\.0\.0\.0:' }) -replace '0.0.0.0:', '' } | Sort-Object -Unique | ForEach-Object { $_ }
Write-Output "---LISTEN COUNT---"
(netstat -ano | Select-String '0.0.0.0:.*LISTENING').Count
Write-Output "---TOP CPU---"
Get-Process | Sort-Object CPU -Descending | Select-Object -First 6 Name, CPU, @{n='MEM_MB'; e={[math]::Round($_.WorkingSet64/1MB)}} | Format-Table -AutoSize | Out-String
Write-Output "---GIT---"
Set-Location C:\Users\ZhouXuan\.openclaw\workspace
git log --oneline -5
