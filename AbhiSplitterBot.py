import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Replace with your bot token
TOKEN = "7858555131:AAF9ft5Fr8JJ78nEcdGJkKItqqIA287hnDM"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Command handler for /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Hello! Abhi Splitter Bot is running.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
