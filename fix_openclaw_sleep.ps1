# 需要以管理员身份运行！
# OpenClaw 熄屏不断连修复脚本 — 皇家卫士 GGOB 🛡️

function Write-Step($text) {
    Write-Host "`n>>> $text" -ForegroundColor Green
}

$sep = "=" * 40

Write-Host $sep -ForegroundColor Cyan
Write-Host " OpenClaw 熄屏不断连修复脚本" -ForegroundColor Cyan
Write-Host " 需要管理员权限！" -ForegroundColor Yellow
Write-Host $sep -ForegroundColor Cyan

# [1/4] 电源设置
Write-Step "设置电源：插电永不睡眠，电池永不睡眠"
powercfg /change standby-timeout-ac 0
powercfg /change standby-timeout-dc 0
Write-Host "  [OK] 睡眠已禁用 (AC + DC)" -ForegroundColor Green

# [2/4] 关闭休眠
Write-Step "关闭休眠 + 混合睡眠"
powercfg /h off
Write-Host "  [OK] 休眠已关闭" -ForegroundColor Green

# [3/4] USB 选择性暂停
Write-Step "关闭 USB 选择性暂停（防止WiFi网卡被挂起）"
$usbGuid = "2a737441-1930-4402-8d77-b2bebba308a3"
$usbSetting = "48e6b7a6-50f5-4782-a5d4-53bb8f07e226"
powercfg /setacvalueindex SCHEME_CURRENT $usbGuid $usbSetting 0
powercfg /setdcvalueindex SCHEME_CURRENT $usbGuid $usbSetting 0
powercfg /setactive SCHEME_CURRENT
Write-Host "  [OK] USB 选择性暂停已禁用" -ForegroundColor Green

# [4/4] 修改计划任务
Write-Step "修改 OpenClaw 计划任务 — 电池模式不停止"
$taskXmlPath = "$env:TEMP\OpenClawGateway_fixed.xml"
schtasks /query /tn "OpenClaw Gateway" /xml 2>$null | Out-File $taskXmlPath -Encoding Unicode
if (Test-Path $taskXmlPath) {
    [xml]$taskXml = Get-Content $taskXmlPath -Encoding Unicode
    $taskXml.Task.Settings.DisallowStartIfOnBatteries = "false"
    $taskXml.Task.Settings.StopIfGoingOnBatteries = "false"
    $taskXml.Save($taskXmlPath)
    schtasks /create /tn "OpenClaw Gateway" /xml $taskXmlPath /f
    Write-Host "  [OK] OpenClaw 计划任务电池策略已修复" -ForegroundColor Green
} else {
    Write-Host "  [!!] 未找到 OpenClaw Gateway 计划任务，请确认 openclaw 已安装" -ForegroundColor Red
}

# [5] 额外优化：唤醒定时器
Write-Step "额外优化：启用唤醒定时器"
$sleepGuid = "238c9fa8-0aad-41ed-83f4-97be242c8f20"
$wakeGuid = "bd3b718a-0680-4d9d-8ab2-e1d2b4ac806d"
powercfg /setacvalueindex SCHEME_CURRENT $sleepGuid $wakeGuid 1
powercfg /setdcvalueindex SCHEME_CURRENT $sleepGuid $wakeGuid 1
powercfg /setactive SCHEME_CURRENT
Write-Host "  [OK] 唤醒定时器已启用" -ForegroundColor Green

Write-Host "`n$sep" -ForegroundColor Cyan
Write-Host " 全部完成！建议重启电脑让设置生效。" -ForegroundColor Green
Write-Host " 或执行: openclaw restart" -ForegroundColor Green
Write-Host "$sep" -ForegroundColor Cyan

Read-Host "`n按 Enter 退出"
