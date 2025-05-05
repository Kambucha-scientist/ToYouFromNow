import asyncio
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from databaseInterface import async_main
from requests import getUnsentMessages, wasSent
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

""""
async def check_messages():
    while True:
        messages = await getUnsentMessages()
        for msg in messages:
            if datetime.now(ZoneInfo('Europe/Moscow')) >= msg.sending_time:
                await bot.send_message(msg.chat_id, f"🔮 Ваше сообщение из прошлого:\n{msg.message_text}")
                await wasSent(msg.id)
        await asyncio.sleep(60)

"""

async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
