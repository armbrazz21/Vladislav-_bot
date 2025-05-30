
import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup

API_TOKEN = '7740237696:AAEvvjyVqwEhCUgS0Nk6zWwVCr9HNqEexbo'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def fetch_binance_usdt():
    url = 'https://p2p.binance.com/en/trade/buy/USDT?fiat=CZK&payment=ALL'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # ЭТО ПРОСТО ЗАГЛУШКА ДЛЯ ТЕСТА – НАСТОЯЩИЕ ДАННЫЕ НУЖНО ПОДКЛЮЧИТЬ ЧЕРЕЗ API
    return {'binance': {'buy': 23.1, 'sell': 24.0}}

async def fetch_bybit_usdt():
    return {'bybit': {'buy': 23.3, 'sell': 23.9}}

async def fetch_okx_usdt():
    return {'okx': {'buy': 23.2, 'sell': 24.1}}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для поиска лучших курсов P2P. Используй /check, чтобы узнать текущие предложения.")

@dp.message_handler(commands=['check'])
async def send_best_rates(message: types.Message):
    binance = await fetch_binance_usdt()
    bybit = await fetch_bybit_usdt()
    okx = await fetch_okx_usdt()
    
    rates = {**binance, **bybit, **okx}
    reply = "🔎 Лучшие курсы для USDT:\n"
    for exchange, data in rates.items():
        diff = round((data['sell'] - data['buy']) / data['buy'] * 100, 2)
        reply += f"{exchange.capitalize()} – Покупка: {data['buy']} CZK, Продажа: {data['sell']} CZK (разница {diff}%)\n"
    await message.reply(reply)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
