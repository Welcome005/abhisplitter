import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = "7858555131:AAF9ft5Fr8JJ78nEcdGJkKItqqIA287hnDM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    intro_text = (
        "🤖 **Welcome to Abhi Splitter Bot!**\n\n"
        "This bot helps you split expenses and remember payment locations easily. "
        "No more confusion about who paid how much and where! 💰📍\n\n"
        "**For complaints or suggestions:** abhishekdeokar005@gmail.com"
    )
    await message.answer(intro_text, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
