$files = Get-ChildItem 'C:\Users\ZhouXuan\.openclaw\workspace\memory\topics\*.md'
foreach ($f in $files) {
    $lines = (Get-Content $f.FullName).Count
    $pending = (Select-String -Path $f.FullName -Pattern '待确认' -SimpleMatch).Count
    Write-Output "$($f.Name)|$lines|$pending|$($f.LastWriteTime)"
}
