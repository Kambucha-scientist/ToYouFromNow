from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from parsing_date import parse_date
from requests import addMessage, messagesByUser

import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="ru_RU.UTF-8"
)

router = Router()


class Parser(StatesGroup):
    first_message = State()
    text = State()
    date = State()
    last_message = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('sup <3! Этот бот позволяет отправить письмо себе в будущее! Хочешь попробовать? напиши команду'
                         ' /help, чтобы узнать доступные команды')

@router.message(Command('help'))
async def getHelp(message: Message):
    await message.answer('Для отправки сообщений в будущее - /send'
                         '\nДля просмотра дат отправленных в будущее сообщений - /check.'
                         )


@router.message(Command('send'))
async def send(message: Message, state: FSMContext):
    await state.set_state(Parser.first_message)
    await state.update_data(first_message=message.message_id)
    await state.set_state(Parser.text)
    await message.answer("Отлично! Напиши сообщение, которое ты получишь в будущем! (>100 символов)")

@router.message(Parser.text)
async def getText(message: Message, state: FSMContext):
    if (len(message.text) >= 100):
        await state.update_data(text=message.text)
        await state.set_state(Parser.date)
        await message.answer('Золотые слова! Теперь напиши, когда ты снова увидешь своё сообщение.(Например, "через год", "через 3 месяца", "2026 год 3 сентября в 15:49")')
    else:
        await message.answer("Так мало слов! Уверен, тебе есть что сказать :D")
@router.message(Parser.date)
async def getDate(message: Message, state: FSMContext,bot: Bot):
    try:
        await state.update_data(date=parse_date(message.text))
        await state.set_state(Parser.last_message)
        await state.update_data(last_message=message.message_id)
        data = await state.get_data()
        await addMessage(message.from_user.id, message.chat.id, data["date"], data["text"])
        await message.answer(f"Увидимся {(data["date"]).strftime("%d %b %Y")} в {(data["date"]).strftime("%H:%M")} !")
        for i in range(data["first_message"], data["last_message"] + 1):
            await bot.delete_message(message.chat.id, i)
        await state.clear()
    except ValueError:
        await message.answer("Ой! Не смог расспознать дату :<. Попробуй ещё раз!")


@router.message(Command('check'))
async def check(message: Message):
    messages = await messagesByUser(message.from_user.id)
    count = 0
    answer = "Сообщения, которые ждут Вас в будущем:\n\n"
    for msg in messages:
        answer += '"' + msg.message_text[:10] + "..." + '"' +" | " + msg.sending_time.strftime("%d %b %Y %H:%M") + "\n"
        count += 1
    if count == 0:
        await message.answer("Вы ещё не отправили ни одного сообщения! Используй /send, чтобы отправить его!")
    else:
        await message.answer(answer)


