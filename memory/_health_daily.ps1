$dailyDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\daily"
$cutoff = (Get-Date).AddDays(-7)
Get-ChildItem "$dailyDir\*.md" | Where-Object { $_.LastWriteTime -gt $cutoff } | Select-Object -ExpandProperty Name | Sort-Object
