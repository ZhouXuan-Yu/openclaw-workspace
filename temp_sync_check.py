import sqlite3
import json
from datetime import datetime

db = r'C:\Users\ZhouXuan\navi-ai\naviall.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Get recent tasks
cur.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10")
tasks = [dict(r) for r in cur.fetchall()]

print("=== Recent Tasks ===")
for t in tasks:
    print(f"ID: {t.get('task_id','?')}")
    print(f"  Title: {t.get('title','?')}")
    print(f"  Status: {t.get('status','?')}")
    print(f"  Type: {t.get('task_type','?')}")
    print(f"  Created: {t.get('created_at','?')}")
    print(f"  Source: {t.get('source_channel','?')}")
    print()

# Get conversations (meetings)
cur.execute("SELECT * FROM conversations ORDER BY updated_at DESC LIMIT 5")
convs = [dict(r) for r in cur.fetchall()]

print("=== Recent Conversations ===")
for c in convs:
    print(f"ID: {c.get('conversation_id','?')}")
    print(f"  Title: {c.get('title','?')}")
    print(f"  Source: {c.get('source_type','?')} / {c.get('source_channel','?')}")
    print(f"  Updated: {c.get('updated_at','?')}")
    print()

# Count by status/stype
cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
print("=== Tasks by Status ===")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]}")

conn.close()
