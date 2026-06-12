$topicDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
Get-ChildItem "$topicDir\*.md" | ForEach-Object {
    $name = $_.Name
    $content = Get-Content $_.FullName -Encoding UTF8
    $lines = ($content | Where-Object { $_ -match '^\s*[-*]' }).Count
    $pending = ($content | Where-Object { $_ -match '\u3010\u5f85\u786e\u8ba4\u3011' }).Count
    $lastWrite = $_.LastWriteTime.ToString('yyyy-MM-dd')
    Write-Output "$name|$lines|$pending|$lastWrite"
}
