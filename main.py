import requests, os, classes, time, curses
from dotenv import load_dotenv


def main():
    load_dotenv()
    location = input("Set Location: ")
    cfg = classes.Config(os.getenv("API_KEY"))
    cfg.set_location(location)
    prntr = classes.Printer()
    while True:
        try:
            weather = cfg.get_weather()
            if weather == None:
                break
            prntr.load_data(weather)
            prntr.output_data()
            time.sleep(30)
        except:
            print("Invalid location")
            location = input("Set Location: ")
            cfg.set_location(location)


if __name__ == "__main__":
    main()
