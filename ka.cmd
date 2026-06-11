@echo off
chcp 65001 >nul
title OpenClaw 熄屏网络保持
echo ===== OpenClaw 熄屏网络保持 =====
echo 仅针对 OpenClaw 进程保持网络活跃
echo.
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在请求管理员权限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
echo 正在应用修复...
powershell -ExecutionPolicy Bypass -File "%~dp0fix_openclaw_keepalive.ps1"
pause
