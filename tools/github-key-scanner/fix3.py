p = r'C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\daily_scan.py'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

old = """total_repos = len(set(v['repo'] for v in verified_sk.values()))
    lines = ["# GitHub 密钥泄露 - 总览", "",
             f"> ✅ 已验证有效: {len(verified_sk)} 密钥 | {total_repos} 仓库 | 更新: {h['last_scan']} | v4 ({ACTIVE_MONTHS}月活跃过滤)", "",
             "| 供应商 | 数量 | 详细文件 |",
             "|--------|------|----------|"]
    for prov, items in sorted(by_provider.items()):
        ps = prov.replace(" ", "_").replace("/", "-")
        lines.append(f"| {prov} | {len(items)} | [[GitHub泄露-{ps}]] |")
    lines.append("")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))

    print(f"📁 Obsidian exported: {len(by_provider)} provider files, {len(verified_sk)} valid keys → {OBSIDIAN_DIR}")"""

new = """total_repos = len(set(v['repo'] for v in sk.values()))
    verified_count = sum(1 for v in sk.values() if v.get("verified") == "valid")
    lines = ["# GitHub 密钥泄露 - 总览", "",
             f"> 总密钥: {len(sk)} | 已验证有效: {verified_count} | {total_repos} 仓库 | 更新: {h['last_scan']} | v4 ({ACTIVE_MONTHS}月活跃过滤)", "",
             "| 供应商 | 数量 | 有效 | 详细文件 |",
             "|--------|------|------|----------|"]
    for prov, items in sorted(by_provider.items()):
        ps = prov.replace(" ", "_").replace("/", "-")
        prov_verified = sum(1 for v in items if v.get("verified") == "valid")
        lines.append(f"| {prov} | {len(items)} | {prov_verified} | [[GitHub泄露-{ps}]] |")
    lines.append("")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))

    print(f"Obsidian exported: {len(by_provider)} provider files, {len(sk)} keys ({verified_count} verified) -> {OBSIDIAN_DIR}")"""

if old in c:
    c = c.replace(old, new)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK')
else:
    print('NOT FOUND')
    # show context
    idx = c.find('total_repos')
    print(repr(c[idx:idx+50]))
