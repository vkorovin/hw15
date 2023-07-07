from bot import mytoken
from bot import validation
from bot import databckend as db

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



bot = Bot(token=mytoken.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

DS = db.DataStore('data.csv', ['username', 'birthday'])

class UserState(StatesGroup):
    name = State()
    birthday = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("I am  BirthDay Reminder BOT")


@dp.message_handler(commands=['birthdays_today'])
async def birthdays_today(message: types.Message):
    await message.answer('Birthday today has:')
    for item in DS.get_today():
        await message.answer(f"Name: {item['username']}\n"
                             f"Birthday: {item['birthday']}")

@dp.message_handler(commands=['people'])
async def birthdays_today(message: types.Message):
    await message.answer('Birthday today has:')
    for item in DS.get():
        await message.answer(f"Name: {item['username']}\n"
                             f"Birthday: {item['birthday']}")

@dp.message_handler(commands=['remind_birthday'])
async def user_name(message: types.Message):
    await message.answer('Enter person name:')
    await UserState.name.set()
@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Enter person birthday:')
    await UserState.next()


@dp.message_handler(state=UserState.birthday)
async def get_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    if validation.is_valid_date(data['birthday']):
        await message.answer(f"Name: {data['username']}\n"
                         f"Birthday: {data['birthday']}")
        DS.save({'username': data['username'], 'birthday': data['birthday']})
        await state.finish()
    else:
        await message.answer('Invalid data!')



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
     asyncio.run(main())

