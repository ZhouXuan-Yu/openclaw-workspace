# SQLPage 数据面板 — 一键管理

# 启动
function Start-Sqlpage {
    cd "$PSScriptRoot"
    docker compose up -d
    Start-Sleep 2
    Write-Host "✅ SQLPage 已启动: http://localhost:8080"
}

# 刷新数据库（从宿主机同步最新数据）
function Update-SqlpageData {
    param([switch]$Restart)
    cd "$PSScriptRoot"
    Write-Host "🔄 刷新数据库副本..."
    docker compose restart sqlpage
    Start-Sleep 2
    Write-Host "✅ 数据库已刷新（重启时自动从宿主机复制最新版本）"
}

# 停止
function Stop-Sqlpage {
    cd "$PSScriptRoot"
    docker compose down
    Write-Host "⏹ SQLPage 已停止"
}

# 状态
function Status-Sqlpage {
    docker ps --filter name=sqlpage --format "{{.Status}}" 2>$null
    if ($LASTEXITCODE -ne 0) { Write-Host "❌ 未运行" }
}
