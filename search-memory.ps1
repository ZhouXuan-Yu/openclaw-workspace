# search-memory.ps1 — GGOB 记忆搜索 v7
# 用法: powershell -ExecutionPolicy Bypass -File search-memory.ps1 "关键词"
# 架构: 读一次文件 → 多 term 匹配 → 去重 → 限制输出 → 年龄感知

param([Parameter(Mandatory=$false)][string]$Query)

# 输入验证
if (-not $Query -or [string]::IsNullOrWhiteSpace($Query)) {
    Write-Host "Error: 搜索词不能为空" -ForegroundColor Red
    exit 0
}
if ($Query.Trim().Length -lt 2) {
    Write-Host "Error: 搜索词至少2个字符" -ForegroundColor Red
    exit 0
}

# 从脚本位置自动推导 workspace 路径（修复：之前硬编码 C:\Users\ZhouXuan\.openclaw\workspace）
$workspace = $PSScriptRoot
$maxResults = 50

# 同义词表
$synonyms = @{
    "docker"     = @("容器", "container", "部署", "deployment", "podman")
    "git"        = @("版本控制", "版本管理", "commit", "push", "pull", "branch")
    "memory"     = @("记忆", "记忆体", "记忆架构", "mem")
    "cron"       = @("定时任务", "计划任务", "调度", "schedule", "timer")
    "search"     = @("搜索", "查找", "检索", "grep", "find")
    "model"      = @("模型", "LLM", "大模型", "AI模型", "llm")
    "prompt"     = @("提示词", "system prompt", "系统提示")
    "preference" = @("偏好", "习惯", "风格", "喜欢")
    "project"    = @("项目", "工程", "任务")
    "learn"      = @("学习", "研究", "分析", "发现")
    "decision"   = @("决策", "选择", "确定", "决定")
    "correction" = @("纠正", "错误", "不对", "不要", "别用")
    "tool"       = @("工具", "插件", "plugin", "MCP", "mcp")
    "sync"       = @("同步", "备份", "backup")
    "consolidate" = @("整合", "合并", "整理", "dream")
    "reflect"    = @("反思", "复盘", "回顾", "教训")
    "aging"      = @("老化", "过期", "清理", "删除")
    "patrol"     = @("巡检", "检查", "健康", "health")
    "topic"      = @("主题", "分类")
    "session"    = @("会话", "对话", "聊天")
}

# 修复：收集所有匹配的同义词组（之前只匹配第一个就break）
$searchTerms = @($Query.Trim())
$qLower = $Query.Trim().ToLower()

$matchedGroups = @()
foreach ($key in $synonyms.Keys) {
    $kLower = $key.ToLower()
    $allVals = @($kLower) + ($synonyms[$key] | ForEach-Object { $_.ToLower() })
    if ($qLower -in $allVals) {
        $matchedGroups += $key
        $matchedGroups += $synonyms[$key]
    }
}
if ($matchedGroups.Count -gt 0) {
    $searchTerms += $matchedGroups | Where-Object { $_ -and $_.Trim() -ne "" } | Select-Object -Unique
}

$searchTerms = $searchTerms | Where-Object { $_ -and $_.Trim() -ne "" } | Select-Object -Unique

Write-Host "Searching memory for: '$Query'" -ForegroundColor Cyan
if ($searchTerms.Count -gt 1) {
    Write-Host "Expanded to: $($searchTerms -join ' | ')" -ForegroundColor DarkGray
}

# 收集所有文件
$allFiles = [System.Collections.ArrayList]::new()

$coreFiles = @(
    "$workspace\USER.md",
    "$workspace\MEMORY.md",
    "$workspace\AGENTS.md",
    "$workspace\SOUL.md",
    "$workspace\IDENTITY.md",
    "$workspace\TOOLS.md",
    "$workspace\HEARTBEAT.md"
)
foreach ($f in $coreFiles) {
    if (Test-Path $f) {
        [void]$allFiles.Add(@{Path=$f; Category="core"; Name=(Split-Path $f -Leaf)})
    }
}

$topicDir = "$workspace\memory\topics"
if (Test-Path $topicDir) {
    Get-ChildItem "$topicDir\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        [void]$allFiles.Add(@{Path=$_.FullName; Category="topics"; Name="topics/$($_.Name)"})
    }
}

$dailyDir = "$workspace\memory\daily"
if (Test-Path $dailyDir) {
    Get-ChildItem "$dailyDir\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        [void]$allFiles.Add(@{Path=$_.FullName; Category="daily"; Name="daily/$($_.Name)"})
    }
}

$agentDir = "$workspace\agents"
if (Test-Path $agentDir) {
    Get-ChildItem "$agentDir\*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        [void]$allFiles.Add(@{Path=$_.FullName; Category="agents"; Name="agents/$($_.Name)"})
    }
}

# 搜索
$results = [System.Collections.ArrayList]::new()

foreach ($fileInfo in $allFiles) {
    $content = Get-Content $fileInfo.Path -Encoding utf8 -ErrorAction SilentlyContinue
    if (-not $content) { continue }

    $mtime = (Get-Item $fileInfo.Path).LastWriteTime
    $ageDays = [math]::Round(((Get-Date) - $mtime).TotalDays, 1)
    $ageTag = ""
    if ($ageDays -gt 30) { $ageTag = " [! ${ageDays}d old]" }
    elseif ($ageDays -gt 7) { $ageTag = " [~ ${ageDays}d old]" }

    for ($lineNum = 0; $lineNum -lt $content.Count; $lineNum++) {
        $line = $content[$lineNum]
        if (-not $line) { continue }
        $lineLower = $line.ToLower()

        foreach ($term in $searchTerms) {
            if ($lineLower.Contains($term.ToLower())) {
                [void]$results.Add(@{
                    File     = $fileInfo.Name
                    Category = $fileInfo.Category
                    Line     = $lineNum + 1
                    Text     = $line.Trim()
                    Term     = $term
                    Age      = $ageDays
                    AgeTag   = $ageTag
                })
                break
            }
        }
    }
}

# 去重 + 限制输出
$unique = $results | Sort-Object File, Line -Unique

if ($unique.Count -eq 0) {
    Write-Host "`n  No results for '$Query'" -ForegroundColor Red
    Write-Host "  Searched: $($searchTerms -join ', ')" -ForegroundColor DarkGray
    exit 0
}

$grouped = $unique | Group-Object File
$shown = 0

foreach ($g in $grouped) {
    if ($shown -ge $maxResults) {
        Write-Host "`n  ... (truncated, $($unique.Count) total matches)" -ForegroundColor Yellow
        break
    }
    Write-Host "`n  [$($g.Name)]" -ForegroundColor Green
    $g.Group | ForEach-Object {
        if ($shown -lt $maxResults) {
            Write-Host "    L$($_.Line): $($_.Text)$($_.AgeTag)" -ForegroundColor Gray
            $shown++
        }
    }
}

Write-Host "`n  Found $($unique.Count) matches in $($grouped.Count) files" -ForegroundColor Cyan