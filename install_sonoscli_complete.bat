@echo off
echo ========================================
echo Sonoscli技能完整安装脚本
echo ========================================
echo.

echo 步骤1: 检查Node.js和npm
node --version
if %errorlevel% neq 0 (
    echo 错误: Node.js未安装
    exit /b 1
)
npm --version
if %errorlevel% neq 0 (
    echo 错误: npm未安装
    exit /b 1
)

echo.
echo 步骤2: 安装Clawhub CLI
echo 正在安装clawhub...
npm install -g clawhub
if %errorlevel% neq 0 (
    echo 警告: 全局安装失败，尝试使用npx
)

echo.
echo 步骤3: 安装sonoscli技能
echo 正在安装sonoscli技能...
clawhub install sonoscli
if %errorlevel% neq 0 (
    echo 尝试使用npx安装...
    npx clawhub@latest install sonoscli
)

echo.
echo 步骤4: 检查Go安装（sonoscli需要）
where go
if %errorlevel% neq 0 (
    echo 警告: Go未安装。sonoscli技能需要Go来编译。
    echo 请从 https://golang.org/dl/ 安装Go
)

echo.
echo 步骤5: 验证安装
echo 已安装的技能列表:
clawhub list

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 注意: sonoscli技能需要Go工具链。
echo 如果Go未安装，请先安装Go，然后运行:
echo go install github.com/steipete/sonoscli/cmd/sonos@latest
echo.
pause