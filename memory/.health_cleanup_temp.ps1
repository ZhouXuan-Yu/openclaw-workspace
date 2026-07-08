# [待确认] check using unicode escape
$topicsDir = "C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
$pattern = [char]0x5F85 + [char]0x786E + [char]0x8BA4
Write-Host "=== [待确认] MARKERS ==="
Get-ChildItem "$topicsDir\*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $count = [regex]::Matches($content, $pattern).Count
    $name = $_.Name
    Write-Host "$name : $count"
}

# Temp cleanup
Write-Host "=== TEMP CLEANUP ==="
$tempDir = "C:\Users\ZhouXuan\.openclaw\workspace\temp"
if (Test-Path $tempDir) {
    Get-ChildItem $tempDir -Directory | Where-Object { $_.Name -ne 'video-audio' -and $_.Name -ne 'video-test' } | ForEach-Object {
        Write-Host "  Deleting dir: $($_.Name)"
        Remove-Item $_.FullName -Recurse -Force
    }
} else {
    Write-Host "  temp dir not found"
}

# tools cleanup
Write-Host "=== TOOLS CLEANUP ==="
$toolsDir = "C:\Users\ZhouXuan\.openclaw\workspace\tools"
$patterns = @('check_*.py','explore_*.py','gen_*.py','render_*.py','launch_*.py','open_*.py')
foreach ($p in $patterns) {
    Get-ChildItem "$toolsDir\$p" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "  Deleting: $($_.Name)"
        Remove-Item $_.FullName -Force
    }
}
