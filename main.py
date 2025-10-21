from interface import interface_main as im
from curses import wrapper


def main(stdscr):
    im.main_interface(stdscr)

def launcher():
    wrapper(main)


if __name__ == "__main__":
    launcher()
