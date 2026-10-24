import sqlite3, sys
con = sqlite3.connect('file:C:/Users/ZhouXuan/navi-ai/naviall.db?mode=ro', uri=True)
tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
print("TABLES:", len(tables))
print(tables)
