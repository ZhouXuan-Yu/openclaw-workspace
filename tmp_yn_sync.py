import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from tools.younavi_bridge import YouNavi
yn = YouNavi()

print("=== channel sync --all ===")
print(json.dumps(yn.channel_sync_all(), ensure_ascii=False))

for ch in ["tencent_meeting", "feishu_miaoji", "dingding_shanji", "plaud", "plaudcn"]:
    print(f"=== sync {ch} ===")
    print(json.dumps(yn.channel_sync(ch), ensure_ascii=False))

print("=== task_list ===")
print(json.dumps(yn.task_list(), ensure_ascii=False))
