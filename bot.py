import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from db import add_value, get_history
from analyzer import smart_analysis, probability_score

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🎛 КНОПКИ
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📊 Анализ", callback_data="analyze")],
    [InlineKeyboardButton(text="📈 Статистика", callback_data="stats")],
    [InlineKeyboardButton(text="🎯 Шанс", callback_data="chance")],
])

def extract_numbers(text):
    return [float(x) for x in re.findall(r"\d+(\.\d+)?", text)]


@dp.message()
async def handler(message: types.Message):
    text = message.text

    if text == "/start":
        await message.answer("🤖 Crash PRO Bot активирован", reply_markup=menu)
        return

    numbers = extract_numbers(text)

    if numbers:
        for n in numbers:
            add_value(n)

        await message.answer(
            f"📥 Добавлено: {numbers}\n\n{smart_analysis(get_history())}",
            reply_markup=menu
        )
        return

    await message.answer("Отправь коэффициенты или нажми меню", reply_markup=menu)


# 🎛 КНОПКИ
@dp.callback_query()
async def callbacks(call: types.CallbackQuery):
    history = get_history()

    if call.data == "analyze":
        await call.message.answer(smart_analysis(history))

    elif call.data == "stats":
        score = probability_score(history)
        await call.message.answer(f"""
📊 СТАТИСТИКА

🔵 низкие: {score['low']}%
🟡 средние: {score['mid']}%
🔴 высокие: {score['high']}%
""")

    elif call.data == "chance":
        await call.message.answer("🎯 Пока базовый режим, дальше добавим AI-предикт")

    await call.answer()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
