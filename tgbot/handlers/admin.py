from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot.config import load_config
from tgbot.misc.states import FSMAdmin
from tgbot.keyboards import inline
from tgbot.database import db_connector
from create_bot import bot

import asyncio

config = load_config(".env")
admin_group = config.misc.admin_group



async def answer_to_user(message: Message):
    user_message = message.reply_to_message.text
    try:
        user_id = int(user_message.split('\n')[1].split(' ')[-1][1:][:-1])
        await bot.send_message(chat_id=user_id, text=message.text)
    except:
        # text = ['Невозможно ответить пользователю. Проверьте входящее сообщение']
        # await message.answer(''.join(text))
        pass

async def no_answer(message: Message):
    text = 'Чтобы ответить на сообщение воспользуйтесь функцией "Ответить"'
    await message.answer(text)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(answer_to_user, state="*", is_reply=True, chat_id=admin_group)
    # dp.register_message_handler(no_answer, state="*", is_reply=False, chat_id=admin_group)

