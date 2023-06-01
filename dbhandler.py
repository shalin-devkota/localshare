import sqlite3

conn = sqlite3.connect("main.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS data (ip TEXT PRIMARY KEY, data TEXT )")
conn.commit()
conn.close()


def check_for_data(ip):
    print(ip)
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()

    cursor.execute("SELECT data FROM data WHERE ip = ?", (ip,))
    data = cursor.fetchone()

    return data


def update_or_add(ip, data):
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data WHERE ip = ? ", (ip,))
    cur_data = cursor.fetchone()
    if cur_data:
        cursor.execute("UPDATE data SET data = ? WHERE ip = ? ", (data, ip))
    else:
        cursor.execute("INSERT INTO data (ip,data) VALUES (?,?)", (ip, data))
    conn.commit()
    conn.close()
