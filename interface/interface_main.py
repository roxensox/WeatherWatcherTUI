import sys,os,time, interface.interface_callbacks
import _curses, curses
import processing.processing_main as p
from dotenv import load_dotenv
from pathlib import Path
from interface.interface_classes import Interface, MainInterface, InfoInterface, MenuInterface, MenuOption


try:
    import text_logger
except:
    pass

LAST_REFRESHED = time.time()

load_dotenv(Path.home() / ".weatherwatcher" / ".env")
CFG = p.Config(os.getenv("API_KEY"))

if 'text_logger' in sys.modules:
    LOG = text_logger.Log()
else:
    LOG = None

def main_interface(stdscr: _curses.window):
    wp = p.WeatherProcessor()
    k = ''
    mainscreen = MainInterface(screen=stdscr)
    mainscreen.screen.nodelay(True)
    rough_data = get_valid_location(mainscreen)
    data = wp.load_data(rough_data)
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    LAST_REFRESHED = time.time()
    refresh_interval = 5
    data = wp.load_data(CFG.get_weather())
    mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
    curses.curs_set(0)

    # User can press q to close
    while k != ord('q'):
        k = mainscreen.screen.getch()

        if curses.is_term_resized(mainscreen.height, mainscreen.width):
            mainscreen.resize_handler()

        now = time.time()

        # Gets new data at the specified interval
        if now - LAST_REFRESHED >= refresh_interval:
            data = wp.load_data(CFG.get_weather())
            mainscreen.display_location_info(data=wp.filtered_data, heading=wp.title)
            LAST_REFRESHED = now

        # User can press r to reselect their location
        if k == ord('r'):
            mainscreen.screen.clear()
            mainscreen.screen.refresh()
            rd = get_valid_location(CFG, mainscreen)
            data = wp.load_data(rd)
            mainscreen.display_location_info(data=wp.filtered_data, heading="Weather")
            LAST_REFRESHED = now

        # User can press m to view the options menu
        if k == ord('m'):
            menu = MenuInterface(parent=mainscreen, heading = "Menu")
            menu.add_option(SaveLocationOption)
            menu.add_option(ExitOption)
            menu.options[0].selected = True
            if LOG:
                LOG.write(menu.options)
            menu.draw()
            menu.draw_options()
            menu.get_selection()
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
    return rough_data


SaveLocationOption = MenuOption(
    "Save Location",
    callback = lambda : interface.interface_callbacks.save_location(CFG.location)
)

ExitOption = MenuOption(
    "Exit",
    callback = quit
)
