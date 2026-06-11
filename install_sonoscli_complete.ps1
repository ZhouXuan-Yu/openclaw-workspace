Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sonoscli技能完整安装脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 步骤1: 检查Node.js和npm
Write-Host "步骤1: 检查Node.js和npm" -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "Node.js版本: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: Node.js未安装" -ForegroundColor Red
    exit 1
}

try {
    $npmVersion = npm --version
    Write-Host "npm版本: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: npm未安装" -ForegroundColor Red
    exit 1

Write-Host ""
Write-Host "步骤2: 安装Clawhub CLI" -ForegroundColor Yellow
Write-Host "正在安装clawhub..." -ForegroundColor Gray
npm install -g clawhub
if ($LASTEXITCODE -ne 0) {
    Write-Host "警告: 全局安装失败，将尝试使用npx" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "步骤3: 安装sonoscli技能" -ForegroundColor Yellow
Write-Host "正在安装sonoscli技能..." -ForegroundColor Gray
clawhub install sonoscli
if ($LASTEXITCODE -ne 0) {
    Write-Host "尝试使用npx安装..." -ForegroundColor Gray
    npx clawhub@latest install sonoscli
}

Write-Host ""
Write-Host "步骤4: 检查Go安装（sonoscli需要）" -ForegroundColor Yellow
$goPath = Get-Command go -ErrorAction SilentlyContinue
if (-not $goPath) {
    Write-Host "警告: Go未安装。sonoscli技能需要Go来编译。" -ForegroundColor Yellow
    Write-Host "请从 https://golang.org/dl/ 安装Go" -ForegroundColor Yellow
} else {
    Write-Host "Go已安装: $($goPath.Source)" -ForegroundColor Green
}

Write-Host ""
Write-Host "步骤5: 验证安装" -ForegroundColor Yellow
Write-Host "已安装的技能列表:" -ForegroundColor Gray
clawhub list

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "注意: sonoscli技能需要Go工具链。" -ForegroundColor Yellow
Write-Host "如果Go未安装，请先安装Go，然后运行:" -ForegroundColor Gray
Write-Host "go install github.com/steipete/sonoscli/cmd/sonos@latest" -ForegroundColor White
Write-Host ""
Read-Host "按Enter键继续..."