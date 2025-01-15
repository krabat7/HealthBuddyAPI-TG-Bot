import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from app.handlers import router
from app.storage import load_data, save_data

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    load_data()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Телеграм бот отключен.')
    finally:
        save_data()