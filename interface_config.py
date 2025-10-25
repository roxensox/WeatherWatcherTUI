import os
from dotenv import load_dotenv
from pathlib import Path
from processing import processing_main as p


load_dotenv(Path.home() / ".weatherwatcher" / ".env")


CFG = p.Config(os.getenv("API_KEY"))
