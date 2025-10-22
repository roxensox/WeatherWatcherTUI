import sqlite3, importlib.resources as resources


def get_db_conn()->sqlite3.Connection:
    '''
    Returns a connection to the database
    '''
    root = __package__.split('.')[0]
    db_path = resources.files(root).joinpath("ww.db")
    return sqlite3.connect(db_path)


def save_location(loc: str):
    '''
    Adds the current location to the database if it isn't 
    already saved
    '''
    check = "SELECT id FROM locations WHERE location = ?"
    sql = "INSERT INTO locations (location) VALUES (?)"

    db_conn = get_db_conn()
    results = db_conn.execute(check, (loc,)).fetchall()

    if len(results) == 0:
        db_conn.execute(sql, (loc,))
        db_conn.commit()

    db_conn.close()
