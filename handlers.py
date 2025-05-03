from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()
@router.message(CommandStart())
async def start(message: Message):
    await message.answer('sup <3! Этот бот позволяет отправить письмо себе в будущее! Хочешь попробовать? напиши команду'
                         ' /help, чтобы узнать доступные команды')

@router.message(Command('help'))
async def getHelp(message: Message):
    await message.answer('Для отправки сообщений в будущее - /send'
                         '\nДля просмотра дат отправленных в будущее сообщений - /check.'
                         '\nДля изменения даты - /edit.'
                         )
