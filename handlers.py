from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()
@router.message(CommandStart())
async def start(message: Message):
    await message.answer('sup <3!')

@router.message(Command('help'))
async def getHelp(message: Message):
    await message.answer('Здесь будет список команд')
