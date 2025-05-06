import datetime
from databaseInterface import async_session
from databaseInterface import Message
from sqlalchemy import select


async def getUnsentMessages():
    async with async_session() as session:
        return await session.scalars(select(Message).where(Message.is_sent == 0).order_by(Message.sending_time))


async def addMessage(user_id: int,chat_id: int,sending_time: datetime,message_text: str):
    async with async_session() as session:
        session.add(Message(user_id=user_id,chat_id=chat_id,sending_time=sending_time,message_text=message_text,is_sent=0))
        await session.commit()

async def wasSent(id: int):
    async with async_session() as session:
        message = await session.get(Message,id)
        if message:
            message.is_sent = 1
            await session.commit()