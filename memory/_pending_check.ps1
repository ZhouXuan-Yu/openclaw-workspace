$pattern = [char]0x5F85 + [char]0x786E + [char]0x8BA4
Get-ChildItem 'C:\Users\ZhouXuan\.openclaw\workspace\memory\topics\*.md' | ForEach-Object {
    $content = Get-Content $_.FullName -Encoding utf8
    $count = ($content | Select-String -Pattern $pattern -SimpleMatch).Count
    Write-Output "$($_.Name): $count"
}
