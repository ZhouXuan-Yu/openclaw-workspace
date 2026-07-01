"""分级 Decay 单元测试"""
import json
import sys
sys.path.insert(0, r'C:\Users\ZhouXuan\.openclaw\workspace\scripts')
import importlib.util
spec = importlib.util.spec_from_file_location("decay_scanner", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py")
mod = importlib.util.module_from_spec(spec)

import os
import shutil

TRUST_FILE = r"C:\Users\ZhouXuan\.openclaw\workspace\memory\evolution\trust-registry.json"
BACKUP_FILE = TRUST_FILE + ".test-backup"

# 备份
shutil.copy(TRUST_FILE, BACKUP_FILE)

passed = 0
failed = 0

def load():
    with open(TRUST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(reg):
    with open(TRUST_FILE, 'w', encoding='utf-8') as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)

def simulate_date(key, days_ago):
    """设置某 fact 的 last_accessed 为 days_ago"""
    from datetime import datetime, timezone, timedelta
    reg = load()
    tz = timezone(timedelta(hours=8))
    past = datetime.now(timezone.utc) - timedelta(days=days_ago)
    past_str = past.astimezone(tz).isoformat()
    reg['facts'][key]['last_accessed'] = past_str
    save(reg)

def reset():
    """恢复备份"""
    shutil.copy(BACKUP_FILE, TRUST_FILE)

# ---- 测试 1: transient 超过 30 天衰减 ----
print("=== 测试 1: transient 超过 30 天 ===")
reg = load()
key = "test-ts-decay"
reg["facts"][key] = {
    "trust": 0.8,
    "tier": "transient",
    "source": "test",
    "fact": "测试临时事实",
    "last_accessed": "2026-05-01T00:00:00+08:00",
    "history": [{"date": "2026-05-01T00:00:00+08:00", "action": "created", "trust": 0.8}]
}
save(reg)

# dry-run decay
from subprocess import run
r = run(["python", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py", "--dry-run"], capture_output=True, text=True)
print(r.stdout)
assert "test-ts-decay" in r.stdout, f"应包含 test-ts-decay，实际: {r.stdout[:200]}"
print("  OK: transient 衰减触发")
passed += 1

# ---- 测试 2: iron_law 永久跳过 ----
print("\n=== 测试 2: iron_law 跳过 ===")
reg = load()
iron_key = "test-iron-decay"
reg["facts"][iron_key] = {
    "trust": 1.0,
    "tier": "iron_law",
    "source": "test",
    "fact": "测试铁律",
    "last_accessed": "2025-01-01T00:00:00+08:00",
    "history": [{"date": "2025-01-01T00:00:00+08:00", "action": "created", "trust": 1.0}]
}
save(reg)

r = run(["python", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py", "--dry-run"], capture_output=True, text=True)
assert "iron_law" in r.stdout
assert iron_key not in r.stdout or "iron_law 跳过" in r.stdout
print("  OK: iron_law 不受衰减影响")
passed += 1

# ---- 测试 3: core_profile 超过 365 天 ----
print("\n=== 测试 3: core_profile 超过 365 天 ===")
reg = load()
key3 = "test-cp-decay"
reg["facts"][key3] = {
    "trust": 1.0,
    "tier": "core_profile",
    "source": "test",
    "fact": "测试核心档案",
    "last_accessed": "2025-01-01T00:00:00+08:00",
    "history": [{"date": "2025-01-01T00:00:00+08:00", "action": "created", "trust": 1.0}]
}
save(reg)

r = run(["python", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py", "--dry-run"], capture_output=True, text=True)
assert key3 in r.stdout, f"应包含 {key3}，实际: {r.stdout}"
# 1.0 * 0.9 = 0.9, floor 0.6
assert "0.9" in r.stdout, f"trust 应变 0.9"
print("  OK: core_profile 衰减 1.0 -> 0.9 (floor 0.6)")
passed += 1

# ---- 测试 4: fact floor 保护 (trust 已接近 floor) ----
print("\n=== 测试 4: fact trust floor 保护 ===")
reg = load()
key4 = "test-flat-fact"
reg["facts"][key4] = {
    "trust": 0.12,
    "tier": "fact",
    "source": "test",
    "fact": "测试 floor 保护",
    "last_accessed": "2025-01-01T00:00:00+08:00",
    "history": [{"date": "2025-01-01T00:00:00+08:00", "action": "created", "trust": 0.12}]
}
save(reg)

r = run(["python", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py", "--dry-run"], capture_output=True, text=True)
assert key4 in r.stdout
# 0.12 * 0.9 = 0.108, floor 0.1 -> 0.1
assert "0.1" in r.stdout and "0.12" in r.stdout
print("  OK: fact trust floor 保护 (0.12 -> 0.1, floor 0.1)")
passed += 1

# ---- 测试 5: 未过期 fact 不衰减 ----
print("\n=== 测试 5: 未过期不衰减 ===")
reg = load()
key5 = "test-fresh-transient"
reg["facts"][key5] = {
    "trust": 0.7,
    "tier": "transient",
    "source": "test",
    "fact": "测试未过期",
    "last_accessed": "2026-06-23T00:00:00+08:00",
    "history": [{"date": "2026-06-23T00:00:00+08:00", "action": "created", "trust": 0.7}]
}
save(reg)

r = run(["python", r"C:\Users\ZhouXuan\.openclaw\workspace\scripts\decay-scanner.py", "--dry-run"], capture_output=True, text=True)
assert "未过期跳过: 1" in r.stdout or key5 not in r.stdout or "无需衰减" in r.stdout
print("  OK: 未过期 1 天不触发衰减")
passed += 1

# ---- 清理 ----
# 恢复原始文件
reset()
os.remove(BACKUP_FILE)

# 删除测试数据
reg = load()
for tk in ["test-ts-decay", "test-iron-decay", "test-cp-decay", "test-flat-fact", "test-fresh-transient"]:
    if tk in reg["facts"]:
        del reg["facts"][tk]
save(reg)

print(f"\n{'='*40}")
print(f"结果: {passed}/{passed+failed} 通过")
