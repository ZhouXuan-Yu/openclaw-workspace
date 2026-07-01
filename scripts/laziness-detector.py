"""
惰性检测器执行引擎 v1
从 hooks/laziness-detectors.yaml 加载配置，对会话日志进行实时检测。
借鉴 SCALE Engine 退出码协议: exit 0=allow, exit 2=block。
"""
import yaml
import json
import re
import sys
import os
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", r"C:\Users\ZhouXuan\.openclaw\workspace"))

def load_config():
    cfg_path = WORKSPACE / "hooks" / "laziness-detectors.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_session_log():
    """加载当前会话的工具调用日志用于检测"""
    log_path = WORKSPACE / "memory" / "detector-logs" / "session-log.jsonl"
    if not log_path.exists():
        return []
    events = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events

class DetectorEngine:
    """惰性检测引擎，输出 exit 0 或 exit 2"""

    def __init__(self, config):
        self.cfg = config
        self.events = load_session_log()
        self.results = []
        self.blocked = False

    def hash_args(self, args):
        return hashlib.md5(json.dumps(args, sort_keys=True).encode()).hexdigest()[:8]

    # ===== 检测器1: 暴力重试 =====
    def check_brute_retry(self):
        c = self.cfg.get("brute_retry", {})
        if not c.get("enabled", True):
            return

        window = timedelta(minutes=c.get("window_minutes", 3))
        threshold = c.get("threshold", 3)
        now = datetime.now(timezone.utc)

        # 统计最近窗口内的 exec 调用
        exec_calls = defaultdict(list)
        for e in self.events:
            if e.get("tool") != "exec":
                continue
            ts = datetime.fromisoformat(e["timestamp"])
            if now - ts > window:
                continue
            key = e.get("command", "")
            exec_calls[key].append(e)

        for cmd, calls in exec_calls.items():
            if len(calls) >= threshold:
                failures = [c for c in calls if c.get("exit_code", 0) != 0]
                # 检查是否有中间读取操作
                has_investigation = any(
                    e.get("tool") in ("read", "memory_search", "web_search")
                    for e in self.events
                    if calls[0]["timestamp"] < e["timestamp"] < calls[-1]["timestamp"]
                )
                if len(failures) >= 2 and not has_investigation:
                    self._block("brute_retry",
                        f"暴力重试：命令 '{cmd[:80]}' 在 {c['window_minutes']} 分钟内执行了 {len(calls)} 次 ({len(failures)} 次失败) 且无中间调查",
                        "换策略前说明新假设；Read 错误日志或 Grep 类似模式")

    # ===== 检测器2: 工具闲置 =====
    def check_idle_tool(self):
        c = self.cfg.get("idle_tool", {})
        if not c.get("enabled", True):
            return

        # 检查：exec 失败后紧接着 edit/write（中间无 read/grep/search）
        for i, e in enumerate(self.events):
            if e.get("tool") != "exec" or e.get("exit_code", 0) == 0:
                continue
            # 找到下一个操作
            if i + 1 >= len(self.events):
                continue
            next_e = self.events[i + 1]
            if next_e.get("tool") in ("edit", "write"):
                self._warn("idle_tool",
                    "工具闲置：exec 失败后立即执行 edit/write，未做任何调查",
                    "先 Read 失败输出或 Grep 相关模式")
                return

    # ===== 检测器3: 忙碌假象 =====
    def check_busy_loop(self):
        c = self.cfg.get("busy_loop", {})
        if not c.get("enabled", True):
            return

        # 统计每文件的连续 edit 次数
        file_edits = defaultdict(list)
        for e in self.events:
            if e.get("tool") == "edit":
                fp = e.get("file_path", "unknown")
                old = hashlib.md5((e.get("old_text", "") or "").encode()).hexdigest()[:8]
                new = hashlib.md5((e.get("new_text", "") or "").encode()).hexdigest()[:8]
                file_edits[fp].append({"ts": e["timestamp"], "old": old, "new": new})

        for fp, edits in file_edits.items():
            if len(edits) < 4:
                continue
            # 检测循环：是否有相同的 old→new 对
            seen = set()
            for ed in edits:
                pair = f"{ed['old']}:{ed['new']}"
                if pair in seen:
                    self._block("busy_loop",
                        f"忙碌假象：文件 {fp} 的修改在两种状态间反复，无新信息产生",
                        "Read 相关文件 / Grep 类似模式 / 换思路")
                    return
                seen.add(pair)

    # ===== 检测器4: 声称完成但未验证 =====
    def check_premature_done(self):
        c = self.cfg.get("premature_done", {})
        if not c.get("enabled", True):
            return

        edits = [e for e in self.events if e.get("tool") in ("edit", "write")]
        if not edits:
            return

        verifications = [e for e in self.events
                        if e.get("tool") == "exec"
                        and re.search(r'test|lint|build|typecheck', e.get("command", ""), re.I)]

        # 情况1：完全未验证
        if not verifications:
            self._block("premature_done",
                f"声称完成但未验证：修改了 {len(edits)} 处代码但未运行任何 test/lint/build",
                "test && lint && build")
            return

        # 情况2：验证在编辑之前
        last_edit_ts = max(e["timestamp"] for e in edits)
        last_verify_ts = max(e["timestamp"] for e in verifications)
        if last_verify_ts < last_edit_ts:
            self._block("premature_done",
                "验证命令在最后一次编辑之前运行，请重新验证",
                "重新运行 test && lint && build")
            return

    # ===== 检测器5: 甩锅检测 =====
    def check_blame_shift(self):
        c = self.cfg.get("blame_shift", {})
        if not c.get("enabled", True):
            return

        patterns = [
            r"可能是环境问题",
            r"建议(你|您)?手动",
            r"maybe (an?|the) (environment|version|setup)",
            r"not sure why",
            r"unable to (determine|figure out|resolve)",
            r"这可能是.*问题",
            r"不确定是不是",
        ]

        for e in self.events:
            output = e.get("output", "") or e.get("stderr", "") or ""
            for pat in patterns:
                if re.search(pat, output, re.I):
                    # 检查是否做了足够验证（≥2 次调查操作）
                    investigations = [ev for ev in self.events
                                    if ev.get("tool") in ("read", "grep", "memory_search", "web_search")]
                    if len(investigations) < 2:
                        self._warn("blame_shift",
                            f"甩锅迹象：'{re.search(pat, output, re.I).group()}' — 未做足够验证就下结论",
                            "至少验证：1.版本 2.依赖 3.能重现问题。证据齐了再下结论")
                        return

    # ===== 检测器6: 被动等待 =====
    def check_passive_wait(self):
        c = self.cfg.get("passive_wait", {})
        if not c.get("enabled", True):
            return

        edits = [e for e in self.events if e.get("tool") in ("edit", "write")]
        if not edits:
            return

        last_edit_ts = max(e["timestamp"] for e in edits)
        # 编辑之后是否有泛化检查
        post_checks = [e for e in self.events
                      if e["timestamp"] > last_edit_ts
                      and e.get("tool") in ("grep", "memory_search", "web_search")
                      and any(kw in (e.get("query", "") + e.get("command", "")).lower()
                             for kw in ["同类", "similar", "same pattern", "上下游", "规则", "rule", "泛化", "generalize"])]
        if not post_checks:
            self._block("passive_wait",
                f"被动等待：修完 {len(edits)} 处代码后未做泛化检查",
                "检查：1.同模块同类问题 2.上下游影响 3.能否添加检测规则防复发")

    # ===== 检测器7: 同文件连续修改 =====
    def check_same_file_edit(self):
        c = self.cfg.get("same_file_edit", {})
        if not c.get("enabled", True):
            return

        threshold = c.get("threshold", 3)
        file_edits = defaultdict(list)
        for e in self.events:
            if e.get("tool") == "edit":
                file_edits[e.get("file_path", "unknown")].append(e["timestamp"])

        for fp, timestamps in file_edits.items():
            if len(timestamps) < threshold:
                continue
            # 检查中间是否有调查操作
            has_investigation = any(
                e.get("tool") in ("read", "grep", "memory_search", "web_search", "web_fetch")
                for e in self.events
                if timestamps[0] < e["timestamp"] < timestamps[-1]
            )
            if not has_investigation:
                self._block("same_file_edit",
                    f"同文件连续修改：{fp} 已改 {len(timestamps)} 次且无新信息输入",
                    "Read 相关文件 / 换思路")

    # ===== 输出协议 =====
    def _block(self, detector, reason, suggestion=None):
        self.blocked = True
        self.results.append({
            "detector": detector,
            "decision": "block",
            "reason": reason,
            "suggestion": suggestion,
            "exit_code": 2
        })

    def _warn(self, detector, reason, suggestion=None):
        self.blocked = True  # warn 也标记但不改变 exit code
        self.results.append({
            "detector": detector,
            "decision": "warn",
            "reason": reason,
            "suggestion": suggestion
        })

    def run_all(self, hook_type="stop"):
        """运行所有检测器。hook_type: pre_tool | post_tool | stop"""
        if hook_type == "pre_tool":
            self.check_brute_retry()
            self.check_idle_tool()
            self.check_busy_loop()
            self.check_same_file_edit()
        elif hook_type == "post_tool":
            self.check_blame_shift()
        elif hook_type == "stop":
            self.check_premature_done()
            self.check_passive_wait()
        elif hook_type == "all":
            self.check_brute_retry()
            self.check_idle_tool()
            self.check_busy_loop()
            self.check_premature_done()
            self.check_blame_shift()
            self.check_passive_wait()
            self.check_same_file_edit()

    def report(self):
        """输出检测报告"""
        if not self.results:
            print(json.dumps({
                "decision": "allow",
                "reason": "所有检测器通过",
                "detectors_run": 7
            }))
            return 0

        blocks = [r for r in self.results if r.get("exit_code") == 2]
        warns = [r for r in self.results if r.get("decision") == "warn"]

        report = {
            "decision": "block" if blocks else ("warn" if warns else "allow"),
            "blocked_by": [r["detector"] for r in blocks],
            "warnings": [r["detector"] for r in warns],
            "details": self.results
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))

        if blocks:
            for b in blocks:
                print(f"\n[BLOCK] {b['detector']}: {b['reason']}", file=sys.stderr)
                if b.get("suggestion"):
                    print(f"  → {b['suggestion']}", file=sys.stderr)
            return 2  # exit 2 = block (Scale Shield 协议)
        if warns:
            for w in warns:
                print(f"\n[WARN] {w['detector']}: {w['reason']}", file=sys.stderr)
                if w.get("suggestion"):
                    print(f"  → {w['suggestion']}", file=sys.stderr)
            return 0  # warn 不退出
        return 0


def generate_test_events():
    """生成测试用的伪造事件日志，用于验证检测器"""
    base_ts = datetime.now(timezone.utc) - timedelta(minutes=2)
    events = [
        # 暴力重试测试: exec 同一命令 4 次
        {"tool": "exec", "command": "npm test -- --force", "exit_code": 1, "timestamp": (base_ts + timedelta(seconds=0)).isoformat()},
        {"tool": "exec", "command": "npm test -- --force", "exit_code": 1, "timestamp": (base_ts + timedelta(seconds=30)).isoformat()},
        {"tool": "exec", "command": "npm test -- --force", "exit_code": 1, "timestamp": (base_ts + timedelta(seconds=60)).isoformat()},
        {"tool": "exec", "command": "npm test -- --force", "exit_code": 1, "timestamp": (base_ts + timedelta(seconds=90)).isoformat()},
        # 甩锅测试
        {"tool": "exec", "command": "python script.py", "exit_code": 1, "output": "Error: 可能是环境问题导致的失败", "timestamp": (base_ts + timedelta(seconds=100)).isoformat()},
        # 声称完成但未验证: edit 后无 test
        {"tool": "edit", "file_path": "src/main.py", "old_text": "old", "new_text": "new", "timestamp": (base_ts + timedelta(seconds=110)).isoformat()},
        {"tool": "write", "file_path": "src/config.py", "timestamp": (base_ts + timedelta(seconds=120)).isoformat()},
        # 同文件连续修改: 3 次无调查
        {"tool": "edit", "file_path": "src/main.py", "old_text": "new", "new_text": "newer", "timestamp": (base_ts + timedelta(seconds=130)).isoformat()},
        {"tool": "edit", "file_path": "src/main.py", "old_text": "newer", "new_text": "newest", "timestamp": (base_ts + timedelta(seconds=140)).isoformat()},
    ]
    return events


if __name__ == "__main__":
    cfg = load_config()
    engine = DetectorEngine(cfg)

    hook_type = sys.argv[1] if len(sys.argv) > 1 else "all"

    if hook_type == "test":
        # 测试模式：生成伪造日志运行所有检测器
        test_events = generate_test_events()
        log_dir = WORKSPACE / "memory" / "detector-logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "session-log.jsonl"
        with open(log_file, "w", encoding="utf-8") as f:
            for e in test_events:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"写入 {len(test_events)} 条测试事件到 {log_file}")
        print("=" * 60)
        print("运行所有检测器...")
        print("=" * 60)
        engine.events = test_events
        engine.run_all("all")
        engine.report()
        print("\n" + "=" * 60)
        print("预期结果:")
        print("  brute_retry: BLOCK (同命令4次失败)")
        print("  blame_shift: WARN (可能是环境问题)")
        print("  premature_done: BLOCK (edit后无验证)")
        print("  same_file_edit: BLOCK (同文件3次改无调查)")
        print("=" * 60)
    else:
        engine.run_all(hook_type)
        code = engine.report()
        sys.exit(code)
