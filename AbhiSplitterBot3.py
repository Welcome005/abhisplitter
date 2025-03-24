import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

TOKEN = "7858555131:AAF9ft5Fr8JJ78nEcdGJkKItqqIA287hnDM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Temporary storage for transactions (Replace with DB later)
payment_data = {}

# Main menu buttons (in typing section)
main_menu_typing = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Add Payment")],
        [KeyboardButton(text="📜 Check History")],
        [KeyboardButton(text="🗑 Clear Chat")]
    ],
    resize_keyboard=True
)

# Main menu buttons (in chat)
main_menu_chat = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Add Payment", callback_data="add_payment")],
        [InlineKeyboardButton(text="📜 Check History", callback_data="check_history")]
    ]
)

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Clearing previous chats...", parse_mode="Markdown")
    await asyncio.sleep(1)
    await message.delete()
    await message.answer("Select an option below:", reply_markup=main_menu_typing)

@dp.message()
async def handle_buttons(message: Message):
    user_id = message.from_user.id
    
    if message.text == "➕ Add Payment":
        payment_data[user_id] = {}
        await message.answer("Enter the total amount to split:")
    
    elif user_id in payment_data and "amount" not in payment_data[user_id]:
        try:
            amount = float(message.text)
            payment_data[user_id]["amount"] = amount
            await message.answer("Enter the number of persons to split among:")
        except ValueError:
            await message.answer("Please enter a valid amount.")
    
    elif user_id in payment_data and "persons" not in payment_data[user_id]:
        try:
            persons = int(message.text)
            if persons <= 0:
                await message.answer("Number of persons must be greater than zero.")
                return
            
            payment_data[user_id]["persons"] = persons
            amount_per_person = payment_data[user_id]["amount"] / persons
            await message.answer(f"Each person should pay: {amount_per_person:.2f}")
        except ValueError:
            await message.answer("Please enter a valid number of persons.")
    
    elif message.text == "📜 Check History":
        await message.answer("History feature coming soon!")
    
    elif message.text == "🗑 Clear Chat":
        await message.answer("Clearing previous chats...", parse_mode="Markdown")
        await asyncio.sleep(1)
        await message.delete()
        await message.answer("Chat cleared!", reply_markup=main_menu_typing)

@dp.callback_query()
async def handle_inline_buttons(callback: types.CallbackQuery):
    if callback.data == "add_payment":
        await callback.message.answer("Enter the total amount to split:")
        payment_data[callback.from_user.id] = {}
    elif callback.data == "check_history":
        await callback.message.answer("History feature coming soon!")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
