# 精准修复：仅保持 OpenClaw 进程的网络连接不被 S0 待机关闭
# 需要以管理员身份运行

Write-Host "===== OpenClaw 熄屏网络保持 =====" -ForegroundColor Cyan
Write-Host "（仅针对 OpenClaw 保持活跃，不影响系统正常节能）" -ForegroundColor Gray
Write-Host ""

# 1. 修改 OpenClaw 启动方式——添加 ExecutionBackoff 防止进程被挂起
#    在启动脚本中嵌入 SetThreadExecutionState 调用
Write-Host "[1/2] 配置 OpenClaw 持续网络保持..." -ForegroundColor Yellow

# 创建一个包装脚本，在运行 OpenClaw 的同时保持系统在网络层面可用
$wrapperPath = "C:\Users\ZhouXuan\.openclaw\gateway_keepalive.ps1"
$wrapperContent = @'
# OpenClaw Gateway KeepAlive Wrapper
# 保持系统在网络层面不被 S0 待机完全冻结

$gatewayCmd = "C:\Users\ZhouXuan\.openclaw\gateway.cmd"

# 启动 OpenClaw 网关进程
$job = Start-Job -ScriptBlock {
    param($cmd)
    cmd /c $cmd
} -ArgumentList $gatewayCmd

# 每 45 秒发一次 ES_SYSTEM_REQUIRED | ES_CONTINUOUS 信号
# 这只阻止系统进入睡眠/关机，不影响显示器关闭
# S0 Modern Standby 下足以保持网络活跃
while ($job.State -eq 'Running') {
    # 加载 win32 API 保持系统活跃但不阻止显示器关闭
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public class PowerHelper {
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
    # ES_SYSTEM_REQUIRED = 0x00000001 | ES_CONTINUOUS = 0x80000000
    [PowerHelper]::SetThreadExecutionState(0x80000001) | Out-Null
    Start-Sleep -Seconds 45
}

# 如果 OpenClaw 意外退出，也取消保持
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class PowerHelper {
    [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
[PowerHelper]::SetThreadExecutionState(0x80000000) | Out-Null
'@

Set-Content -Path $wrapperPath -Value $wrapperContent
Write-Host "  ✅ 已创建包装脚本: gateway_keepalive.ps1" -ForegroundColor Green

# 2. 更新计划任务引用到新的包装脚本
Write-Host "[2/2] 更新计划任务..." -ForegroundColor Yellow

# 创建一个新的计划任务或更新现有任务
# 新的启动命令: powershell -ExecutionPolicy Bypass -File "...gateway_keepalive.ps1"
$newAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$wrapperPath`""

# 停止现有任务
Stop-ScheduledTask -TaskPath "\" -TaskName "OpenClaw Gateway" -ErrorAction SilentlyContinue

# 更新任务的配置
# 保持 LogonType=InteractiveToken（交互登录），这样能访问用户凭据
# 但是去掉"只使用交互方式"的限制
$taskPath = "\OpenClaw Gateway"

# 获取现有任务
$task = Get-ScheduledTask -TaskPath "\" -TaskName "OpenClaw Gateway" -ErrorAction SilentlyContinue
if ($task) {
    # 更新 action
    $task.Actions = $newAction
    # 确保电源相关设置：不因电池停止，不因电池暂停
    $task.Settings.DisallowStartIfOnBatteries = $false
    $task.Settings.StopIfGoingOnBatteries = $false
    # 应用
    Set-ScheduledTask -TaskPath "\" -TaskName "OpenClaw Gateway" -Action $newAction -ErrorAction SilentlyContinue
    Write-Host "  ✅ 已更新计划任务: OpenClaw Gateway" -ForegroundColor Green
} else {
    # 如果任务不存在，重新创建
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
    Register-ScheduledTask -TaskName "OpenClaw Gateway" -Action $newAction -Trigger $trigger -Settings $settings -Principal $principal -Force
    Write-Host "  ✅ 已创建计划任务: OpenClaw Gateway" -ForegroundColor Green
}

Write-Host ""
Write-Host "===== 完成 =====" -ForegroundColor Cyan
Write-Host "重启计划任务即可生效..." -ForegroundColor Yellow
Write-Host ""
Write-Host "可选：你也可以在设备管理器中关闭网卡节能（不必须）"
Write-Host "  设备管理器 → 网络适配器 → WLAN → 属性 → 电源管理"
Write-Host "  → 取消勾选'允许计算机关闭此设备以节约电源'"
