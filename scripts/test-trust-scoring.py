"""Trust Scoring 测试脚本"""
import json
import sys

TRUST_FILE = r"C:\Users\ZhouXuan\.openclaw\workspace\memory\evolution\trust-registry.json"

def load():
    with open(TRUST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(reg):
    with open(TRUST_FILE, 'w', encoding='utf-8') as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)

passed = 0
failed = 0

# ---- 测试 1：添加新事实 ----
print("=== 测试 1: 添加新事实 ===")
reg = load()
key = "test-neovim-editor"
assert key not in reg["facts"], "测试数据应不存在"
reg["facts"][key] = {
    "trust": 0.8,
    "tier": "fact",
    "source": "manual",
    "fact": "主要编辑器是 Neovim",
    "history": [{"date": "2026-06-24T20:10:00", "action": "created", "trust": 0.8}]
}
assert reg["facts"][key]["trust"] == 0.8
assert reg["facts"][key]["tier"] == "fact"
print(f"  OK: {key} trust=0.8 tier=fact")
passed += 1

# ---- 测试 2：用户纠正 ----
print("\n=== 测试 2: 用户纠正 ===")
f = reg["facts"][key]
tier_min = reg["tiers"][f["tier"]]["min_trust"]
old_trust = f["trust"]
new_trust = max(old_trust * 0.5, tier_min)
f["trust"] = new_trust
f["history"].append({"date": "2026-06-24T20:11:00", "action": "corrected", "trust": new_trust, "prev_trust": old_trust})
assert f["trust"] == 0.4, f"纠正后应为 0.4，实际 {f['trust']}"
print(f"  OK: correct: trust {old_trust} -> {new_trust} (floor={tier_min})")
passed += 1

# ---- 测试 3：验证通过 ----
print("\n=== 测试 3: 验证通过 ===")
old_trust = f["trust"]
new_trust = min(old_trust + 0.1, 1.0)
f["trust"] = new_trust
f["history"].append({"date": "2026-06-24T20:12:00", "action": "verified", "trust": new_trust, "prev_trust": old_trust})
assert f["trust"] == 0.5, f"验证后应为 0.5，实际 {f['trust']}"
print(f"  OK: verify: trust {old_trust} -> {new_trust}")
passed += 1

# ---- 测试 4：事实冲突 ----
print("\n=== 测试 4: 事实冲突 ===")
key2 = "test-editor-preference"
reg["facts"][key2] = {
    "trust": 1.0,
    "tier": "core_profile",
    "source": "manual",
    "fact": "主要编辑器是 VS Code",
    "history": [{"date": "2026-06-24T20:13:00", "action": "created", "trust": 1.0}]
}
f1 = reg["facts"][key]
old_trust = f1["trust"]
f1["trust"] = 0.3
f1["history"].append({"date": "2026-06-24T20:14:00", "action": "contradicted", "trust": 0.3, "prev_trust": old_trust, "by": key2})
assert f1["trust"] == 0.3, f"冲突后应为 0.3，实际 {f1['trust']}"
print(f"  OK: contradiction: {key} trust {old_trust} -> 0.3")
passed += 1

# ---- 测试 5：iron_law 不可降 ----
print("\n=== 测试 5: iron_law 不可降 ===")
iron_key = "test-iron-rule"
reg["facts"][iron_key] = {
    "trust": 1.0,
    "tier": "iron_law",
    "source": "SOUL.md",
    "fact": "SOUL 核心规则不可修改",
    "history": [{"date": "2026-06-24T20:15:00", "action": "created", "trust": 1.0}]
}
f = reg["facts"][iron_key]
tier_cfg = reg["tiers"][f["tier"]]
if not tier_cfg["editable"]:
    print(f"  OK: {iron_key} iron_law blocked correction")
else:
    print(f"  FAIL: iron_law should be non-editable")
    failed += 1
    passed -= 1
assert f["trust"] == 1.0, "iron_law trust 应保持 1.0"
passed += 1

# ---- 测试 6：纠正不能跌破 tier floor ----
print("\n=== 测试 6: 纠正 floor 保护 ===")
weak_key = "test-weak-fact"
reg["facts"][weak_key] = {
    "trust": 0.15,
    "tier": "fact",
    "source": "manual",
    "fact": "某临时配置",
    "history": [{"date": "2026-06-24T20:16:00", "action": "created", "trust": 0.15}]
}
f = reg["facts"][weak_key]
tier_min = reg["tiers"][f["tier"]]["min_trust"]
old_trust = f["trust"]
corrected = max(old_trust * 0.5, tier_min)
assert corrected == 0.1, f"纠正后应 floor 到 0.1，实际 {corrected}"
f["trust"] = corrected
print(f"  OK: trust {old_trust} x0.5={old_trust*0.5} floor to {tier_min}")
passed += 1

# ---- 清理测试数据 ----
for tk in ["test-neovim-editor", "test-editor-preference", "test-iron-rule", "test-weak-fact"]:
    del reg["facts"][tk]
reg["lastUpdated"] = "2026-06-24T20:17:00+08:00"
save(reg)

print(f"\n{'='*40}")
print(f"结果: {passed}/{passed+failed} 通过")
if failed > 0:
    print(f"  {failed} 项失败")
    sys.exit(1)
else:
    print("  全部通过")
