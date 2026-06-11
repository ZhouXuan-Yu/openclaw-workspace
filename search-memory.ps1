# search-memory.ps1 — GGOB 记忆搜索 v5
# 用法: .\search-memory.ps1 "关键词"
# 新增：同义词扩展 + 模糊匹配 + 年龄感知

param([Parameter(Mandatory=$true)][string]$Query)

$workspace = "C:\Users\ZhouXuan\.openclaw\workspace"

# ═══════ 同义词表 ═══════
$synonyms = @{
    "docker"     = @("容器", "container", "部署", "deployment", "podman")
    "git"        = @("版本控制", "版本管理", "commit", "push", "pull", "branch")
    "记忆"       = @("memory", "记忆体", "记忆架构", "mem")
    "cron"       = @("定时任务", "计划任务", "调度", "schedule", "timer")
    "搜索"       = @("search", "查找", "检索", "grep", "find")
    "模型"       = @("model", "LLM", "大模型", "AI模型", "llm")
    "提示词"     = @("prompt", "system prompt", "系统提示", "system-prompt")
    "偏好"       = @("preference", "习惯", "风格", "喜欢")
    "项目"       = @("project", "工程", "任务")
    "学习"       = @("learn", "研究", "分析", "发现")
    "决策"       = @("decision", "选择", "确定", "决定")
    "纠正"       = @("correction", "错误", "不对", "不要", "别用")
    "工具"       = @("tool", "插件", "plugin", "MCP", "mcp")
    "同步"       = @("sync", "备份", "backup", "git")
    "整合"       = @("consolidation", "合并", "整理", "dream")
    "反思"       = @("reflection", "复盘", "回顾", "教训")
    "老化"       = @("aging", "过期", "清理", "删除")
    "巡检"       = @("patrol", "检查", "健康", "health")
    "topic"      = @("主题", "分类", "文件")
    "session"    = @("会话", "对话", "聊天")
}

# ═══════ 构建搜索词列表 ═══════
$searchTerms = @($Query)

# 查找同义词（不区分大小写）
foreach ($key in $synonyms.Keys) {
    if ($Query -ieq $key -or $synonyms[$key] -contains $Query) {
        $searchTerms += $key
        $searchTerms += $synonyms[$key]
        break
    }
}

# 去重 + 过滤空值
$searchTerms = $searchTerms | Where-Object { $_ -ne "" } | Select-Object -Unique

Write-Host "Searching memory for: '$Query'" -ForegroundColor Cyan
if ($searchTerms.Count -gt 1) {
    Write-Host "Expanded to: $($searchTerms -join ' | ')" -ForegroundColor DarkGray
}

# ═══════ 搜索文件 ═══════
$files = @(
    "$workspace\USER.md",
    "$workspace\MEMORY.md",
    "$workspace\AGENTS.md",
    "$workspace\SOUL.md"
)
$memoryDir = "$workspace\memory"

$total = 0
$results = @()

# 搜索核心文件
foreach ($f in $files) {
    if (Test-Path $f) {
        foreach ($term in $searchTerms) {
            $r = Select-String -Path $f -Pattern $term -SimpleMatch -ErrorAction SilentlyContinue
            if ($r) {
                $name = Split-Path $f -Leaf
                $r | ForEach-Object {
                    $results += [PSCustomObject]@{
                        File = $name
                        Line = $_.LineNumber
                        Text = $_.Line.Trim()
                        Term = $term
                    }
                }
            }
        }
    }
}

# 搜索 memory/ 目录
if (Test-Path $memoryDir) {
    foreach ($term in $searchTerms) {
        # 搜索 topics/
        $topicFiles = Get-ChildItem "$memoryDir\topics\*.md" -ErrorAction SilentlyContinue
        foreach ($tf in $topicFiles) {
            $r = Select-String -Path $tf.FullName -Pattern $term -SimpleMatch -ErrorAction SilentlyContinue
            if ($r) {
                $r | ForEach-Object {
                    $results += [PSCustomObject]@{
                        File = "topics/$(Split-Path $_.Path -Leaf)"
                        Line = $_.LineNumber
                        Text = $_.Line.Trim()
                        Term = $term
                    }
                }
            }
        }

        # 搜索 daily/
        $dailyFiles = Get-ChildItem "$memoryDir\daily\*.md" -ErrorAction SilentlyContinue
        foreach ($df in $dailyFiles) {
            $r = Select-String -Path $df.FullName -Pattern $term -SimpleMatch -ErrorAction SilentlyContinue
            if ($r) {
                $r | ForEach-Object {
                    $results += [PSCustomObject]@{
                        File = "daily/$(Split-Path $_.Path -Leaf)"
                        Line = $_.LineNumber
                        Text = $_.Line.Trim()
                        Term = $term
                    }
                }
            }
        }

        # 搜索根目录 memory/*.md（旧格式兼容）
        $rootFiles = Get-ChildItem "$memoryDir\*.md" -ErrorAction SilentlyContinue
        foreach ($rf in $rootFiles) {
            $r = Select-String -Path $rf.FullName -Pattern $term -SimpleMatch -ErrorAction SilentlyContinue
            if ($r) {
                $r | ForEach-Object {
                    $results += [PSCustomObject]@{
                        File = "memory/$(Split-Path $_.Path -Leaf)"
                        Line = $_.LineNumber
                        Text = $_.Line.Trim()
                        Term = $term
                    }
                }
            }
        }
    }
}

# ═══════ 去重输出 ═══════
$grouped = $results | Sort-Object File, Line -Unique | Group-Object File

if ($grouped) {
    foreach ($g in $grouped) {
        Write-Host "`n  [$($g.Name)]" -ForegroundColor Green
        $g.Group | ForEach-Object {
            $ageWarning = ""
            # 年龄感知：检查文件修改时间
            $filePath = "$workspace\$($_.File)"
            if (Test-Path $filePath) {
                $mtime = (Get-Item $filePath).LastWriteTime
                $days = ((Get-Date) - $mtime).Days
                if ($days -gt 30) { $ageWarning = " [🚨 ${days}天前]" }
                elseif ($days -gt 7) { $ageWarning = " [⚠️ ${days}天前]" }
            }
            Write-Host "    $($_.Line): $($_.Text)$ageWarning" -ForegroundColor Gray
        }
        $total++
    }
    Write-Host "`n  Found $total files with matches" -ForegroundColor Cyan
} else {
    Write-Host "`n  No results for '$Query'" -ForegroundColor Red
    Write-Host "  Searched terms: $($searchTerms -join ', ')" -ForegroundColor DarkGray
}
