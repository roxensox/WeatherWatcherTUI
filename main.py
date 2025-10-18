import requests, os, processing, time, curses
from interface import main_interface
from pathlib import Path
from dotenv import load_dotenv
from curses import wrapper


def main(stdscr):
    load_dotenv(Path.home() / ".weatherwatcher" / ".env")
    cfg = processing.Config(os.getenv("API_KEY"))
    main_interface(stdscr, cfg)


def launcher():
    wrapper(main)

if __name__ == "__main__":
    launcher()
