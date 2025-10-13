import requests, os, classes, time, curses
from dotenv import load_dotenv
from curses import wrapper


# FIXME: Incorporate printer with curses interface in interface.py
def main(stdscr):
    load_dotenv()
    cfg = classes.Config(os.getenv("API_KEY"))
    location = "58401"
    cfg.set_location(location)
    cfg.screen = stdscr
    stdscr.addstr(0, 0, "Set Location: ")
    stdscr.refresh()
    stdscr.getch()
    prntr = classes.Printer()
    while True:
        stdscr.clear()
        stdscr.addstr("Test")
        weather = cfg.get_weather()
        if weather == None:
            break
        prntr.load_data(weather)
        prntr.output_data()
        time.sleep(30)


if __name__ == "__main__":
    wrapper(main)
