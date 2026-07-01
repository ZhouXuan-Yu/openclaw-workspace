# OpenClaw Dashboard 自维护脚本
# 每次对话结束时自动调用，从系统实时采集数据并生成 HTML
# 调用方式: powershell -File tools\refresh-dashboard.ps1

$ErrorActionPreference = "SilentlyContinue"
$out = "$env:USERPROFILE\.openclaw\workspace\tools\dashboard.html"
$db = "$env:USERPROFILE\.openclaw\memory\main.sqlite"
$ws = "$env:USERPROFILE\.openclaw\workspace"

$ver = (openclaw --version 2>&1).Trim()
$mf  = (sqlite3 $db "SELECT COUNT(*) FROM files;" 2>&1).Trim()
$mc  = (sqlite3 $db "SELECT COUNT(*) FROM chunks;" 2>&1).Trim()
$ec  = (Get-ChildItem "$ws\memory\evolution\*" -File -EA 0).Count
$dc  = (Get-ChildItem "$ws\memory\daily\*.md" -File -EA 0).Count
$tc  = (Get-ChildItem "$ws\memory\topics\*.md" -File -EA 0).Count
$sc  = (Get-ChildItem "$ws\skills" -Directory -EA 0).Count
$oc  = (Get-ChildItem "$ws\memory\evolution\observations*" -File -EA 0).Count
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
$hn  = $env:COMPUTERNAME

$rf = & sqlite3 $db "SELECT path || '|' || printf('%.1f KB', size/1024.0) FROM files ORDER BY mtime DESC LIMIT 8;" 2>&1 | ForEach-Object {
    $p = $_.Split('|')
    "<div class='status-row'><span class='clip'>$($p[0])</span><span style='margin-left:auto;font-family:monospace;font-size:0.75rem'>$($p[1])</span></div>"
}
$rf_html = $rf -join ""

$df = Get-ChildItem "$ws\memory\daily\*.md" -File -EA 0 | Sort-Object Name -Descending | Select-Object -First 7 | ForEach-Object {
    "<div class='status-row'><span>$($_.Name)</span></div>"
}
$df_html = $df -join ""

# Build cron status from cron list
$cron_raw = & openclaw cron list 2>&1 | Select-Object -Skip 1
$cron_rows = @()
$cron_ok = 0; $cron_err = 0
foreach ($line in $cron_raw) {
    if ($line -match '^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}\s+(\S+).*?\b(ok|error)\b') {
        $name = $Matches[1]
        $status = $Matches[2]
        if ($status -eq 'ok') { $cron_ok++; $cl = 'ok'; $tg = 'OK' }
        else { $cron_err++; $cl = 'err'; $tg = 'ERROR' }
        $cron_rows += "<div class='status-row'><span class='dot $cl'></span>$name<span class='tag $cl'>$tg</span></div>"
    }
}
$cron_html = $cron_rows -join ""

$alerts = ""
if ($cron_err -gt 0) { $alerts += "<div class='alert warn'>$cron_err cron tasks with errors</div>" }

# Capabilities
$cap_html = ""
$cap_file = "$ws\memory\evolution\capability-state.json"
if (Test-Path $cap_file) {
    try {
        $cap = Get-Content $cap_file -Raw -Encoding UTF8 | ConvertFrom-Json
        $lvl_color = @{recorded="orange"; practiced="blue"; passed="green"; generalized="purple"}
        foreach ($c in $cap.capabilities) {
            $cname = $c.name
            $lv = $c.level
            $clr = $lvl_color[$lv]
            $cap_html += "<div class='status-row'><span class='dot $clr'></span>$cname<span style='margin-left:auto;font-size:0.72rem;color:var(--muted)'>$lv</span></div>"
        }
    } catch { }
}

$html = @"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OpenClaw Dashboard</title>
<style>
  :root { --bg:#0d1117; --card:#161b22; --border:#30363d; --text:#c9d1d9; --muted:#8b949e; --accent:#58a6ff; --green:#3fb950; --orange:#d2991d; --red:#f85149; --purple:#a371f7; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif; line-height:1.5; padding:2rem; }
  .container { max-width:960px; margin:0 auto; }
  h1 { font-size:1.5rem; font-weight:600; margin-bottom:0.15rem; }
  .subtitle { color:var(--muted); font-size:0.82rem; margin-bottom:1.25rem; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(175px,1fr)); gap:0.75rem; margin-bottom:1.5rem; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:8px; padding:1rem; }
  .card .label { color:var(--muted); font-size:0.68rem; text-transform:uppercase; letter-spacing:0.05em; }
  .card .value { font-size:1.5rem; font-weight:700; margin:0.1rem 0; }
  .card .detail { color:var(--muted); font-size:0.75rem; }
  .card.g .value { color:var(--green); }
  .card.b .value { color:var(--accent); }
  .card.p .value { color:var(--purple); }
  .card.o .value { color:var(--orange); }
  .section { margin-bottom:1.75rem; }
  .section h2 { font-size:1rem; font-weight:600; margin-bottom:0.65rem; padding-bottom:0.4rem; border-bottom:1px solid var(--border); }
  .status-row { display:flex; align-items:center; gap:0.5rem; padding:0.25rem 0; font-size:0.82rem; border-bottom:1px solid rgba(48,54,61,0.5); }
  .status-row:last-child { border:none; }
  .dot { width:6px; height:6px; border-radius:50%; flex-shrink:0; margin-right:0.15rem; }
  .dot.ok { background:var(--green); }
  .dot.err { background:var(--red); }
  .dot.orange { background:var(--orange); }
  .dot.blue { background:var(--accent); }
  .dot.purple { background:var(--purple); }
  .tag { display:inline-block; font-size:0.64rem; padding:0.05rem 0.35rem; border-radius:3px; margin-left:auto; font-weight:500; }
  .tag.ok { background:rgba(63,185,80,0.12); color:var(--green); }
  .tag.err { background:rgba(248,81,73,0.12); color:var(--red); }
  .alert { padding:0.5rem 0.8rem; border-radius:6px; margin-bottom:0.75rem; font-size:0.8rem; }
  .alert.warn { background:rgba(210,153,29,0.08); border:1px solid rgba(210,153,29,0.2); color:var(--orange); }
  .clip { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:420px; }
  .footer { text-align:center; color:var(--muted); font-size:0.68rem; margin-top:2rem; padding-top:1rem; border-top:1px solid var(--border); }
</style>
</head>
<body>
<div class="container">

<h1>OpenClaw Dashboard</h1>
<div class="subtitle">$ver &middot; $hn &middot; $now</div>

<div class="grid">
  <div class="card b"><div class="label">Memory Files</div><div class="value">$mf</div><div class="detail">Indexed documents</div></div>
  <div class="card g"><div class="label">Memory Chunks</div><div class="value">$mc</div><div class="detail">bge-m3:latest &middot; 1024d</div></div>
  <div class="card p"><div class="label">Skills</div><div class="value">$sc</div><div class="detail">Custom skills</div></div>
  <div class="card o"><div class="label">Daily Logs</div><div class="value">$dc</div><div class="detail">$dc records</div></div>
</div>

$alerts

<div class="section">
  <h2>Cron Tasks</h2>
  <div class="card">$cron_html</div>
</div>

<div class="section">
  <h2>Capability Evolution (v5)</h2>
  <div class="card">$cap_html</div>
</div>

<div class="section">
  <h2>Data Inventory</h2>
  <div class="grid">
    <div class="card p"><div class="label">Evolution</div><div class="value">$ec</div><div class="detail">$oc observations</div></div>
    <div class="card b"><div class="label">Daily Logs</div><div class="value">$dc</div><div class="detail">memory/daily/</div></div>
    <div class="card g"><div class="label">Topics</div><div class="value">$tc</div><div class="detail">memory/topics/</div></div>
  </div>
</div>

<div class="section">
  <h2>Recent Memory Files</h2>
  <div class="card">$rf_html</div>
</div>

<div class="section">
  <h2>Recent Daily Logs</h2>
  <div class="card">$df_html</div>
</div>

<div class="footer">Auto-generated &middot; Refreshed after each conversation</div>

</div>
</body>
</html>
"@

[System.IO.File]::WriteAllText($out, $html, [System.Text.UTF8Encoding]::new($false))
Write-Host "Dashboard: $out"
Write-Host "Memory: $mf files / $mc chunks | Evolution: $ec files | Skills: $sc | Daily: $dc logs"
Write-Host "Cron: $cron_ok OK / $cron_err errors"
