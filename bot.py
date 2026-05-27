import asyncio
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from storage import add, get
from engine import predict, format_prediction
from users import set_user, get_user, is_owner

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 💎 меню
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚡ SIGNAL", callback_data="sig")],
    [InlineKeyboardButton(text="📊 GRAPH", callback_data="graph")],
    [InlineKeyboardButton(text="🔐 ACCESS", callback_data="access")],
])

def parse(text):
    return [float(x) for x in re.findall(r"\d+\.?\d*", text)]


# ✨ АНИМАЦИЯ
async def loading(msg):
    for i in range(3):
        await asyncio.sleep(0.3)
        await msg.edit_text("⏳ анализ" + "." * (i + 1))


# 🚀 START
@dp.message()
async def msg(m: types.Message):
    uid = m.from_user.id

    if m.text == "/start":
        await m.answer("💎 VIP SYSTEM ONLINE", reply_markup=menu)
        return

    nums = parse(m.text)

    if nums:
        for n in nums:
            add(n)

        p = predict(get())

        await m.answer(format_prediction(p), reply_markup=menu)
        return

    await m.answer("Отправь коэффициенты")


# 🎛 CALLBACKS
@dp.callback_query()
async def cb(c: types.CallbackQuery):
    uid = c.from_user.id

    if c.data == "sig":
        await c.message.answer("⚡ генерирую сигнал...")
        await asyncio.sleep(1)
        await c.message.answer(format_prediction(predict(get())))

    # 📊 график (заглушка под будущий matplotlib)
    if c.data == "graph":
        await c.message.answer("📊 график пока подключается...")

    # 🔐 VIP выдача (ТОЛЬКО ВЛАДЕЛЕЦ)
    if c.data == "access":
        if is_owner(uid):
            set_user(uid, "ELITE")
            await c.message.answer("💎 доступ выдан: ELITE")
        else:
            await c.message.answer("🚫 нет доступа")

    await c.answer()


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
