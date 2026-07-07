"""Check available accounts for social platforms"""
import json
from pathlib import Path

cookies_dir = Path(__file__).parent.parent / "cookies"

for f in sorted(cookies_dir.glob("*_creator.json")):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        account = d.get("account_name", d.get("nickname", "?"))
        print(f"{f.stem:40s} account={account}")
    except Exception as e:
        print(f"{f.stem:40s} ERROR: {e}")
