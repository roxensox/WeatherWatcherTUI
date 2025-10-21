import sqlite3, importlib.resources as resources


def get_db_conn():
    root = __package__.split('.')[0]
    db_path = resources.files(root).joinpath("ww.db")
    return sqlite3.connect(db_path)


def save_location(loc: str):
    check = "SELECT id FROM locations WHERE location = ?"
    sql = "INSERT INTO locations (location) VALUES (?)"

    db_conn = get_db_conn()
    results = db_conn.execute(check, (loc,)).fetchall()

    if len(results) == 0:
        db_conn.execute(sql, (loc,))
        db_conn.commit()

    db_conn.close()
