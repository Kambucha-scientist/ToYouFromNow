"""
import sqlite3 as sl


def createTable():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("CREATE TABLE IF NOT EXISTS messages(user_id BIGINT NOT NULL, chat_id BIGINT NOT NULL, "
                       "text TEXT NOT NULL, sending_time TIMESTAMP NOT NULL, is_sent INT default 0)")
    con.commit()
    con.close()


def getUnsentMessage():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("SELECT * from messages WHERE is_sent = 0")
        messages = cursor.fetchall()
    con.commit()
    con.close()
    return messages


def clear():
    con = sl.connect('messages.db')
    cursor = con.cursor()
    with con:
        cursor.execute("DELETE FROM messages WHERE is_sent = 1")
    con.commit()
    con.close()
"""

from sqlalchemy import BigInteger, TIMESTAMP, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    sending_time: Mapped[datetime]= mapped_column(TIMESTAMP)
    message_text: Mapped[str] = mapped_column(Text)
    is_sent: Mapped[int] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


