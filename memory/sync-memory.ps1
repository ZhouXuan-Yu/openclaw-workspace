# GGOB 记忆同步脚本 v2
# 用途：自动 commit + push 记忆文件变更
# 触发：cron 每天 02:15（整合完成后）或手动执行
# 合并了原 git-sync.ps1 的功能

$workspace = "C:\Users\ZhouXuan\.openclaw\workspace"
cd $workspace

# 检查是否有变更
$changes = git diff --name-only -- memory/ MEMORY.md memory/evolution/ 2>$null
$untracked = git ls-files --others --exclude-standard -- memory/ MEMORY.md memory/evolution/ 2>$null

if (-not $changes -and -not $untracked) {
    Write-Output "[memory-sync] 没有记忆文件变更，跳过"
    exit 0
}

# Stage 记忆文件
git add MEMORY.md memory/

# 构建 commit 消息
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
$summary = ""
if ($changes) { $summary += "更新: " + ($changes -join ", ") }
if ($untracked) { $summary += " 新增: " + ($untracked -join ", ") }

# Commit
git commit -m "memory: auto-sync $date`n$summary" 2>&1

# Push（如果配置了 remote）
$remote = git remote 2>$null
if ($remote) {
    git push 2>&1
    Write-Output "[memory-sync] 已推送到 remote"
} else {
    Write-Output "[memory-sync] 无 remote 配置，仅本地 commit"
}
