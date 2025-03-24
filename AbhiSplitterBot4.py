from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

# Bot token from BotFather (replace with your own)
TOKEN = "7858555131:AAF9ft5Fr8JJ78nEcdGJkKItqqIA287hnD"

# In-memory storage (temporary)
payments = {}  # Format: {user_id: [{"amount": float, "people": list, "split": float, "photo": str}]}

# Conversation states
AMOUNT, PEOPLE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to AbhiSplitterBot! Use:\n/add - Split a payment\n/history - View transactions\n/clear - Reset records\n/upload - Add a receipt"
    )

# Add Payment Feature
async def add_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter the total amount (e.g., 100):")
    return AMOUNT

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
        context.user_data["amount"] = amount
        await update.message.reply_text("Enter people to split with (e.g., @alice @bob):")
        return PEOPLE
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
        return AMOUNT

async def handle_people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people = update.message.text.split()
    amount = context.user_data["amount"]
    split = amount / len(people)
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Someone"
    
    # Store payment
    if user_id not in payments:
        payments[user_id] = []
    payments[user_id].append({"amount": amount, "people": people, "split": split, "photo": None})
    
    # Notify each person (simulated in same chat for now)
    for person in people:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"{person}, you owe {split:.2f} for a payment by @{username}"
        )
    
    await update.message.reply_text("Payment split recorded! Add a receipt with /upload if needed.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Canceled.")
    return ConversationHandler.END

# Check Payment History
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in payments or not payments[user_id]:
        await update.message.reply_text("No payment history yet.")
        return
    
    response = "Your Payment History:\n"
    total_owed = 0
    for i, payment in enumerate(payments[user_id], 1):
        total_owed += payment["split"]
        photo_note = " (with receipt)" if payment["photo"] else ""
        response += f"{i}. Amount: {payment['amount']:.2f}, Split: {payment['split']:.2f} with {', '.join(payment['people'])}{photo_note}\n"
    response += f"Total you owe: {total_owed:.2f}"
    await update.message.reply_text(response)

# Clear Payment Records
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="clear_yes"), InlineKeyboardButton("No", callback_data="clear_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Are you sure you want to clear all records?", reply_markup=reply_markup)

async def clear_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if query.data == "clear_yes":
        if user_id in payments:
            del payments[user_id]
            await query.edit_message_text("All records cleared!")
        else:
            await query.edit_message_text("No records to clear.")
    else:
        await query.edit_message_text("Action canceled.")

# Upload Receipts
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in payments or not payments[user_id]:
        await update.message.reply_text("No payments to attach a receipt to. Use /add first.")
        return
    await update.message.reply_text("Please send an image as a receipt.")
    context.user_data["awaiting_photo"] = True

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_photo"):
        return
    
    user_id = update.message.from_user.id
    photo_file = update.message.photo[-1].file_id  # Get the highest resolution photo
    payments[user_id][-1]["photo"] = photo_file  # Attach to latest payment
    
    await update.message.reply_text("Receipt uploaded and linked to your latest payment!")
    context.user_data["awaiting_photo"] = False

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add payment conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_payment)],
        states={
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)],
            PEOPLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_people)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Other command handlers
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(clear_callback, pattern="^clear_"))
    
    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()