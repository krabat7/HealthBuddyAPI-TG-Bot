import os
from dotenv import load_dotenv

load_dotenv()

# Токены для работы с ботом и API погоды, еды
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
FOOD_TOKEN = os.getenv("FOOD_TOKEN")