from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


miss_button = InlineKeyboardButton(text='Пропустить', callback_data='miss')




miss_keyboard = InlineKeyboardMarkup(row_width=1).add(miss_button)


