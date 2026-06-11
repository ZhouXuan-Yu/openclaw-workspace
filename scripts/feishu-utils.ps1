# feishu-utils.ps1 - 飞书 API 工具函数

function Get-FeishuToken {
    param([string]$AppId = "cli_a947f10f56f8dcc3", [string]$AppSecret)
    $body = '{"app_id":"' + $AppId + '","app_secret":"' + $AppSecret + '"}'
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -Body $body -ContentType "application/json"
    return $resp.tenant_access_token
}

function New-FeishuDoc {
    param([string]$Title, [string]$Token, [int]$MaxTitleLength = 200)
    if ([string]::IsNullOrWhiteSpace($Title)) {
        $Title = "unnamed-doc-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Warning "Title empty, using default: $Title"
    }
    if ($Title.Length -gt $MaxTitleLength) {
        $Title = $Title.Substring(0, $MaxTitleLength) + "..."
        Write-Warning "Title truncated to $MaxTitleLength chars"
    }
    $Title = $Title -replace '<script.*?</script>', ''
    $Title = $Title -replace 'javascript:', ''
    $hdr = @{Authorization = "***"; "Content-Type" = "application/json"}
    $body = '{"title":"' + ($Title -replace '"', '\"') + '"}'
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/docx/v1/documents" -Method Post -Headers $hdr -Body $body
    return $resp
}

function Send-FeishuMessage {
    param([string]$ReceiveId, [string]$Content, [string]$Token, [int]$MaxContentLength = 5000)
    if ([string]::IsNullOrWhiteSpace($Content)) { throw "Content cannot be empty" }
    if ($ReceiveId -notmatch '^(ou_|oc_|cli_)') { throw "Invalid receive_id: $ReceiveId" }
    if ($Content.Length -gt $MaxContentLength) {
        $Content = $Content.Substring(0, $MaxContentLength) + "`n...[truncated]"
        Write-Warning "Content truncated to $MaxContentLength chars"
    }
    $hdr = @{Authorization = "***"; "Content-Type" = "application/json"}
    $escapedContent = ($Content -replace '"', '\"') -replace "`n", '\n'
    $body = '{"receive_id":"' + $ReceiveId + '","msg_type":"text","content":"{\"text\":\"' + $escapedContent + '\"}"}'
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" -Method Post -Headers $hdr -Body $body
    return $resp
}

function New-FeishuEvent {
    param([string]$Summary, [DateTime]$StartTime, [DateTime]$EndTime, [string]$Token)
    if ([string]::IsNullOrWhiteSpace($Summary)) { $Summary = "meeting-$(Get-Date -Format 'HH:mm')" }
    if ($EndTime -le $StartTime) { throw "EndTime must be after StartTime" }
    if ($StartTime -lt (Get-Date)) { Write-Warning "StartTime is in the past" }
    $startTs = [DateTimeOffset]::new($StartTime).ToUnixTimeSeconds()
    $endTs = [DateTimeOffset]::new($EndTime).ToUnixTimeSeconds()
    $hdr = @{Authorization = "***"; "Content-Type" = "application/json"}
    $body = '{"summary":"' + $Summary + '","start_time":{"timestamp":"' + $startTs + '"},"end_time":{"timestamp":"' + $endTs + '"}}'
    $resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary/events" -Method Post -Headers $hdr -Body $body
    return $resp
}

Write-Output "feishu-utils.ps1 loaded: Get-FeishuToken, New-FeishuDoc, Send-FeishuMessage, New-FeishuEvent"
