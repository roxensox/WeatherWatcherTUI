import os
from dotenv import load_dotenv
from pathlib import Path
from processing import processing_main as p


load_dotenv(Path.home() / ".weatherwatcher" / ".env")

try:
    import utils.text_logger as log
    NewLog = log.Log()
    print("Log initialized")
except Exception as e:
    print(e)
    NewLog = None
    pass


CFG = p.Config(API_Key = os.getenv("API_KEY"), log = NewLog)
