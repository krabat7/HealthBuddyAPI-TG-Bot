import os
from dotenv import load_dotenv

load_dotenv()

# Токены для работы с ботом и API погоды
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")