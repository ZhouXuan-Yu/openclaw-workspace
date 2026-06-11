@echo off
chcp 65001 >nul
echo ========================================
echo  OpenClaw 熄屏不断连修复脚本
echo  皇家卫士 GGOB 🛡️
echo ========================================
echo.

echo [1/4] 设置电源：插电永不睡眠，电池永不睡眠
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
echo ✅ 睡眠已禁用（AC + DC）
echo.

echo [2/4] 关闭休眠（同时也关闭混合睡眠）
powercfg /h off
echo ✅ 休眠已关闭
echo.

echo [3/4] 关闭 USB 选择性暂停（防止 WiFi 网卡被挂起）
powercfg /setacvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvalueindex SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setactive SCHEME_CURRENT
echo ✅ USB 选择性暂停已禁用
echo.

echo [4/4] 修改 OpenClaw 计划任务 — 电池模式下不停止
schtasks /change /tn "OpenClaw Gateway" /IT ^
    /change /tn "OpenClaw Gateway" /RU "%USERDOMAIN%\%USERNAME%"
:: 改用 XML 导入方式修改电源设置
schtasks /query /tn "OpenClaw Gateway" /xml > "%TEMP%\OpenClawGateway_orig.xml"
powershell -Command ^
    "$x = [xml](Get-Content '%TEMP%\OpenClawGateway_orig.xml' -Encoding Unicode);" ^
    "$x.Task.Settings.DisallowStartIfOnBatteries = 'false';" ^
    "$x.Task.Settings.StopIfGoingOnBatteries = 'false';" ^
    "$x.Save('%TEMP%\OpenClawGateway_fixed.xml');"
schtasks /create /tn "OpenClaw Gateway" /xml "%TEMP%\OpenClawGateway_fixed.xml" /f
echo ✅ OpenClaw 计划任务电池策略已修复
echo.

echo ========================================
echo 🎉 全部完成！请重启一下电脑让设置生效
echo ========================================
pause
