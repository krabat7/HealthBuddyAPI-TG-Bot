import requests
from config import WEATHER_TOKEN

# Получение температуры города с помощью OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_TOKEN}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("main", {}).get("temp")
    return None

# Поиск информации о продукте с помощью OpenFoodFacts API
def get_food_info(product_name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?action=process&search_terms={product_name}&json=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        if products:
            first_product = products[0]
            return {
                'name': first_product.get('product_name', 'Неизвестно'),
                'calories': first_product.get('nutriments', {}).get('energy-kcal_100g', 0)
            }
    return None