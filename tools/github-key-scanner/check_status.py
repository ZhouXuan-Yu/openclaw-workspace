import json
h = json.loads(open("tools/github-key-scanner/scan_history.json", encoding="utf-8").read())
print(f"总key数: {len(h['seen_keys'])}")
print(f"日志条目数: {len(h['log_entries'])}")
# 打印最后一条日志
if h['log_entries']:
    e = h['log_entries'][-1]
    print(f"最后日期: {e['date']}, total: {e['total_found']}, new: {e['new_found']}, entries: {len(e['entries'])}")
