import requests
from config import WEATHER_TOKEN, FOOD_TOKEN

# Получение температуры города с помощью OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("main", {}).get("temp")
    return None

# Поиск информации о продукте с помощью FoodData Central API (USDA)
def get_calories_from_usda(product_name):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={product_name}&api_key={FOOD_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('foods'):
            food = data['foods'][0]
            return {
                'name': food['description'],
                'calories': next(
                    (nutrient['value'] for nutrient in food['foodNutrients'] if nutrient['nutrientName'] == 'Energy'),
                    'Не найдено'
                )
            }
    return None
