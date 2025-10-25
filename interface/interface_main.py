import sys,os,time
import _curses, curses, sqlite3


from interface import interface_classes as ic
from interface import interface_callbacks as cb
from processing import processing_main as p

from interface_config import CFG


try:
    import utils.text_logger as log
    LOG = log.Log()
    print("Log initialized")
except Exception as e:
    print(e)
    LOG = None
    pass


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
    CFG.mainScreen = mainscreen
    CFG.processor = wp
    get_cached_location()
    rough_data = get_valid_location(mainscreen) if CFG.location == "" else CFG.get_weather()
    data = CFG.processor.load_data(rough_data)
    mainscreen.display_location_info(data=CFG.processor.filtered_data, heading="Weather")
    data = CFG.processor.load_data(CFG.get_weather())
    mainscreen.display_location_info(data=CFG.processor.filtered_data, heading="Weather")
    curses.curs_set(0)
    main_loop(mainscreen, CFG.processor, LAST_REFRESHED)


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
            mainscreen.screen.clear()
            mainscreen.screen.refresh()
            mainscreen.draw()
            new_loc = get_valid_location(mainscreen)
            CFG.process_location_reset(mainscreen, new_loc)
            if LOG != None:
                LOG.write(new_loc)
            last_refreshed = now


        # User can press m to view the options menu
        if k == ord('m'):
            menu = ic.MenuInterface(parent=mainscreen, heading = "Menu")
            menu.add_option(SaveLocationOption)
            menu.add_option(ChooseLocationOption)
            menu.add_option(ExitOption)
            for opt in menu.options:
                opt.selected = False
            menu.options[0].selected = True
            if LOG:
                LOG.write([i.content for i in menu.options])
            menu.draw()
            menu.draw_options()
            menu.get_selection(LOG)
        time.sleep(0.05)


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
    return location


SaveLocationOption = ic.MenuOption(
    "Save Location",
    callback = lambda : cb.save_location(CFG.location)
)


ExitOption = ic.MenuOption(
    "Exit",
    callback = quit
)


ChooseLocationOption = ic.MenuOption(
    "Choose Location",
    callback = lambda : cb.choose_location(CFG.mainScreen, LOG)
)

