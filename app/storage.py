import json
from datetime import datetime

# Хранилище данных пользователей
users = {}
daily_reset_keys = [
    "logged_water",
    "logged_calories",
    "extra_water",
    "extra_calories",
    "burned_calories",
]

# Сбрасывает данные за день
def reset_daily_data():
    if not users:
        return
    
    current_date = datetime.now().date().isoformat()
    for user_id, data in users.items():
        if data.get("last_updated") == current_date:
            continue
        for key in daily_reset_keys:
            data[key] = 0
        data["last_updated"] = current_date

# Сохраняет данные пользователей в файл
def save_data():
    try:
        with open("users_data.json", "w", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

# Загружает данные пользователей из файла
def load_data():
    global users
    try:
        with open("users_data.json", "r", encoding="utf-8") as file:
            users = json.load(file)
            print(f"Данные успешно загружены: {users}")
            reset_daily_data()  # Сброс данных за новый день
    except FileNotFoundError:
        users = {}
        print("Файл данных не найден. Создаётся пустой словарь.")
        save_data()
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        users = {}