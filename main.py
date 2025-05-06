import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from databaseInterface import async_main
from requests import getUnsentMessages, wasSent
from parsing_date import convertToMoscowTime
import os
import logging


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stop_flag = True


async def check_messages():
    logger.info("Checking messages started")
    while stop_flag:
        logger.info("checking...")
        messages = await getUnsentMessages()
        logger.info(datetime.now(ZoneInfo('Europe/Moscow')))
        for msg in messages:
            if datetime.now(ZoneInfo('Europe/Moscow')) >= convertToMoscowTime(msg.sending_time):
                logger.info(datetime.now(ZoneInfo('Europe/Moscow')))
                logger.info(convertToMoscowTime(msg.sending_time))
                await bot.send_message(msg.chat_id, f"🔮 Ваше сообщение из прошлого:\n{msg.message_text}")
                await wasSent(msg.id)
        await asyncio.sleep(60)


async def on_startup():
    asyncio.create_task(check_messages())


async def on_shutdown():
    stop_flag = False


async def main():
    await async_main()
    dp.include_router(router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)
    dp.shutdown.register(on_shutdown)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
