from app.storage import users

def calculate_goals(weight, height, age, activity, temperature):
    water = weight * 30 + (500 if activity > 30 else 0) + (500 if temperature > 25 else 0)
    calories = 10 * weight + 6.25 * height - 5 * age + activity * 5
    return {"water_goal": water, "calorie_goal": calories}

def get_user_data(user_id):
    user = users.get(user_id)
    if not user:
        raise ValueError("Сначала настройте профиль с помощью команды /set_profile.")
    return user