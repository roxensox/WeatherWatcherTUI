import requests, os, processing.processing_main as p, time, curses
from interface.interface_main import main_interface
from pathlib import Path
from dotenv import load_dotenv
from curses import wrapper


def main(stdscr):
    load_dotenv(Path.home() / ".weatherwatcher" / ".env")
    cfg = p.Config(os.getenv("API_KEY"))
    main_interface(stdscr, cfg)


def launcher():
    wrapper(main)

if __name__ == "__main__":
    launcher()
