from bot import mytoken
from bot import date_operations as do
from bot import databckend as db

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

hello = """
I am  BirthDay Reminder BOT !

This is my command list:
"""
commands = """
/start - starts me
/birthdays_today - print persons with today's birthday
/remind_birthday  - add person and his birthday
/people - print lict known persons
/help - show this list
"""

bot = Bot(token=mytoken.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

DS = db.DataStore('data.csv', ['username', 'birthday'])

class UserState(StatesGroup):
    name = State()
    birthday = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(hello)
    await message.answer(commands)


@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer(commands)


@dp.message_handler(commands=['birthdays_today'])
async def birthdays_today(message: types.Message):
    await message.answer('Birthday today has:')
    empty = True
    for item in DS.get():
         if do.is_today(item['birthday']):
            empty = False
            await message.answer(f"Name: {item['username']}\n"
                             f"Birthday: {item['birthday']}")
    if empty:
        await message.answer('People not found!')


@dp.message_handler(commands=['people'])
async def birthdays_today(message: types.Message):
    await message.answer('I know next persons:')
    empty = True
    for item in DS.get():
        empty = False
        await message.answer(f"Name: {item['username']}\n"
                             f"Birthday: {item['birthday']}")
    if empty:
        await message.answer('Person list is empty!')


@dp.message_handler(commands=['remind_birthday'])
async def user_name(message: types.Message):
    await message.answer('Enter person name:')
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Enter person birthday in %d-%m-%Y format:')
    await UserState.next()


@dp.message_handler(state=UserState.birthday)
async def get_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    if do.is_valid_date(data['birthday']):
        await message.answer(f"Name: {data['username']}\n"
                         f"Birthday: {data['birthday']}")
        DS.save({'username': data['username'], 'birthday': data['birthday']})
        await state.finish()
    else:
        await message.answer('Invalid birthday data! Try again:')


async def main():
    await dp.start_polling(bot)

def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()


