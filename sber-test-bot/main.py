import json
import logging
import re
from datetime import datetime
import aiohttp
import asyncio
import yaml
from aiogram import Bot, Dispatcher, executor, types


def get_config():
    with open('config/dev.yml', 'r') as file:
        conf = yaml.load(file)
    return conf

CONFIG = get_config()['bot']
API_TOKEN = CONFIG['api_token_prod']
URL = CONFIG['url']
HEADER = {'Content-Type': 'application/json'}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_count_people(user_input):
    try:
        find_count = re.search(r' ([0-9]?[0-9])$', user_input)
        logging.INFO(f"{find_count}")
        count_people = int(find_count)
    except (ValueError, IndexError, TypeError):
        count_people = None
    if count_people and 0 < count_people < 50:
        return count_people
    else:
        return None

def get_booking_time(user_input):
    # TODO Нет проверки на прошедшее время
    # TODO Нет проверки на то что все столики заняты
    # TODO Нету заложения 2-х часового резерва в бронь конкретного столика
    try:
        find_time = re.search(r'[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]', user_input)
        booking_time = datetime.strptime(find_time[0], "%Y-%m-%d %H:%M")
    except (ValueError, IndexError, TypeError):
        booking_time = None
    return booking_time

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Если ты хочешь забронировать столик, напиши /set_booking YYYY-MM-DD h:m 4 - (количество человек),\n Если хочешь посмотреть свою бронь напиши /my_booking")

@dp.message_handler(commands=['set_booking'])
async def set_booking(message: types.Message):

    data_booking = {}
    data_booking['chat_id'] = message.chat.id
    data_booking['booking_time'] = get_booking_time(message.text)
    data_booking['count_people'] = get_count_people(message.text)
    if not data_booking['booking_time']:
        return await message.reply('Некорректный формат даты/времени, пожалуйста введите дату и время бронирования согласно формату YYYY-MM-DD h:m')
    elif not data_booking['count_people']:
        return await message.reply('Некорректное число людей, введите число от 1-50 в формате /set_booking YYYY-MM-DD h:m 4 - где 4 - число людей')
    send_data = json.dumps(data_booking, indent=4, sort_keys=True, default=str)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=URL, data=send_data, headers=HEADER) as resp:
            if resp.status == 200:
                return await message.answer('Закрепляю столик за вами')
            else:
                return await message.answer('Что-то не так попробуйте позже')

@dp.message_handler(commands=['my_booking'])
async def my_booking(message: types.Message):
    url = URL + str(message.chat.id) + '/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADER) as resp:
            # TODO сделать форматирование сообщения
            output = await resp.text()
            await message.answer(output)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)