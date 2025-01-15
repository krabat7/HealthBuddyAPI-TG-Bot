import os
from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.utils import *
from app.keyboards import main_menu, workout_types, confirmation_keyboard
import app.storage
from app.storage import save_data
from app.api import get_weather, get_food_info


router = Router()

class ProfileSetup(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()

class WaterLogging(StatesGroup):
    waiting_for_amount = State()

class FoodLogging(StatesGroup):
    waiting_for_food = State()

@router.message(Command("start"))
async def cmd_start(message: Message):
    commands_info = get_commands_info()
    profile_info = await get_profile_info(message.from_user.id)

    if profile_info:
        await message.answer(
            f"{commands_info}\n\n{profile_info}",
            reply_markup=main_menu,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"{commands_info}\n\n"
            "Ваш профиль <b>не настроен</b>. Пожалуйста, настройте его с помощью команды /set_profile.",
            reply_markup=main_menu,
            parse_mode="HTML"
        )


@router.message(F.text == "Главное меню")
async def handle_main_menu(message: Message):
    commands_info = get_commands_info()
    profile_info = await get_profile_info(message.from_user.id)

    if profile_info:
        await message.answer(
            f"{commands_info}\n\n{profile_info}",
            reply_markup=main_menu,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"{commands_info}\n\n"
            "Ваш профиль <b>не настроен</b>. Пожалуйста, настройте его с помощью команды /set_profile.",
            reply_markup=main_menu,
            parse_mode="HTML"
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
        
    user_id = str(message.from_user.id)
    app.storage.users[user_id] = {
        "weight": data["weight"],
        "height": data["height"],
        "age": data["age"],
        "activity": data["activity"],
        "city": data["city"],
        "logged_water": 0,
        "logged_calories": 0,
        "water_goal": 0,
        "calorie_goal": 0,
        "extra_water": 0,
        "extra_calories": 0,
        "burned_calories": 0,
        "last_updated": datetime.now().date().isoformat(),
        **calculate_goals(data["weight"], data["height"], data["age"], data["activity"], temperature),
    }
    
    save_data()

    await state.clear()
    await message.answer("Профиль настроен! Данные о погоде успешно учтены.", reply_markup=main_menu)

# Команда /log_water
@router.message(Command("log_water"))
async def log_water(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Используйте: /log_water <количество> (в мл)")
        return
    try:
        amount = int(args[1])
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение (в мл).")
    
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

        # Увеличение целей после тренировки
        extra_water = (duration // 30) * 200
        extra_calories = duration * 10
        user["extra_water"] = user.get("extra_water", 0) + extra_water
        user["extra_calories"] = user.get("extra_calories", 0) + extra_calories

        # Сожженные калории
        user["burned_calories"] = user.get("burned_calories", 0) + extra_calories

        await callback.message.answer(
            f"🏃‍♂️ {workout_type.capitalize()} ({duration} минут):\n"
            f"🔥 Сожжено: {extra_calories} ккал.\n"
            f"💧 Потребность в воде увеличена на {extra_water} мл."
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
    user_id = str(callback.from_user.id)
    if user_id in app.storage.users:
        app.storage.users.pop(user_id, None)
        save_data()
        await callback.message.answer("Ваши данные удалены.")
    else:
        await callback.message.answer("У вас нет данных для удаления.")
    await callback.answer()


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery):
    await callback.message.answer("Действие отменено.")
    await callback.answer()

@router.message(F.text == "Проверить прогресс")
async def check_progress(message: Message):
    try:
        user = get_user_data(message.from_user.id)

        water_goal = user["water_goal"] + user.get("extra_water", 0)
        calorie_goal = user["calorie_goal"] + user.get("extra_calories", 0)

        logged_water = user.get("logged_water", 0)
        logged_calories = user.get("logged_calories", 0)
        burned_calories = user.get("burned_calories", 0)

        file_path = f"progress_{message.from_user.id}.png"
        generate_progress_graph(user, file_path)

        water_progress = f"💧 Выпито: {logged_water} мл из {water_goal} мл."
        calorie_progress = (
            f"🍎 Потреблено: {logged_calories} ккал из {calorie_goal} ккал.\n"
            f"🔥 Сожжено: {burned_calories} ккал."
        )

        await message.answer(f"📊 Ваш прогресс:\n\n{water_progress}\n{calorie_progress}")
        
        photo = FSInputFile(file_path)
        await message.answer_photo(photo)

    except ValueError as e:
        await message.answer(str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.message(F.text == "Настроить профиль")
async def handle_setup_profile_button(message: Message, state: FSMContext):
    await set_profile(message, state)

@router.message(F.text == "Записать тренировку")
async def handle_log_workout_button(message: Message):
    await log_workout(message)

@router.message(F.text == "Проверить прогресс")
async def handle_check_progress_button(message: Message):
    await check_progress(message)

@router.message(F.text == "Удалить данные")
async def handle_delete_data_button(message: Message):
    await delete_data_text(message)

@router.message(F.text == "Записать воду")
async def handle_log_water_button(message: Message, state: FSMContext):
    await state.set_state(WaterLogging.waiting_for_amount)
    await message.answer("Введите количество воды (в мл):")

@router.message(WaterLogging.waiting_for_amount)
async def log_water_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение (в мл).")

    try:
        user = get_user_data(message.from_user.id)
        user["logged_water"] = user.get("logged_water", 0) + amount
        await message.answer(f"💧 Записано: {amount} мл. Выпито: {user['logged_water']} мл из {user['water_goal']} мл.")
        await state.clear()
    except ValueError as e:
        await message.answer(str(e))

@router.message(F.text == "Записать еду")
async def handle_log_food_button(message: Message, state: FSMContext):
    await state.set_state(FoodLogging.waiting_for_food)
    await message.answer("Введите название продукта:")

@router.message(FoodLogging.waiting_for_food)
async def log_food_entry(message: Message, state: FSMContext):
    product_name = message.text.strip()
    food_info = get_food_info(product_name)
    if food_info is None:
        await message.answer(f"Информация о продукте '{product_name}' не найдена.")
        await state.clear()
        return

    try:
        user = get_user_data(message.from_user.id)
        calories = food_info["calories"]
        user["logged_calories"] = user.get("logged_calories", 0) + calories
        await message.answer(
            f"🍎 {food_info['name']} содержит {calories} ккал на 100 г. Записано в ваш дневник. "
            f"Всего потреблено: {user['logged_calories']} ккал из {user['calorie_goal']} ккал."
        )
        await state.clear()
    except ValueError:
        await message.answer("Ошибка при обработке данных. Пожалуйста, попробуйте снова.")