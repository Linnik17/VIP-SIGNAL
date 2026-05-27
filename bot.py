import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from db import add, get
from engine import analyze, stats
from signal import generate_signal

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 Анализ", callback_data="a")],
    [InlineKeyboardButton(text="📊 Статистика", callback_data="s")],
    [InlineKeyboardButton(text="⚡ AUTO SIGNAL", callback_data="sig")],
])

def nums(text):
    return [float(x) for x in re.findall(r"\d+(\.\d+)?", text)]


@dp.message()
async def msg(m: types.Message):
    if m.text == "/start":
        await m.answer("💎 VIP CRASH BOT ONLINE", reply_markup=menu)
        return

    n = nums(m.text)

    if n:
        for i in n:
            add(i)

        await m.answer(analyze(get()), reply_markup=menu)
        return

    await m.answer("Отправь коэффициенты", reply_markup=menu)


@dp.callback_query()
async def cb(c: types.CallbackQuery):
    h = get()

    if c.data == "a":
        await c.message.answer(analyze(h))

    if c.data == "s":
        st = stats(h)
        await c.message.answer(f"""
📊 STAT

🔵 low: {st['low']}%
🟡 mid: {st['mid']}%
🔴 high: {st['high']}%
""")

    if c.data == "sig":
        await c.message.answer(generate_signal())

    await c.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
