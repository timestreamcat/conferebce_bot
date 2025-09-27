
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

dp = Dispatcher()

@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
