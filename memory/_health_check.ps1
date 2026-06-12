Get-ChildItem 'C:\Users\ZhouXuan\.openclaw\workspace\memory\topics\*.md' | ForEach-Object {
    $lines = (Get-Content $_.FullName -Encoding utf8).Count
    $pending = (Select-String -Path $_.FullName -Pattern '待确认' -SimpleMatch -Encoding utf8).Count
    Write-Output "$($_.Name)|$($_.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))|$lines|$pending"
}
