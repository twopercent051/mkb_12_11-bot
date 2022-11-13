from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold
from aiogram.dispatcher import FSMContext

from tgbot.misc.states import *
from tgbot.database import db_connector
from tgbot.keyboards import reply
from tgbot.keyboards import inline
from tgbot.config import load_config
from create_bot import bot



config = load_config(".env")
admin_group_id = config.misc.admin_group


def mute(message: Message):
    pass


async def user_start(message: Message):
    text_rus = [
        'Благодарим за обращение в компанию <b>МКБ</b>! Напишите Ваш вопрос и контактные данные, мы обязательно с',
        'Вами свяжемся в ближайшее время.'
    ]
    text_eng = [
        'Thank you for contacting <b>MKB</b> company! Write your question and contact details, we will definitely',
        'contact you as soon as possible.'
    ]
    text = [
        ' '.join(text_rus),
        '',
        ' '.join(text_eng)
    ]


    await FSMConnection.connection_start.set()
    await message.answer('\n'.join(text))



async def user_start_after_cancel(message: Message):
    text = [
        'Отправьте свою контактную информацию в любом удобном Вам формате (например номер',
        'телефона или электронную почту) или нажмите клавишу <b>пропустть</b>'
    ]
    await FSMConnection.connection_start.set()
    await message.answer(' '.join(text), reply_markup=inline.miss_keyboard)



async def get_empty_contact(callback: CallbackQuery, state: FSMContext):
    text_to_user = [
        '✅Теперь задайте вопрос и мы ответим Вам в кратчайшее время. Для выхода из режима диалога нажмите клавишу',
        '"Завершить диалог"']
    contact = None
    async with state.proxy() as data:
        data['contact'] = contact
    await FSMConnection.connection_contact.set()
    await callback.message.answer(' '.join(text_to_user), reply_markup=reply.cancel_keyboard)
    await bot.answer_callback_query(callback.id)



async def get_contact(message: Message, state: FSMContext):
    text_to_user = [
        '✅Теперь задайте вопрос или оставьте заявку и мы Вам перезвоним. Для выхода из режима диалога',
                    'нажмите клавишу "Завершить диалог"'
    ]
    contact = message.text
    async with state.proxy() as data:
        data['contact'] = contact
    await FSMConnection.connection_contact.set()
    await message.answer(' '.join(text_to_user), reply_markup=reply.cancel_keyboard)



async def dialog(message: Message):

    username = message.from_user.username
    user_id = message.from_user.id
    try:
        if len(username) > 0:
            username = '@' + username
    except:
        username = ''
    text_to_admin = [
        '✉️<b>Сообщение от пользователя:</b>',
        f'{username} [{user_id}]',
        f'<b><i>Текст сообщения:</i></b> {message.text}',
        '',
        '<b>Для ответа используйте "Ответить на сообщение"</b>'
    ]
    await bot.send_message(chat_id=admin_group_id, text='\n'.join(text_to_admin))



def register_user(dp: Dispatcher):
    dp.register_message_handler(mute, chat_id=admin_group_id)
    dp.register_message_handler(user_start, commands=["start"], state='*')
    # dp.register_message_handler(user_start_after_cancel, Text(equals='📛Завершить диалог'), state='*')
    # dp.register_message_handler(get_contact, content_types=['text'], state=FSMConnection.connection_start)
    # dp.register_message_handler(dialog, content_types=['text'], state=FSMConnection.connection_contact)
    #
    # dp.register_callback_query_handler(get_empty_contact, lambda x: x.data == 'miss',
    #                                    state=FSMConnection.connection_start)
    dp.register_message_handler(dialog, content_types='text', state='*')


