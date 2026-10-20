"""GitHub 仓库追踪 — 监测目标仓库更新并推送通知"""
import requests, json, time, sys, os
from pathlib import Path
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

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
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def _html_repo_info(repo_full):
    """无 token 且 API 限流时，从 GitHub 网页内嵌 JSON 兜底读取 stars/forks。"""
    import re
    try:
        r = requests.get(f"https://github.com/{repo_full}", headers={"User-Agent": UA}, timeout=25)
        if r.status_code != 200:
            return None
        t = r.text
        stars = re.search(r'"stargazerCount":(\d+)', t)
        forks = re.search(r'"forksCount":(\d+)', t)
        if not stars:
            return None
        return {
            "stars": int(stars.group(1)),
            "forks": int(forks.group(1)) if forks else 0,
            "open_issues": 0,
            "pushed_at": "",
            "updated_at": "",
            "description": "",
            "size_kb": 0,
        }
    except Exception:
        return None

def _atom_commits(repo_full, per_page=10):
    """API 限流时从 commits atom feed 兜底读取提交。"""
    import re, html as _html
    for branch in ("main", "master"):
        try:
            r = requests.get(f"https://github.com/{repo_full}/commits/{branch}.atom",
                             headers={"User-Agent": UA}, timeout=25)
            if r.status_code != 200:
                continue
            out = []
            for e in re.findall(r"<entry>(.*?)</entry>", r.text, re.S)[:per_page]:
                tit = re.search(r"<title>(.*?)</title>", e, re.S)
                upd = re.search(r"<updated>(.*?)</updated>", e, re.S)
                link = re.search(r'<link[^>]*href="([^"]+)"', e)
                auth = re.search(r"<name>(.*?)</name>", e, re.S)
                url = link.group(1) if link else ""
                sha = url.rstrip("/").split("/")[-1][:7]
                out.append({
                    "sha": sha,
                    "date": (upd.group(1) if upd else "")[:19],
                    "author": _html.unescape((auth.group(1) if auth else "")),
                    "message": _html.unescape((tit.group(1) if tit else "")).strip()[:120],
                    "url": url,
                })
            if out:
                return out
        except Exception:
            continue
    return []

def get_repo_info(repo_full):
    r = requests.get(f"https://api.github.com/repos/{repo_full}", headers=gh_headers(), timeout=15)
    if r.status_code != 200:
        return _html_repo_info(repo_full)
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
        return _atom_commits(repo_full, per_page=per_page)
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
        
        # Filter commits we haven't seen: 新于上次记录的那条提交
        if prev_sha and any(c["sha"] == prev_sha for c in new_commits):
            idx = next(i for i, c in enumerate(new_commits) if c["sha"] == prev_sha)
            unseen = new_commits[:idx]
        elif prev_push:
            cutoff = prev_push.rstrip("Z")[:19]
            unseen = [c for c in new_commits if c["date"][:19] > cutoff]
        else:
            unseen = new_commits[:5]
        total_new_commits += len(unseen)

        # Get file changes if there are new commits
        changed_files = get_file_changes(repo, since_iso=prev_push) if unseen else []

        # Update state
        state["repos"][repo] = {
            "last_sha": new_commits[0]["sha"] if new_commits else prev_sha,
            "last_push": info["pushed_at"] or prev_push,
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
