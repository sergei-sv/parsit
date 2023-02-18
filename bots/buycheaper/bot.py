import csv
import json
import logging
import os
import pandas as pd
import re
import subprocess
from urllib.parse import quote_plus

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hstrikethrough, hlink
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = 5550623930:AAGY3AjL855emSHFWp3LLTYU8TfvzaizShc

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # start_buttons = ['Somat']
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(*start_buttons)

    # await message.reply('Ready to work!', reply_markup=keyboard)
    welcome_msg = (
        'Готов к поиску!\nНачни со слова "найти". Например:\n\t\t"найти '
        'порошок somat 3 кг"\n\t\t"найти подгузники pampers 9-15 кг')
    await message.answer(welcome_msg)


@dp.message_handler(Text(startswith='найти', ignore_case=True))
async def get_discount(message: types.Message):
    await message.answer('Поиск...')

    search_phrase = re.search(r'[Нн]айти (.*)', message.text).group(1)
    base_command = ('scrapy crawl {spider} -a search={search} -O '
                    '/app/bots/output/res.csv')
    command = base_command.format(
        spider='shops.ostrovshop_by_search',
        search=search_phrase.replace(' ', '+'))
    subprocess.run(command.split())

    csv_file = pd.read_csv('/app/bots/output/res.csv')
    csv_file.sort_values('price', axis=0, ascending=True, inplace=True)
    csv_file.to_csv('/app/bots/output/sorted_res.csv')

    with open(
            '/app/bots/output/sorted_res.csv', 'r') as f:
        for i in csv.DictReader(f):
            title = hlink(i.get("title"), i.get("url"))
            price = i.get("price")
            discount = f'скидка: {i.get("discount")}'
            old_price = (
                f'цена до скидки: {hstrikethrough(i.get("old_price"))}'
                if i.get("discount") != '0' else '')
            card = '\n'.join((title, price, discount, old_price))
            await message.answer(card, disable_web_page_preview=True)


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
