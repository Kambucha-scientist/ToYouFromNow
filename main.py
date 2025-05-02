import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO) -- debugging
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")