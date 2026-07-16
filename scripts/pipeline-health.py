"""
Pipeline Health — 自进化内容生产链路健康管理
=============================================
使用方式: python scripts/pipeline-health.py <command> [args]

命令:
  status         显示所有平台健康状态
  check [platform]  测试指定或所有平台
  learn          根据检测结果自动更新路由表
  report         生成可读的健康报告

依赖: memory/evolution/pipeline-health.json
"""

import json, subprocess, sys, os, time
from datetime import datetime
from pathlib import Path

HEALTH_DB = Path.home() / ".openclaw" / "workspace" / "memory" / "evolution" / "pipeline-health.json"
PYTHON_SCRIPTS = Path.home() / "AppData" / "Roaming" / "Python" / "Python314" / "Scripts"

AGENT_REACH = PYTHON_SCRIPTS / "agent-reach.exe"
BILI = PYTHON_SCRIPTS / "bili.exe"
YTDLP = PYTHON_SCRIPTS / "yt-dlp.exe"

def load_health():
    if HEALTH_DB.exists():
        return json.loads(HEALTH_DB.read_text(encoding="utf-8"))
    return {"platforms": {}, "version": 1}

def save_health(data):
    HEALTH_DB.parent.mkdir(parents=True, exist_ok=True)
    data["version"] = 1
    HEALTH_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 已更新健康记录: {HEALTH_DB}")

def run_cmd(cmd, timeout=15):
    """安全执行命令，捕获输出"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
        return {"ok": r.returncode == 0, "stdout": r.stdout[:500], "stderr": r.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"ok": False, "stdout": "", "stderr": str(e)}

def test_platform(name, cmd, success_check=None):
    if success_check is None:
        success_check = lambda r: r["ok"]
    print(f"  Testing {name}... ", end="", flush=True)
    r = run_cmd(cmd)
    ok = success_check(r)
    print("✅" if ok else "❌")
    if not ok and r["stderr"]:
        print(f"    Error: {r['stderr'][:200]}")
    return ok, r

def cmd_status():
    """显示所有平台健康状态"""
    db = load_health()
    print("\n=== 📊 内容生产链路健康状态 ===\n")
    for platform, info in sorted(db["platforms"].items()):
        ab = info.get("active_backend") or "—"
        status = "✅" if ab != "—" else "❌"
        # 检查是否为兜底方案
        is_fallback = any(
            b.get("status") == "ok" 
            for b in info.get("backends", [])
        )
        if not is_fallback:
            status = "⚠️"
        print(f"  {status} {platform}: {ab}")
        for b in info.get("backends", []):
            icon = {"ok": "✅", "fail": "❌", "off": "⚪", "warn": "⚠️"}.get(b["status"], "❓")
            note = f" — {b.get('note','')}" if b.get('note') else ""
            print(f"    {icon} {b['name']} (fail×{b['fail_count']}){note}")
    wins = db.get("windows_patches", {})
    if wins.get("curl_is_alias"):
        print("\n  ⚠️ Windows: curl 是别名，必须用 curl.exe")
    print(f"\n  🔄 上次学习: {db.get('platforms',{}).get('bilibili',{}).get('learned_at','从未')}")

def cmd_check(platform_arg=None):
    """测试平台可用性"""
    print("\n=== 🔍 平台健康检查 ===")
    
    tests = [
        ("GitHub CLI", ["gh", "search", "repos", "test", "--limit", "1", "--json", "fullName"]),
        ("V2EX API", ["curl.exe", "-s", "--max-time", "10", "https://www.v2ex.com/api/topics/hot.json"]),
        ("Jina Reader (英文)", ["curl.exe", "-s", "--max-time", "10", "https://r.jina.ai/https://example.com"]),
        ("B站搜索 (bili-cli)", [str(BILI), "search", "test", "--type", "video", "-n", "1"]),
    ]
    
    results = {}
    for name, cmd in tests:
        ok, r = test_platform(name, cmd)
        results[name] = ok
    
    print(f"\n结果: {sum(results.values())}/{len(results)} 通过")
    return results

def cmd_learn():
    """从测试结果学习，自动更新路由表"""
    print("\n=== 🧠 自进化学习 ===")
    db = load_health()
    results = cmd_check()
    
    # 定义平台映射
    mapping = {
        "GitHub CLI": "github",
        "V2EX API": "v2ex",
        "Jina Reader (英文)": "web_jina",
        "B站搜索 (bili-cli)": "bilibili",
    }
    
    changed = False
    for test_name, platform in mapping.items():
        ok = results.get(test_name, False)
        platforms = db.get("platforms", {})
        if platform not in platforms:
            continue
        backends = platforms[platform].get("backends", [])
        for b in backends:
            if ok:
                if b["status"] in ("fail", "off"):
                    b["status"] = "ok"
                    b["last_ok"] = datetime.now().isoformat()
                    b["fail_count"] = 0
                    b["success_count"] = (b.get("success_count", 0) + 1)
                    changed = True
                    print(f"  ✅ {platform}/{b['name']}: 已恢复 → ok")
                elif b["status"] == "ok":
                    b["success_count"] = (b.get("success_count", 0) + 1)
            else:
                b["fail_count"] = (b.get("fail_count", 0) + 1)
                b["last_fail"] = datetime.now().isoformat()
                if b["fail_count"] >= 3 and b.get("status") in ("ok", "warn"):
                    b["status"] = "fail"
                    changed = True
                    print(f"  ❌ {platform}/{b['name']}: 连续{b['fail_count']}次失败→标记为bad")
    
    if changed:
        save_health(db)
        print("  ✅ 路由表已自动更新")
    else:
        print("  ℹ️   无变更")
    
    return changed

def cmd_report():
    """生成人类可读报告"""
    status = cmd_status()
    print("\n优化建议:")
    db = load_health()
    off_platforms = [
        p for p, i in db.get("platforms", {}).items()
        if all(b.get("status") in ("off",) for b in i.get("backends", []))
    ]
    if off_platforms:
        print(f"  📦 以下平台需配置后使用: {', '.join(off_platforms)}")

if __name__ == "__main__":
    commands = {
        "status": cmd_status,
        "check": lambda: cmd_check(sys.argv[2] if len(sys.argv) > 2 else None),
        "learn": cmd_learn,
        "report": cmd_report,
    }
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"命令: {', '.join(commands.keys())}")
