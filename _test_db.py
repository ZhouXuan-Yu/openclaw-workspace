import sqlite3

# Read OpenHuman memory.db
conn = sqlite3.connect(r'C:\Users\ZhouXuan\.openhuman\users\6a12f57084ae4d690e684277\workspace\memory\memory.db')
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print('Tables:', [t[0] for t in tables])

cur.execute('SELECT COUNT(*) FROM memory_docs')
print('memory_docs rows:', cur.fetchone()[0])

cur.execute('SELECT * FROM memory_docs LIMIT 3')
for row in cur.fetchall():
    print('Row:', row)

cur.execute('SELECT COUNT(*) FROM vector_chunks')
print('vector_chunks rows:', cur.fetchone()[0])

cur.execute('PRAGMA table_info(memory_docs)')
for col in cur.fetchall():
    print('Column:', col)

conn.close()
