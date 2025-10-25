import sqlite3, importlib.resources as resources
from interface.interface_classes import MenuInterface, MenuOption
from interface_config import CFG


def get_db_conn()->sqlite3.Connection:
    '''
    Returns a connection to the database
    '''
    root = __package__.split('.')[0]
    db_path = resources.files(root).joinpath("ww.db")
    return sqlite3.connect(db_path)


def save_location(loc: str, log = None):
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


def choose_location(mainscreen, log = None):
    location_query = "SELECT location FROM locations ORDER BY location"
    db_conn = get_db_conn()
    locations = db_conn.execute(location_query).fetchall()
    if len(locations) == 0:
        return
    else:
        subMenu = MenuInterface(
            parent=mainscreen,
            heading="Saved Locations"
        )

        for option in locations:
            option = option[0]
            if log != None:
                log.write(option)
            new_option = MenuOption(content=option, callback=lambda opt = option: set_location(mainscreen, opt, log))
            log.write(f"Option location: {option}")
            subMenu.add_option(new_option)

        subMenu.options[0].selected = True
        subMenu.draw()
        subMenu.draw_options()
        subMenu.get_selection(log)


def set_location(mainscreen, location: str, log = None):
    CFG.set_location(location)
    CFG.process_location_reset(mainscreen, location=location)
    log.write(f"New location: {location}")
