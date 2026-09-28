from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import random

router = Router()
balances = {}

@router.message(CommandStart())
async def start(message: Message):
    uid = message.from_user.id
    if uid not in balances:
        balances[uid] = 1000000
    await message.answer(f"🎰 Салам {message.from_user.first_name}!\nАкчаң: {balances[uid]} сом\n\nОйноо учун жаз:\nкызыл 100\nкара 100\n0 100")

@router.message(F.text.lower().contains("кызыл"))
async def red_bet(message: Message):
    await game(message, "кызыл")

@router.message(F.text.lower().contains("кара"))
async def black_bet(message: Message):
    await game(message, "кара")

@router.message(F.text.lower().contains("0"))
async def zero_bet(message: Message):
    await game(message, "0")

async def game(message: Message, choice):
    uid = message.from_user.id
    if uid not in balances:
        balances[uid] = 1000000
    try:
        bet = int(''.join(filter(str.isdigit, message.text)))
    except:
        bet = 100
    if bet <= 0:
        bet = 100
    if balances[uid] < bet:
        await message.answer(f"Акчаң жок! Акчаң: {balances[uid]}")
        return
    num = random.randint(0, 36)
    if num == 0:
        col = "0"
        emo = "🟢"
    elif num % 2 == 0:
        col = "кара"
        emo = "⚫"
    else:
        col = "кызыл"
        emo = "🔴"
    if choice == col:
        win = bet*14 if col=="0" else bet
        balances[uid] += win
        await message.answer(f"{emo} {num} {col} тушту!\n🎉 Уттуң +{win}\nАкчаң: {balances[uid]}")
    else:
        balances[uid] -= bet
        txt = f"{emo} {num} {col} тушту!\n😭 Утулдуң -{bet}\nАкчаң: {balances[uid]}"
        if balances[uid] <= 0:
            balances[uid] = 1000000
            txt += "\n\nАкчаң бүттү, 1 000 000 кайра бердим! Миллионерсиң дагы 😎"
        await message.answer(txt)
