# Git Evolution Analysis Script
# Called by awareness loop to analyze Git history

param(
    [int]$Days = 7,
    [switch]$FullReport
)

Set-Location "C:\Users\ZhouXuan\.openclaw\workspace"

Write-Output "=== Git Evolution Analysis (Last $Days days) ==="

# 1. Commit count
$commits = git log --oneline --since="$Days days" 2>&1
$commitCount = ($commits | Measure-Object).Count
Write-Output ""
Write-Output "Total commits: $commitCount"

# 2. By type
Write-Output ""
Write-Output "--- Evolution Types ---"
$typeList = @("feat","fix","refactor","docs","security","evolution","meta","snapshot")
foreach ($t in $typeList) {
    $c = ($commits | Select-String -Pattern "^$t").Count
    if ($c -gt 0) {
        $bar = ""
        for ($i = 0; $i -lt [math]::Min($c, 20); $i++) { $bar += "#" }
        Write-Output ("  {0}: {1} {2}" -f $t, $bar, $c)
    }
}

# 3. Most active files
Write-Output ""
Write-Output "--- Most Active Files (Top 10) ---"
$files = git log --since="$Days days" --name-only --pretty=format:"" 2>&1 |
    Where-Object { $_ -ne "" } | Group-Object | Sort-Object Count -Descending | Select-Object -First 10
foreach ($f in $files) {
    Write-Output ("  {0}x: {1}" -f $f.Count, $f.Name)
}

# 4. Skill evolution
Write-Output ""
Write-Output "--- Skill Evolution ---"
$skillCommits = git log --since="$Days days" -- "skills/*/SKILL.md" --pretty=format:"%s" 2>&1
if ($skillCommits) {
    foreach ($s in $skillCommits) { Write-Output "  $s" }
} else {
    Write-Output "  No skill evolution"
}

# 5. Architecture changes
Write-Output ""
Write-Output "--- Architecture Changes ---"
$archCommits = git log --since="$Days days" -- "agents/*.md" --pretty=format:"%s" 2>&1
if ($archCommits) {
    foreach ($a in $archCommits) { Write-Output "  $a" }
} else {
    Write-Output "  No architecture changes"
}

# 6. Security
Write-Output ""
Write-Output "--- Security Related ---"
$secCommits = $commits | Select-String -Pattern "security|safe"
if ($secCommits) {
    foreach ($s in $secCommits) { Write-Output "  $($s.Line)" }
} else {
    Write-Output "  No security commits"
}

# 7. Daily trend
if ($FullReport) {
    Write-Output ""
    Write-Output "--- Daily Trend ---"
    for ($d = $Days - 1; $d -ge 0; $d--) {
        $date = (Get-Date).AddDays(-$d).ToString("yyyy-MM-dd")
        $dayCommits = git log --after="$date 00:00" --before="$date 23:59" --oneline 2>&1
        $dayCount = ($dayCommits | Measure-Object).Count
        $bar = ""
        for ($i = 0; $i -lt [math]::Min($dayCount, 20); $i++) { $bar += "#" }
        Write-Output ("  {0}: {1} {2}" -f $date, $bar, $dayCount)
    }
}

Write-Output ""
Write-Output "=== Analysis Complete ==="