from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записать воду")],
        [KeyboardButton(text="Записать еду")],
        [KeyboardButton(text="Записать тренировку")],
        [KeyboardButton(text="Проверить прогресс")],
        [KeyboardButton(text="Удалить данные")],
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