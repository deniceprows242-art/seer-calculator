import sqlite3

ELVES_DATA = [
    ("雷伊", "电", None),
    ("盖亚", "战斗", None),
    ("布莱克", "暗影", None),
    ("卡修斯", "地面", "暗影"),
    ("缪斯", "超能", None),
    ("哈莫雷特", "龙", None),
    ("迈尔斯", "圣灵", None),
    ("瑞尔斯", "战斗", None),
    ("谱尼", "神灵", None),
    ("索伦森", "混沌", "圣灵"),
]

def init_database():
    print("正在连接数据库 seer_data.db ...")
    conn = sqlite3.connect("seer_data.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spirits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_cn TEXT NOT NULL,
            attribute1 TEXT NOT NULL,
            attribute2 TEXT
        )
    ''')

    print("清空旧数据...")
    cursor.execute('DELETE FROM spirits')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="spirits"')

    print("插入新数据...")
    count = 0
    for name, attr1, attr2 in ELVES_DATA:
        cursor.execute(
            'INSERT INTO spirits (name_cn, attribute1, attribute2) VALUES (?, ?, ?)',
            (name, attr1, attr2)
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"成功插入 {count} 个精灵")

if __name__ == "__main__":
    init_database()
