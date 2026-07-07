# vault-bridge.ps1 — PowerShell helper
# 用法: .\vault-bridge.ps1 extract "E:\Obsidian仓库\...\书.pdf" --slug my-book
#        .\vault-bridge.ps1 list
#        .\vault-bridge.ps1 status

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ArgsList
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Forward all args to the Python script
if ($ArgsList) {
    & python "$ScriptDir\vault_bridge.py" $Command @ArgsList
} else {
    & python "$ScriptDir\vault_bridge.py" $Command
}
