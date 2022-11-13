from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMConnection(StatesGroup):
    connection_start = State()
    connection_contact = State()

class FSMSettings(StatesGroup):
    settings_choice = State()
    settings_name = State()
    settings_phone = State()


class FSMAdmin(StatesGroup):
    main = State()
    mailing = State()
    user_info = State()
    block_choice = State()
    block_user = State()
    unblock_user = State()
