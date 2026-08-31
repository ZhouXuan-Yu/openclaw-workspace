#!/usr/bin/env python3
"""Check YouNavi DB for cached data and generate report from local sources."""
import sqlite3, os, json, glob
from datetime import datetime

navi_data = r"C:\Users\ZhouXuan\navi-ai"
found_dbs = []

# Find all DB files
for root, dirs, files in os.walk(navi_data):
    for f in files:
        if f.endswith(".db"):
            found_dbs.append(os.path.join(root, f))

found_dbs.sort()
print(f"Found {len(found_dbs)} DB files")

for db_path in found_dbs:
    fname = os.path.basename(db_path)
    size = os.path.getsize(db_path)
    print(f"\n--- {fname} ({size/1024:.0f} KB) ---")
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"  Tables: {tables}")
        
        for tbl in tables[:10]:  # limit to 10 tables
            try:
                cur.execute(f"SELECT COUNT(*) FROM \"{tbl}\"")
                cnt = cur.fetchone()[0]
                print(f"  {tbl}: {cnt} rows")
                
                # Show columns
                cur.execute(f"PRAGMA table_info(\"{tbl}\")")
                cols = [r[1] for r in cur.fetchall()]
                print(f"    Columns: {cols}")
                
                # Show sample
                cur.execute(f"SELECT * FROM \"{tbl}\" LIMIT 2")
                rows = cur.fetchall()
                if rows:
                    print(f"    Sample: {rows[0][:3]}")
            except Exception as e:
                print(f"  {tbl}: error - {e}")
        
        conn.close()
    except Exception as e:
        print(f"  Error: {e}")

# Also check generated_artifacts
artifacts_dir = os.path.join(navi_data, "generated_artifacts")
if os.path.isdir(artifacts_dir):
    files = [f for f in os.listdir(artifacts_dir) if f.endswith(".md")]
    print(f"\n--- Generated Artifacts ({len(files)} .md files) ---")
    for f in sorted(files, reverse=True)[:10]:
        fpath = os.path.join(artifacts_dir, f)
        mtime = os.path.getmtime(fpath)
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        print(f"  {f} ({mtime_str}, {os.path.getsize(fpath)/1024:.0f} KB)")
