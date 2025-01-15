from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.keyboards import main_menu, workout_types, confirmation_keyboard
from app.storage import users
from app.utils import calculate_goals, get_user_data
from app.api import get_weather, get_food_info

router = Router()

class ProfileSetup(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я помогу отслеживать воду и калории.\n\n"
        "🔧 Основные команды:\n"
        "/set_profile - Настройка профиля\n"
        "/log_water <количество> - Записать потребление воды (в мл)\n"
        "/log_food <название продукта> - Записать потребление пищи\n"
        "/log_workout - Записать тренировку\n"
        "/delete_data - Удалить все данные\n\n"
        "Выберите действие с помощью меню ниже или отправьте команду вручную.",
        reply_markup=main_menu
    )

@router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    await state.set_state(ProfileSetup.weight)
    await message.answer("Введите ваш вес (в кг):")

@router.message(ProfileSetup.weight)
async def set_weight(message: Message, state: FSMContext):
    try:
        await state.update_data(weight=int(message.text))
        await state.set_state(ProfileSetup.height)
        await message.answer("Введите ваш рост (в см):")
    except ValueError:
        await message.answer("Пожалуйста, введите число.")

@router.message(ProfileSetup.height)
async def set_height(message: Message, state: FSMContext):
    try:
        await state.update_data(height=int(message.text))
        await state.set_state(ProfileSetup.age)
        await message.answer("Введите ваш возраст:")
    except ValueError:
        await message.answer("Пожалуйста, введите число.")

@router.message(ProfileSetup.age)
async def set_age(message: Message, state: FSMContext):
    try:
        await state.update_data(age=int(message.text))
        await state.set_state(ProfileSetup.activity)
        await message.answer("Сколько минут активности у вас в день?")
    except ValueError:
        await message.answer("Пожалуйста, введите число.")

@router.message(ProfileSetup.activity)
async def set_activity(message: Message, state: FSMContext):
    try:
        await state.update_data(activity=int(message.text))
        await state.set_state(ProfileSetup.city)
        await message.answer("В каком городе вы находитесь?")
    except ValueError:
        await message.answer("Пожалуйста, введите число.")

@router.message(ProfileSetup.city)
async def set_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()

    temperature = get_weather(data["city"])
    if temperature is None:
        await message.answer("Не удалось получить данные о погоде. Возможно ошибка в названии города.")
        return
    
    users[message.from_user.id] = {
        "weight": data["weight"],
        "height": data["height"],
        "age": data["age"],
        "activity": data["activity"],
        "city": data["city"],
        **calculate_goals(data["weight"], data["height"], data["age"], data["activity"], temperature)
    }
    await state.clear()
    await message.answer("Профиль настроен! Данные о погоде успешно учтены.", reply_markup=main_menu)


# Команда /log_water
@router.message(Command("log_water"))
async def log_water(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Используйте: /log_water <количество> (в мл)")
        return

    amount = int(args[1])
    
    try:
        user = get_user_data(message.from_user.id)
        user["logged_water"] = user.get("logged_water", 0) + amount
        await message.answer(f"💧 Записано: {amount} мл. Выпито: {user['logged_water']} мл из {user['water_goal']} мл.")
    except ValueError as e:
        await message.answer(str(e))

# Команда /log_food
@router.message(Command("log_food"))
async def log_food(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("Используйте: /log_food <название продукта>")
        return

    product_name = args[1]
    food_info = get_food_info(product_name)
    if food_info is None:
        await message.answer(f"Информация о продукте '{product_name}' не найдена.")
        return

    try:
        user = get_user_data(message.from_user.id)
        calories = food_info["calories"]
        user["logged_calories"] = user.get("logged_calories", 0) + calories
        await message.answer(
            f"🍎 {food_info['name']} содержит {calories} ккал на 100 г. Записано в ваш дневник. "
            f"Всего потреблено: {user['logged_calories']} ккал из {user['calorie_goal']} ккал."
        )
    except ValueError as e:
        await message.answer(str(e))

# Команда /log_workout
@router.message(Command("log_workout"))
async def log_workout(message: Message):
    await message.answer("Выберите тип тренировки:", reply_markup=workout_types)

@router.callback_query(F.data.startswith("workout_"))
async def handle_workout_type(callback: CallbackQuery):
    workout_type = callback.data.split("_")[1]
    duration = 30  # время тренировки по умолчанию

    try:
        user = get_user_data(callback.from_user.id)
        calories_burned = duration * 10  # Условная формула
        user["burned_calories"] = user.get("burned_calories", 0) + calories_burned
        water_loss = (duration // 30) * 200
        user["logged_water"] = user.get("logged_water", 0) - water_loss

        await callback.message.answer(
            f"🏃‍♂️ {workout_type.capitalize()} ({duration} минут) — {calories_burned} ккал сожжено.\n"
            f"Не забудьте выпить дополнительно {water_loss} мл воды. "
            f"Общее сожжённое: {user['burned_calories']} ккал."
        )
        await callback.answer()
    except ValueError as e:
        await callback.answer(str(e))

@router.message(F.text == "Удалить данные")
async def delete_data_text(message: Message):
    await message.answer(
        "Вы уверены, что хотите удалить все данные? Это действие необратимо.",
        reply_markup=confirmation_keyboard
    )

@router.callback_query(F.data == "confirm")
async def confirm_action(callback: CallbackQuery):
    users.pop(callback.from_user.id, None)
    await callback.message.answer("Ваши данные удалены.")
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery):
    await callback.message.answer("Действие отменено.")
    await callback.answer()