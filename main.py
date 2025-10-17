import requests, os, processing, time, curses
from interface import main_interface
from dotenv import load_dotenv
from curses import wrapper


def main(stdscr):
    load_dotenv()
    cfg = processing.Config(os.getenv("API_KEY"))
    main_interface(stdscr, cfg)


if __name__ == "__main__":
    wrapper(main)
