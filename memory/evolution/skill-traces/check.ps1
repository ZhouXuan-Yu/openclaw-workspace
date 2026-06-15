Get-ChildItem 'C:\Users\ZhouXuan\.openclaw\workspace\memory\evolution\skill-traces\' -File -Filter '*.jsonl' | ForEach-Object {
    $f = $_
    $lines = Get-Content $f.FullName
    Write-Output ("FILE: " + $f.Name + " LINES: " + $lines.Count + " SIZE: " + $f.Length)
    foreach ($l in $lines) {
        try {
            $null = $l | ConvertFrom-Json
            Write-Output '  LINE_OK'
        } catch {
            Write-Output ('  LINE_BAD: ' + $l.Substring(0, [Math]::Min(80, $l.Length)))
        }
    }
}
