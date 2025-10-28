import sys, os, time
import _curses, curses, sqlite3


from interface import interface_classes as ic
from interface import interface_callbacks as cb
from processing import processing_main as p

from interface.interface_config import CFG


#TODO:  Change queries that access the locations table to update access time for retrieved elements
#       The most recently accessed element should be the cached one, not the most recently added
def get_cached_location():
    dbConn = cb.get_db_conn()
    sql = "SELECT location FROM locations ORDER BY id DESC LIMIT 1"
    results = dbConn.execute(sql).fetchone()
    dbConn.close()
    if results != None:
        CFG.location = results[0]


def main_interface(stdscr: _curses.window):
    # Initializes refresh time
    LAST_REFRESHED = time.time()

    # Gets the weather processor
    wp = p.WeatherProcessor()

    # Creates the main screen
    mainscreen = ic.MainInterface(screen=stdscr)

    # Makes it so the data can update while also listening for input
    mainscreen.screen.nodelay(True)

    # Adds elements to config
    CFG.mainScreen = mainscreen
    CFG.processor = wp

    # Loads persistent data into config
    CFG.get_saved_locations(cb.get_db_conn())
    get_cached_location()

    # Calls the API for data
    rough_data = get_valid_location(mainscreen) if CFG.location == "" else CFG.get_weather()

    # Processes data through weather processor and writes it to the screen
    data = CFG.processor.load_data(rough_data)
    mainscreen.display_location_info(data=CFG.processor.filtered_data, heading="Weather")

    # Hides the cursor
    curses.curs_set(0)

    # Runs the input loop
    main_loop(mainscreen, CFG.processor, LAST_REFRESHED)


def main_loop(mainscreen, wp, last_refreshed):
    refresh_interval = 5
    k = ''
    # User can press q to close
    while k != ord('q'):
        CFG.get_saved_locations(cb.get_db_conn())
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
            new_loc = get_valid_location(mainscreen, curr_loc = CFG.location)
            CFG.process_location_reset(mainscreen, new_loc)
            if CFG.log != None:
                CFG.log.write(new_loc)
            last_refreshed = now


        # User can press m to view the options menu
        if k == ord('m'):
            menu = ic.MenuInterface(parent=mainscreen, heading = "Menu")
            menu.add_option(SaveLocationOption)
            if CFG.saved_locations > 0:
                menu.add_option(ChooseLocationOption)
            menu.add_option(ExitOption)
            for opt in menu.options:
                opt.selected = False
            menu.options[0].selected = True
            if CFG.log:
                CFG.log.write([i.content for i in menu.options])
            menu.draw()
            menu.draw_options()
            menu.get_selection(CFG.log)
        time.sleep(0.05)


def get_valid_location(main, curr_loc = None):
    '''
    Prompts for input and validates it with the API
    '''
    rough_data = {}
    while rough_data.get("location") == None:
        location = main.get_location()
        if location == "":
            main.screen.clear()
            if curr_loc == None:
                main.screen.addstr(0, 0, "No location provided... exiting.")
                main.screen.refresh()
                curses.curs_set(0)
                time.sleep(1)
                quit()
            else:
                location = curr_loc
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


ChooseLocationOption = ic.MenuOption(
    "Choose Location",
    callback = lambda : cb.choose_location(CFG.mainScreen, CFG.log)
)

