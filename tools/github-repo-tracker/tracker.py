"""GitHub 仓库追踪 — 监测目标仓库更新并推送通知"""
import requests, json, time, sys
from pathlib import Path
from datetime import datetime

TRACKED_REPOS = [
    {
        "name": "awesome-generative-ai-guide",
        "url": "https://github.com/aishwaryanr/awesome-generative-ai-guide",
        "repo": "aishwaryanr/awesome-generative-ai-guide",
        "local_path": r"E:\Obsidian仓库\ZhouXuan私人领域\学习项目\awesome-generative-ai-guide",
        "obsidian_dir": r"E:\Obsidian仓库\ZhouXuan私人领域\学习笔记\GenAI",
        "tracking_since": "2026-06-29",
        "why": "GenAI 学习资源聚合 — 论文/面试题/课程/Notebook",
    },
]

STATE_FILE = Path("tools/github-repo-tracker/state.json")
LOG_FILE = Path("tools/github-repo-tracker/tracking_log.md")

def gh_headers():
    h = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Repo-Tracker/1.0"}
    return h

def get_repo_info(repo_full):
    r = requests.get(f"https://api.github.com/repos/{repo_full}", headers=gh_headers(), timeout=15)
    if r.status_code != 200:
        return None
    d = r.json()
    return {
        "stars": d.get("stargazers_count", 0),
        "forks": d.get("forks_count", 0),
        "open_issues": d.get("open_issues_count", 0),
        "pushed_at": d.get("pushed_at", ""),
        "updated_at": d.get("updated_at", ""),
        "description": d.get("description", ""),
        "size_kb": d.get("size", 0),
    }

def get_recent_commits(repo_full, since_iso=None, per_page=10):
    url = f"https://api.github.com/repos/{repo_full}/commits?per_page={per_page}"
    if since_iso:
        url += f"&since={since_iso}"
    r = requests.get(url, headers=gh_headers(), timeout=15)
    if r.status_code != 200:
        return []
    commits = r.json()
    if not isinstance(commits, list):
        return []
    return [{
        "sha": c["sha"][:7],
        "date": c["commit"]["author"]["date"],
        "author": c["commit"]["author"]["name"],
        "message": c["commit"]["message"].split("\n")[0][:120],
        "url": c["html_url"],
    } for c in commits]

def get_file_changes(repo_full, since_iso=None):
    """Get list of changed files from recent merges"""
    url = f"https://api.github.com/repos/{repo_full}/commits?per_page=5"
    if since_iso:
        url += f"&since={since_iso}"
    r = requests.get(url, headers=gh_headers(), timeout=15)
    if r.status_code != 200:
        return []
    
    changes = set()
    commits = r.json() if isinstance(r.json(), list) else []
    for c in commits[:3]:  # Check top 3 commits for files
        sha = c["sha"]
        cr = requests.get(f"https://api.github.com/repos/{repo_full}/commits/{sha}",
                        headers=gh_headers(), timeout=15)
        if cr.status_code == 200:
            cd = cr.json()
            for f in cd.get("files", [])[:20]:
                status = f.get("status", "?")
                fn = f.get("filename", "")
                if status == "added":
                    changes.add(f"➕ {fn}")
                elif status == "modified":
                    changes.add(f"📝 {fn}")
                elif status == "removed":
                    changes.add(f"➖ {fn}")
                else:
                    changes.add(f"   {fn}")
    return sorted(changes)[:30]

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"repos": {}, "last_check": ""}

def save_state(s):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")

def run():
    state = load_state()
    now = datetime.now()
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    results = []
    total_new_commits = 0

    for repo_cfg in TRACKED_REPOS:
        repo = repo_cfg["repo"]
        name = repo_cfg["name"]
        prev = state.get("repos", {}).get(repo, {})
        prev_sha = prev.get("last_sha", "")
        prev_push = prev.get("last_push", "")
        prev_stars = prev.get("stars", 0)

        info = get_repo_info(repo)
        if not info:
            results.append(f"❌ {name}: API 获取失败")
            continue

        # Stars delta
        star_delta = info["stars"] - prev_stars if prev_stars else 0

        # Commits since last check
        new_commits = get_recent_commits(repo, since_iso=prev_push, per_page=10)
        
        # Filter commits we haven't seen
        unseen = [c for c in new_commits if c["sha"] != prev_sha]
        total_new_commits += len(unseen)

        # Get file changes if there are new commits
        changed_files = get_file_changes(repo, since_iso=prev_push) if unseen else []

        # Update state
        state["repos"][repo] = {
            "last_sha": new_commits[0]["sha"] if new_commits else prev_sha,
            "last_push": info["pushed_at"],
            "last_check": now_iso,
            "stars": info["stars"],
            "forks": info["forks"],
        }

        # Build result
        star_str = f" (+{star_delta})" if star_delta > 0 else ""
        result = f"## {name}"
        result += f"\n⭐ {info['stars']:,}{star_str} | 🍴 {info['forks']:,} | 📦 {info['size_kb']:,}KB"
        
        if unseen:
            result += f"\n\n### {len(unseen)} 个新提交"
            for c in unseen[:5]:
                result += f"\n- [{c['date'][:10]}] {c['message'][:80]}"
            
            if changed_files:
                result += "\n\n### 变更文件"
                for f in changed_files[:10]:
                    result += f"\n- {f}"
                if len(changed_files) > 10:
                    result += f"\n- ... 等 {len(changed_files)} 个文件"
        else:
            result += "\n\n无新提交"

        results.append(result)

    state["last_check"] = now_iso
    save_state(state)

    # Generate report
    report = f"# 📡 GitHub 仓库追踪报告\n\n> {now.strftime('%Y-%m-%d %H:%M')} | 追踪 {len(TRACKED_REPOS)} 个仓库\n\n---\n\n"
    report += "\n\n---\n\n".join(results)
    report += f"\n\n---\n> 下次检查约 24h 后"

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(report, encoding="utf-8")

    # Sync to Obsidian
    for repo_cfg in TRACKED_REPOS:
        obs_dir = repo_cfg.get("obsidian_dir", "")
        if not obs_dir:
            continue
        obs_path = Path(obs_dir)
        obs_path.mkdir(parents=True, exist_ok=True)
        # Save today's report
        daily_file = obs_path / f"追踪-{repo_cfg['name']}-{now.strftime('%Y-%m-%d')}.md"
        daily_file.write_text(report, encoding="utf-8")
        # Update cumulative log
        cum_file = obs_path / f"追踪-{repo_cfg['name']}-完整记录.md"
        header = f"### {now.strftime('%Y-%m-%d %H:%M')}\n"
        if cum_file.exists():
            existing = cum_file.read_text(encoding="utf-8")
            cum_file.write_text(existing + "\n" + header + report, encoding="utf-8")
        else:
            cum_file.write_text(f"# {repo_cfg['name']} 追踪记录\n\n{header}{report}", encoding="utf-8")

    return total_new_commits, report

if __name__ == "__main__":
    new_count, report = run()
    print(report)
    print(f"\n总计 {new_count} 个新提交")
