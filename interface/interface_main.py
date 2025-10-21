import sys,os,time
import _curses, curses, sqlite3

from dotenv import load_dotenv
from pathlib import Path

from processing import processing_main as p
from interface import interface_classes as ic
from interface import interface_callbacks as cb


try:
    import text_logger
except:
    pass

load_dotenv(Path.home() / ".weatherwatcher" / ".env")

CFG = p.Config(os.getenv("API_KEY"))

if 'text_logger' in sys.modules:
    LOG = text_logger.Log()
else:
    LOG = None


def get_cached_location():
    dbConn = cb.get_db_conn()
    sql = "SELECT location FROM locations ORDER BY id DESC LIMIT 1"
    results = dbConn.execute(sql).fetchone()
    dbConn.close()
    if results != None:
        CFG.location = results[0]


def main_interface(stdscr: _curses.window):
    LAST_REFRESHED = time.time()
    wp = p.WeatherProcessor()
    mainscreen = ic.MainInterface(screen=stdscr)
    mainscreen.screen.nodelay(True)
    get_cached_location()
    rough_data = get_valid_location(mainscreen) if CFG.location == "" else CFG.get_weather()
    data = wp.load_data(rough_data)
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    data = wp.load_data(CFG.get_weather())
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    curses.curs_set(0)
    main_loop(mainscreen, wp, LAST_REFRESHED)


def main_loop(mainscreen, wp, last_refreshed):
    refresh_interval = 5
    k = ''
    # User can press q to close
    while k != ord('q'):
        k = mainscreen.screen.getch()

        if curses.is_term_resized(mainscreen.height, mainscreen.width):
            mainscreen.resize_handler()

        now = time.time()

        # Gets new data at the specified interval
        if now - last_refreshed >= refresh_interval:
            data = wp.load_data(CFG.get_weather())
            mainscreen.display_location_info(data=wp.filtered_data, heading=wp.title)
            last_refreshed = now

        # User can press r to reselect their location
        if k == ord('r'):
            process_location_reset(mainscreen, wp)
            last_refreshed = now

        # User can press m to view the options menu
        if k == ord('m'):
            menu = ic.MenuInterface(parent=mainscreen, heading = "Menu")
            menu.add_option(SaveLocationOption)
            menu.add_option(ExitOption)
            menu.options[0].selected = True
            if LOG:
                LOG.write(menu.options)
            menu.draw()
            menu.draw_options()
            menu.get_selection()
        time.sleep(0.05)


def process_location_reset(mainscreen, wp):
        mainscreen.screen.clear()
        mainscreen.screen.refresh()
        rd = get_valid_location(mainscreen)
        data = wp.load_data(rd)
        mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")


def get_valid_location(main):
    '''
    Prompts for input and validates it with the API
    '''
    rough_data = {}
    while rough_data.get("location") == None:
        location = main.get_location()
        if location == "":
            main.screen.clear()
            main.screen.addstr(0, 0, "No location provided... exiting.")
            main.screen.refresh()
            curses.curs_set(0)
            time.sleep(1)
            quit()
        main.draw()
        CFG.set_location(location)
        rough_data = CFG.get_weather()
    return rough_data


SaveLocationOption = ic.MenuOption(
    "Save Location",
    callback = lambda : cb.save_location(CFG.location)
)

ExitOption = ic.MenuOption(
    "Exit",
    callback = quit
)
