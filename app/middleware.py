import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

# Настройка логирования
log_file = "logs/bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Middleware для логирования действий пользователей
class LogCommandsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            username = event.from_user.username or "No username"
            text = event.text or "No text"
            logging.info(f"Сообщение: Пользователь {user_id} ({username}) отправил: {text}")
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            username = event.from_user.username or "No username"
            callback_data = event.data or "No callback data"
            logging.info(f"Кнопка: Пользователь {user_id} ({username}) выбрал: {callback_data}")
        return await handler(event, data)
