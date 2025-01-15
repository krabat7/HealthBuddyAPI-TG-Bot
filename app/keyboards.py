from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Настроить профиль"), KeyboardButton(text="Записать воду")],
        [KeyboardButton(text="Проверить прогресс"), KeyboardButton(text="Записать еду")],
        [KeyboardButton(text="Удалить данные"), KeyboardButton(text="Записать тренировку")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


# Инлайн-клавиатура для тренировки
workout_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Бег", callback_data="workout_run")],
        [InlineKeyboardButton(text="Плавание", callback_data="workout_swim")],
        [InlineKeyboardButton(text="Йога", callback_data="workout_yoga")],
    ]
)

# Инлайн-клавиатура для подтверждения действий
confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="confirm")],
        [InlineKeyboardButton(text="Отменить", callback_data="cancel")],
    ]
)