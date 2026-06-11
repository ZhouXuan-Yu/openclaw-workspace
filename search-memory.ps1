# search-memory.ps1 — GGOB 记忆搜索 v6
# 用法: .\search-memory.ps1 "关键词"
# 修复: UTF-8 BOM 编码问题 + 空查询防护 + 边界处理

param([Parameter(Mandatory=$true)][string]$Query)

# 空查询防护
if ([string]::IsNullOrWhiteSpace($Query)) {
    Write-Host "Error: 搜索词不能为空" -ForegroundColor Red
    exit 1
}

$workspace = "C:\Users\ZhouXuan\.openclaw\workspace"

# ═══════ 同义词表（英文key避免编码问题）═══════
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

# ═══════ 构建搜索词列表 ═══════
$searchTerms = @($Query)

# 查找同义词（不区分大小写）
foreach ($key in $synonyms.Keys) {
    if ($Query -ieq $key) {
        $searchTerms += $synonyms[$key]
        break
    }
    if ($synonyms[$key] -contains $Query) {
        $searchTerms += $key
        $searchTerms += ($synonyms[$key] | Where-Object { $_ -ne $Query })
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
                if ($days -gt 30) { $ageWarning = " [! ${days}d old]" }
                elseif ($days -gt 7) { $ageWarning = " [~ ${days}d old]" }
            }
            Write-Host "    L$($_.Line): $($_.Text)$ageWarning" -ForegroundColor Gray
        }
    }
    Write-Host "`n  Found $($results.Count) matches in $($grouped.Count) files" -ForegroundColor Cyan
} else {
    Write-Host "`n  No results for '$Query'" -ForegroundColor Red
    Write-Host "  Searched: $($searchTerms -join ', ')" -ForegroundColor DarkGray
}
