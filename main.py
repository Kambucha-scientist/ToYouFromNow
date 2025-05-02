import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram.types import Message
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('sup <3!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
