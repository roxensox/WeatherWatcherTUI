import requests, os, classes, time
from dotenv import load_dotenv


def main():
    load_dotenv()
    cfg = classes.Config(os.getenv("API_KEY"))
    cfg.set_location("58401")
    while True:
        weather = cfg.get_weather()
        print(weather)
        time.sleep(30)


if __name__ == "__main__":
    main()
