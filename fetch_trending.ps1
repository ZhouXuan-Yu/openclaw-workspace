$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
foreach ($p in @(@("daily","https://github.com/trending?since=daily"), @("weekly","https://github.com/trending?since=weekly"))) {
    $name = $p[0]; $url = $p[1]
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 60 -Headers @{ "User-Agent" = "Mozilla/5.0" }
        $r.Content | Out-File -Encoding utf8 ("raw_" + $name + ".html")
        Write-Output ("$name OK " + $r.Content.Length)
    } catch {
        Write-Output ("$name FAIL " + $_.Exception.Message)
    }
}
