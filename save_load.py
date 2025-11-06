import sqlite3
import pygame
import sys
import math

import value

pygame.init()
import os


def infer_sqlite_type(value):
    if isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "REAL"
    elif isinstance(value, str):
        return "TEXT"
    else:
        return "BLOB"  # その他（画像など）も対応可能
    
def save(slot):
    #セーブスロット　012

    #データ
    data = [
        slot,
        value.deckcolor[slot],
        *value.deck[slot],
    ]

    #セーブ
    os.makedirs("save", exist_ok=True)  # フォルダがなければ作成

    # データベース接続（なければ自動で作成される）
    conn = sqlite3.connect(os.path.join("save", "save.db"))
    cursor = conn.cursor()             # SQLを操作するためのカーソルを取得

    #要素数が変わるときにいるけど要素数が変わらないならいらない
    cursor.execute(f"DROP TABLE IF EXISTS save{slot}")

    num_columns = len(data)
    columns = [f"col{i}" for i in range(1, num_columns + 1)]
    column_type = [infer_sqlite_type(val) for val in data]

    col_defs = ",\n    ".join([
        f"{columns[0]} INTEGER PRIMARY KEY"
    ] + [f"{name} {column_type}" for name in columns[1:]])

    sql = f"CREATE TABLE IF NOT EXISTS save{slot} (\n    {col_defs}\n)"
    cursor.execute(sql)

    placeholders = ', '.join(['?'] * len(data))  # "?, ?, ?, ..., ?" を自動生成

    sql = f"INSERT INTO save{slot} VALUES ({placeholders})"
    cursor.execute(sql, data)


    conn.commit()  # 保存（変更を確定）
    conn.close()   # 接続を終了

def load(slot):
    db_path = os.path.join("save", "save.db")
    if not os.path.exists(db_path):
        return  # ファイルがなければ何もせず終了

    conn = sqlite3.connect(db_path)


    #ロード
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM save{slot} WHERE col1 = ?", (slot,))
        row = cursor.fetchone()
    except sqlite3.OperationalError as e:
        return
    
    cursor.execute(f"PRAGMA table_info(save{slot})")
    columns_info = cursor.fetchall()
    columns = [col[1] for col in columns_info]

    cursor.execute(f"SELECT * FROM save{slot} WHERE col1 = ?", (slot,))
    row = cursor.fetchone()

    value.deckcolor[slot]=list(row)[1]
    value.deck[slot] = list(row[2:])

    conn.close()




