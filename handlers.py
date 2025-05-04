from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext


router = Router()


class Parser(StatesGroup):
    text = State()
    date = State()


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


@router.message(Command('send'))
async def send(message: Message, state: FSMContext):
    await state.set_state(Parser.text)
    await message.answer("Отлично! Напиши сообщение, которое ты получишь в будущем!")

@router.message(Parser.text)
async def getText(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Parser.date)
    await message.answer("Золотые слова! Теперь напиши дату и время, когда ты снова увидешь своё сообщение( сообщение придёт в указанное время по МСК)")

@router.message(Parser.date)
async def getDate(message: Message, state: FSMContext):
    await state.update_data(data=message.text)
    data = await state.get_data()
    await message.answer(f"Увидимся в {data["date"]} !")
    await state.clear()

@router.message(Command('check'))
async def check(message: Message):
    await message.answer("Заглушка для команды check")


@router.message(Command('edit'))
async def edit(message: Message):
    await message.answer("Заглушка для команды edit")
