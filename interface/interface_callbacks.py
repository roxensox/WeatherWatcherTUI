import sqlite3


def get_db_conn():
    return sqlite3.connect("./ww.db")


def save_location(loc: str):
    check = "SELECT id FROM locations WHERE location = ?"
    sql = "INSERT INTO locations (location) VALUES (?)"

    db_conn = get_db_conn()
    results = db_conn.execute(check, (loc,)).fetchall()

    if len(results) == 0:
        db_conn.execute(sql, (loc,))
        db_conn.commit()

    db_conn.close()
