import requests, os, processing.processing_main as p, time, curses
from interface.interface_main import main_interface
from pathlib import Path
from dotenv import load_dotenv
from curses import wrapper


def main(stdscr):
    main_interface(stdscr)


def launcher():
    wrapper(main)


if __name__ == "__main__":
    launcher()
