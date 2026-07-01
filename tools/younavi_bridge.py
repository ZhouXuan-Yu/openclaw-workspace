#!/usr/bin/env python3
"""
YouNavi CLI Bridge — OpenClaw 与 YouNavi 的桥梁层
解决 GBK 编码问题，提供干净的 Python 接口

用法:
    from younavi_bridge import YouNavi
    yn = YouNavi()
    result = yn.auth_me()
    result = yn.research_plan_only("主题")
    result = yn.task_list()
"""

import subprocess
import os
import json
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

CLI_PATH = r"D:\YouNavi\resources\backend\agent-cli.exe"
NAVI_DATA = r"C:\Users\ZhouXuan\navi-ai"
ARTIFACTS_DIR = os.path.join(NAVI_DATA, "generated_artifacts")

class YouNavi:
    """YouNavi CLI 的 Python 封装"""

    def __init__(self, cli_path: str = CLI_PATH, auto_start: bool = True):
        self.cli = cli_path
        self.auto_start = auto_start
        self.env = os.environ.copy()
        self.env["PYTHONIOENCODING"] = "utf-8"
        self.env["PYTHONUTF8"] = "1"

    def _run(self, args: List[str], timeout: int = 60) -> Dict[str, Any]:
        """执行 CLI 命令，返回结构化结果"""
        cmd = [self.cli, "-f", "json"]
        if not self.auto_start:
            cmd.append("--no-auto-start")
        cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=self.env,
                timeout=timeout
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip() if result.stderr else ""

            # 尝试解析 JSON
            data = None
            if stdout:
                try:
                    data = json.loads(stdout)
                except json.JSONDecodeError:
                    data = {"raw": stdout}

            return {
                "ok": result.returncode == 0 and (data is None or data.get("success", True)),
                "rc": result.returncode,
                "data": data,
                "stderr": stderr[:500] if stderr else None
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "rc": -1, "data": None, "stderr": f"timeout ({timeout}s)"}
        except Exception as e:
            return {"ok": False, "rc": -1, "data": None, "stderr": str(e)}

    # ─── 认证 ───────────────────────────────────────

    def auth_me(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self._run(["auth", "me"])

    # ─── 会话管理 ────────────────────────────────────

    def convo_list(self) -> Dict[str, Any]:
        """列出所有会话"""
        return self._run(["convo", "list"])

    def convo_show(self, convo_id: str) -> Dict[str, Any]:
        """查看会话详情"""
        return self._run(["convo", "show", convo_id])

    # ─── 深度研究 ────────────────────────────────────

    def research_plan_only(self, query: str) -> Dict[str, Any]:
        """生成研究计划（不执行）"""
        return self._run(["research", "plan-only", query], timeout=120)

    def research_start(self, query: str) -> Dict[str, Any]:
        """启动异步深度研究（plan + execute）"""
        return self._run(["research", "start", query], timeout=120)

    def research_report(self, task_id: str) -> Dict[str, Any]:
        """获取研究报告"""
        return self._run(["task", "report", task_id])

    def research_wait(self, task_id: str, poll_interval: int = 10, max_wait: int = 600) -> Dict[str, Any]:
        """等待研究任务完成并返回报告"""
        start = time.time()
        while time.time() - start < max_wait:
            result = self._run(["task", "show", task_id])
            if result["ok"]:
                status = result["data"].get("data", {}).get("status")
                if status == "finished":
                    return self.research_report(task_id)
                elif status in ("failed", "cancelled"):
                    return {"ok": False, "data": None, "stderr": f"task {status}"}
            time.sleep(poll_interval)
        return {"ok": False, "data": None, "stderr": f"wait timeout ({max_wait}s)"}

    def research_full(self, query: str, wait: bool = True) -> Dict[str, Any]:
        """完整研究流程：启动 → 等待 → 获取报告"""
        start_result = self.research_start(query)
        if not start_result["ok"]:
            return start_result

        task_id = start_result["data"].get("data", {}).get("task_id")
        if not task_id:
            return {"ok": False, "data": None, "stderr": "no task_id in response"}

        if wait:
            return self.research_wait(task_id)
        return {"ok": True, "data": {"task_id": task_id, "status": "started"}}

    # ─── 任务管理 ────────────────────────────────────

    def task_list(self) -> Dict[str, Any]:
        """列出所有任务"""
        return self._run(["task", "list"])

    def task_show(self, task_id: str) -> Dict[str, Any]:
        """查看任务详情"""
        return self._run(["task", "show", task_id])

    def task_report(self, task_id: str) -> Dict[str, Any]:
        """获取任务报告"""
        return self._run(["task", "report", task_id])

    def task_cancel(self, task_id: str) -> Dict[str, Any]:
        """取消任务"""
        return self._run(["task", "cancel", task_id])

    def task_wait(self, task_id: str, poll_interval: int = 5, max_wait: int = 300) -> Dict[str, Any]:
        """等待任务完成"""
        start = time.time()
        while time.time() - start < max_wait:
            result = self._run(["task", "show", task_id])
            if result["ok"]:
                status = result["data"].get("data", {}).get("status")
                if status == "finished":
                    return result
                elif status in ("failed", "cancelled"):
                    return {"ok": False, "data": None, "stderr": f"task {status}"}
            time.sleep(poll_interval)
        return {"ok": False, "data": None, "stderr": f"wait timeout ({max_wait}s)"}

    # ─── 记忆管理 ────────────────────────────────────

    def memory_list(self) -> Dict[str, Any]:
        """列出记忆文件"""
        return self._run(["memory", "list"])

    def memory_get(self, file_id: str) -> Dict[str, Any]:
        """获取记忆内容"""
        return self._run(["memory", "get", file_id])

    def memory_update(self, file_id: str, content: str) -> Dict[str, Any]:
        """更新记忆内容"""
        return self._run(["memory", "update", "--file", file_id, "--content", content])

    def memory_append(self, file_id: str, content: str) -> Dict[str, Any]:
        """追加记忆内容"""
        return self._run(["memory", "append", "--file", file_id, "--content", content])

    # ─── 笔记管理 ────────────────────────────────────

    def notes_list(self) -> Dict[str, Any]:
        """列出笔记"""
        return self._run(["notes", "list"])

    def notes_show(self, file_id: str) -> Dict[str, Any]:
        """查看笔记"""
        return self._run(["notes", "show", "--file", file_id])

    def notes_create(self, title: str, content: str) -> Dict[str, Any]:
        """创建笔记"""
        return self._run(["notes", "create", "--title", title, "--content", content])

    # ─── 文件管理 ────────────────────────────────────

    def file_list(self) -> Dict[str, Any]:
        """列出文件"""
        return self._run(["file", "list"])

    def file_upload(self, path: str) -> Dict[str, Any]:
        """上传文件"""
        return self._run(["file", "upload", path])

    # ─── 渠道同步 ────────────────────────────────────

    def channel_list(self) -> Dict[str, Any]:
        """列出支持的渠道"""
        return self._run(["channel", "list"])

    def channel_sync(self, channel: str) -> Dict[str, Any]:
        """同步指定渠道数据"""
        return self._run(["channel", "sync", "--name", channel])

    def channel_sync_all(self) -> Dict[str, Any]:
        """同步所有渠道"""
        return self._run(["channel", "sync", "--all"])

    # ─── 音频转写 ────────────────────────────────────

    def audio_transcribe(self, path: str) -> Dict[str, Any]:
        """转写音频文件"""
        return self._run(["audio", "transcribe", path], timeout=300)

    # ─── LLM 设置 ────────────────────────────────────

    def llm_show(self) -> Dict[str, Any]:
        """查看 LLM 设置"""
        return self._run(["llm", "show"])

    def llm_models(self) -> Dict[str, Any]:
        """列出可用模型"""
        return self._run(["llm", "models"])

    def llm_set(self, fast_model: str = None, full_model: str = None) -> Dict[str, Any]:
        """设置 LLM 模型"""
        args = ["llm", "set"]
        if fast_model:
            args.extend(["--fast-model", fast_model])
        if full_model:
            args.extend(["--full-model", full_model])
        return self._run(args)

    # ─── 监控目录 ────────────────────────────────────

    def dir_list(self) -> Dict[str, Any]:
        """列出监控目录"""
        return self._run(["dir", "list"])

    def dir_add(self, path: str) -> Dict[str, Any]:
        """添加监控目录"""
        return self._run(["dir", "add", path])

    # ─── 生成产物 ────────────────────────────────────

    def get_artifacts(self) -> List[Dict[str, Any]]:
        """获取所有生成的产物"""
        if not os.path.exists(ARTIFACTS_DIR):
            return []
        artifacts = []
        for f in os.listdir(ARTIFACTS_DIR):
            fp = os.path.join(ARTIFACTS_DIR, f)
            if os.path.isfile(fp):
                artifacts.append({
                    "name": f,
                    "path": fp,
                    "size": os.path.getsize(fp),
                    "modified": time.ctime(os.path.getmtime(fp))
                })
        return artifacts

    # ─── 高级工作流 ──────────────────────────────────

    def sync_meetings(self) -> Dict[str, Any]:
        """同步所有会议渠道并返回新内容"""
        return self.channel_sync_all()

    def daily_briefing(self) -> Dict[str, Any]:
        """生成每日简报：同步会议 + 获取任务 + 汇总"""
        # 1. 同步会议
        sync = self.sync_meetings()

        # 2. 获取任务列表
        tasks = self.task_list()

        # 3. 获取文件列表
        files = self.file_list()

        return {
            "ok": True,
            "data": {
                "sync": sync.get("data"),
                "tasks": tasks.get("data"),
                "files": files.get("data")
            }
        }


# ─── 命令行入口 ──────────────────────────────────────

if __name__ == "__main__":
    import sys

    yn = YouNavi()

    if len(sys.argv) < 2:
        print("用法: python younavi_bridge.py <command> [args...]")
        print("命令: auth_me, memory_list, notes_list, task_list, file_list,")
        print("      channel_list, llm_models, research_plan, research_start,")
        print("      sync_meetings, daily_briefing")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    method = getattr(yn, cmd, None)
    if not method:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    result = method(*args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
