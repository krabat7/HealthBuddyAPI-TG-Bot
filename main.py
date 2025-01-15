import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import router
from app.storage import load_data, save_data

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    try:
        load_data()
        dp.include_router(router)

        print("Бот запущен.")
        await dp.start_polling(bot)

    except asyncio.CancelledError:
        print("Программа завершена.")
    finally:
        await bot.session.close()
        save_data()
        print("Данные сохранены и бот остановлен.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nЗавершение работы по запросу пользователя.")
    except Exception as e:
        print(f"Ошибка: {e}")