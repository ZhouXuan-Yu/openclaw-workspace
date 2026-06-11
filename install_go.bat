@echo off
echo ========================================
echo Go工具链安装脚本
echo ========================================
echo.

echo 步骤1: 下载Go安装程序
echo 正在下载Go 1.21.0 for Windows...
powershell -Command "Invoke-WebRequest -Uri 'https://golang.org/dl/go1.21.0.windows-amd64.msi' -OutFile 'go-install.msi'"
if %errorlevel% neq 0 (
    echo 下载失败，尝试备用链接...
    powershell -Command "Invoke-WebRequest -Uri 'https://dl.google.com/go/go1.21.0.windows-amd64.msi' -OutFile 'go-install.msi'"
)

echo.
echo 步骤2: 安装Go
echo 正在安装Go...
msiexec /i go-install.msi /quiet /norestart
if %errorlevel% neq 0 (
    echo 安装失败，请手动运行: msiexec /i go-install.msi
    pause
    exit /b 1
)

echo.
echo 步骤3: 设置环境变量
echo 设置Go环境变量...
setx GOPATH "%USERPROFILE%\go"
setx PATH "%PATH%;C:\Go\bin"

echo.
echo 步骤4: 验证安装
echo 等待环境变量生效...
timeout /t 5 /nobreak >nul

echo 检查Go版本:
go version
if %errorlevel% neq 0 (
    echo 警告: Go可能未正确安装，请重启命令行或系统
)

echo.
echo 步骤5: 安装sonos CLI工具
echo 正在安装sonos CLI...
go install github.com/steipete/sonoscli/cmd/sonos@latest
if %errorlevel% neq 0 (
    echo 安装sonos CLI失败
    echo 请确保Go已正确安装并重启命令行
)

echo.
echo 步骤6: 清理
del go-install.msi

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 注意: 可能需要重启命令行才能使环境变量生效
echo.
echo 验证命令:
echo 1. go version
echo 2. where sonos
echo.
pause