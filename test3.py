import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

BOT_TOKEN = '8350350899:AAFSG_rc0vuEYis37oUTNr5mQOuW3GZo4ls'
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def get_channel_id(message: types.Message):
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        channel_title = message.forward_from_chat.title
        await message.answer(
            f"📊 Информация о канале:\n"
            f"Название: {channel_title}\n"
            f"ID: `{channel_id}`\n"
            f"Username: @{message.forward_from_chat.username}",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "📝 Для получения ID канала:\n"
            "1. Добавьте меня в канал как администратора\n"
            "2. Перешлите любое сообщение из канала мне"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())