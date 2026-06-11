# GGOB 记忆同步脚本
# 用途：自动 commit + push 记忆文件变更
# 触发：cron 每天 02:10（整合完成后）或手动执行

$workspace = "C:\Users\ZhouXuan\.openclaw\workspace"
cd $workspace

# 只提交记忆相关文件（不碰其他文件）
$memoryFiles = @(
    "MEMORY.md",
    "memory/"
)

# 检查是否有变更
$changes = git diff --name-only -- memory/ MEMORY.md 2>$null
$untracked = git ls-files --others --exclude-standard -- memory/ MEMORY.md 2>$null

if (-not $changes -and -not $untracked) {
    Write-Output "[memory-sync] 没有记忆文件变更，跳过"
    exit 0
}

# Stage 记忆文件
git add MEMORY.md memory/

# Commit
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
$summary = ""
if ($changes) { $summary += "更新: " + ($changes -join ", ") }
if ($untracked) { $summary += " 新增: " + ($untracked -join ", ") }
git commit -m "memory: auto-sync $date`n$summary" 2>&1

# Push（如果配置了 remote）
$remote = git remote 2>$null
if ($remote) {
    git push 2>&1
    Write-Output "[memory-sync] 已推送到 remote"
} else {
    Write-Output "[memory-sync] 无 remote 配置，仅本地 commit"
}
