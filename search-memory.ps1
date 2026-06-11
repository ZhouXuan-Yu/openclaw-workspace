# search-memory.ps1
# 用法: .\search-memory.ps1 "关键词"
param([Parameter(Mandatory=$true)][string]$Query)

$workspace = "C:\Users\ZhouXuan\.openclaw\workspace"
$files = @(
    "$workspace\USER.md",
    "$workspace\MEMORY.md",
    "$workspace\AGENTS.md",
    "$workspace\SOUL.md"
)
$memoryDir = "$workspace\memory"

Write-Host "Searching memory for: '$Query'" -ForegroundColor Cyan

$total = 0
foreach ($f in $files) {
    if (Test-Path $f) {
        $r = Select-String -Path $f -Pattern $Query -SimpleMatch
        if ($r) {
            $name = Split-Path $f -Leaf
            Write-Host "`n  [$name]" -ForegroundColor Green
            $r | ForEach-Object { Write-Host "    $($_.LineNumber): $($_.Line.Trim())" }
            $total++
        }
    }
}

if (Test-Path $memoryDir) {
    $r = Select-String -Path "$memoryDir\*.md" -Pattern $Query -SimpleMatch
    if ($r) {
        Write-Host "`n  [memory/]" -ForegroundColor Green
        $r | Group-Object Filename | ForEach-Object {
            Write-Host "    $(Split-Path $_.Name -Leaf):" -ForegroundColor Yellow
            $_.Group | ForEach-Object { Write-Host "      $($_.LineNumber): $($_.Line.Trim())" }
        }
        $total++
    }
}

if ($total -eq 0) { Write-Host "`n  No results for '$Query'" -ForegroundColor Red }
