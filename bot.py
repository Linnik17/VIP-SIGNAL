import asyncio
import re

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN
from storage import add, get
from engine import analyze
from users import set_user, get_user, is_owner
from graphics import make_graph

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚡ SIGNAL", callback_data="sig")],
    [InlineKeyboardButton(text="📊 GRAPH", callback_data="graph")],
    [InlineKeyboardButton(text="👑 ADMIN", callback_data="admin")]
])


def parse(text):
    return [float(x) for x in re.findall(r"\d+\.?\d*", text)]


# ⏳ fake animation
async def typing(msg):
    await asyncio.sleep(0.5)


@dp.message()
async def msg(m: types.Message):
    uid = m.from_user.id

    if m.text == "/start":
        await m.answer("💎 ULTRA VIP PLATFORM", reply_markup=menu)
        return

    nums = parse(m.text)

    if nums:
        for n in nums:
            add(n)

        await m.answer(analyze(get()) or "⏳ недостаточно данных", reply_markup=menu)
        return

    await m.answer("Отправь коэффициенты")


# 🎛 CALLBACKS
@dp.callback_query()
async def cb(c: types.CallbackQuery):
    uid = c.from_user.id

    # ⚡ SIGNAL
    if c.data == "sig":
        await c.message.answer(analyze(get()) or "⏳ нет сигнала")

    # 📊 GRAPH
    if c.data == "graph":
        path = make_graph(get())
        await c.message.answer_photo(types.FSInputFile(path))

    # 👑 ADMIN PANEL
    if c.data == "admin":
        if is_owner(uid):
            set_user(uid, "ELITE")
            await c.message.answer("👑 ADMIN ACCESS GRANTED\n💎 YOU ARE OWNER")
        else:
            await c.message.answer("🚫 NO ACCESS")

    await c.answer()


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
