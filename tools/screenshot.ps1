<#
.SYNOPSIS
    截取当前屏幕截图并保存为 PNG 文件
.DESCRIPTION
    使用 Windows GDI+ 原生 API 截取主屏幕画面。
    输出路径: memory/screenshots/screenshot_<时间戳>.png
.PARAMETER OutputPath
    自定义输出路径（可选）
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\screenshot.ps1
    powershell -ExecutionPolicy Bypass -File tools\screenshot.ps1 -OutputPath "C:\temp\shot.png"
#>
param(
    [string]$OutputPath
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 默认输出路径
if (-not $OutputPath) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $OutputPath = Join-Path $PSScriptRoot "..\memory\screenshots\screenshot_$timestamp.png"
}

# 创建目录
$outputDir = Split-Path $OutputPath -Parent
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# 获取主屏幕尺寸
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

# 截图
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()

Write-Output $OutputPath
