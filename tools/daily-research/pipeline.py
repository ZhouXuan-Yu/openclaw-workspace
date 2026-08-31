#!/usr/bin/env python3
"""
每日深度调研 — Q0 数据管线
========================
纯本地文件操作 + 工具状态检查。
数据采集由 cron agent 的 web_search/web_fetch 工具完成，
本脚本负责：
  1. 管线健康检查
  2. 数据持久化（接收 agent 写入的结构化数据）
  3. 状态汇总
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent.parent
DAILY_DIR = WORKSPACE / "memory" / "daily"
EVOLUTION_DIR = WORKSPACE / "memory" / "evolution"
RESEARCH_DIR = DAILY_DIR / "research"
PIPELINE_HEALTH = EVOLUTION_DIR / "pipeline-health.json"

# =============================================================
# 1. 管线健康检查
# =============================================================

def do_health():
    """输出管线健康状态（JSON），供 agent 判断"""
    ensure_dir()
    result = {
        "timestamp": now(),
        "date": today(),
        "pipeline_health_exists": PIPELINE_HEALTH.exists(),
        "backends": {}
    }

    if PIPELINE_HEALTH.exists():
        try:
            data = json.loads(PIPELINE_HEALTH.read_text(encoding="utf-8"))
            platforms = data.get("platforms", {})
            active = {k: v.get("active_backend", "?") for k, v in platforms.items()}
            result["backends"] = active
        except:
            pass

    out = stage("health")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


# =============================================================
# 2. 保存数据（由 agent 调用）
# =============================================================

def save_social(data_json):
    """保存社会监听数据"""
    ensure_dir()
    out = stage("social")
    data = {"timestamp": now(), "date": today(), "sources": safe_parse(data_json)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"saved": str(out), "sources": len(data["sources"])}


def save_websearch(data_json):
    """保存 web_search 采集结果"""
    ensure_dir()
    out = stage("websearch")
    data = {"timestamp": now(), "date": today(), "results": safe_parse(data_json)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"saved": str(out), "results": len(data["results"])}


def save_younavi(data_json):
    """保存 YouNavi 研究结果"""
    ensure_dir()
    out = stage("younavi")
    data = {"timestamp": now(), "date": today(), "research": safe_parse(data_json)}
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"saved": str(out)}


# =============================================================
# 3. 数据读取与摘要
# =============================================================

def read_all():
    """读取今天所有已采集的阶段数据，输出整合 JSON"""
    ensure_dir()
    results = {}
    prefix = today()
    for f in sorted(RESEARCH_DIR.glob(f"{prefix}-*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            stage_name = f.name.replace(f"{prefix}-", "").replace(".json", "")
            results[stage_name] = data
        except:
            pass
    return results


def summary():
    """输出每日采集摘要（Markdown）"""
    data = read_all()
    lines = [
        f"# 📡 Q0 采集摘要 — {today()}",
        f"> 时间: {now()}",
        "",
        "## 管线状态",
    ]

    health = data.get("health", {})
    lines.append(f"- pipeline-health.json: {'✅ 存在' if health.get('pipeline_health_exists') else '❌ 不存在'}")
    backends = health.get("backends", {})
    for k, v in backends.items():
        lines.append(f"  - {k}: {v}")

    lines.append("")
    lines.append("## Track A — 社会监听")
    social = data.get("social", {})
    lines.append(f"- 来源数: {len(social.get('sources', []))}")

    lines.append("")
    lines.append("## Track B — 深度研究")
    younavi = data.get("younavi", {})
    lines.append(f"- YouNavi 研究数: {len(younavi.get('research', []))}")

    lines.append("")
    lines.append("## web_search")
    ws = data.get("websearch", {})
    lines.append(f"- 搜索结果数: {len(ws.get('results', []))}")

    lines.append("")
    lines.append("---")
    lines.append(f"📁 数据目录: {RESEARCH_DIR}/")

    return "\n".join(lines)


# =============================================================
# 工具函数
# =============================================================

def today():
    return datetime.now().strftime("%Y-%m-%d")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_dir():
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

def stage(name):
    return RESEARCH_DIR / f"{today()}-{name}.json"

def safe_parse(s):
    if isinstance(s, (list, dict)):
        return s
    try:
        return json.loads(s)
    except:
        return [{"raw": str(s)[:500]}]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--help"

    if cmd == "--health":
        r = do_health()
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif cmd == "--save-social":
        r = save_social(sys.stdin.read())
        print(json.dumps(r))

    elif cmd == "--save-websearch":
        r = save_websearch(sys.stdin.read())
        print(json.dumps(r))

    elif cmd == "--save-younavi":
        r = save_younavi(sys.stdin.read())
        print(json.dumps(r))

    elif cmd == "--summary":
        print(summary())

    elif cmd == "--data":
        print(json.dumps(read_all(), ensure_ascii=False, indent=2))

    else:
        print("用法:")
        print("  python tools/daily-research/pipeline.py --health     # 健康检查")
        print("  echo '...' | pipeline.py --save-social               # 保存社会数据")
        print("  echo '...' | pipeline.py --save-websearch            # 保存搜索数据")
        print("  pipeline.py --summary                                # 摘要")
        print("  pipeline.py --data                                   # 原始数据")
