import logging
import requests
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)


BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_TELEGRAM_ID = 6335543803
WALLET_IMAGE_PATH = "kcash_wallet.jpeg"

logging.basicConfig(level=logging.INFO)

WAITING_FOR_NAME = 1
user_counter = 0
registered_users = {}

INSTRUCTIONS = (
    "📌 *PLEASE READ THIS CAREFULLY BEFORE YOU CLICK ANYTHING*\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "‼️ *COPY THESE INSTRUCTIONS NOW.*\n"
    "‼️ *Once you tap NEXT, this message will disappear and will NOT come back unless you restart the process.*\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "This is a Play-to-Earn platform where you complete simple tasks like playing games and dropping feedback, and you get paid real money for it.\n\n"
    "💼 *What You Need Before Starting*\n"
    "You will need three things — a Gmail account, the KGEN app, and an X (Twitter) account. Make sure you have all three ready.\n\n"
    "🔗 *Step 1 — Mint Your POG First*\n"
    "Use the first link to mint your POG. You will be asked some questions about how you want it set up. Do this before anything else.\n\n"
    "📲 *Step 2 — Download the KGEN App*\n"
    "Use the second link to download KGEN on your phone. Log in with the same Gmail you used to register.\n\n"
    "👥 *Step 3 — Join the Clan*\n"
    "Use the third link to join the clan. This unlocks more tasks and earning opportunities.\n\n"
    "🐦 *Step 4 — Set Up Your X Account*\n"
    "Use the fourth link to download X. You can create a new account or use an existing active one.\n\n"
"🎮 *How You Earn*\n"
    "Every task you complete earns you KCash. Current conversion rate:\n"
    "2000 KCash = $0.8 which is roughly ₦1,120\n\n"
    "⏳ *How Long Does It Take to Get Paid?*\n"
    "After you submit a task, review takes 10 to 15 days. New tasks are added regularly so stay active!\n\n"
    "✍️ *Tips for Getting Approved*\n"
    "Base your reviews on your own experience. Keep it honest and in your own words. Always submit before the deadline.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "‼️ *REMINDER: Copy these instructions before tapping NEXT. They will not show again.*\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "Good luck and start earning 💰🎮"
)

LINKS_MESSAGE = (
    "🚀 *You are all set! Here are your links:*\n\n"
    "1️⃣ *Mint your POG:*\nhttps://link.kgen.io/bXSovE\n\n"
    "2️⃣ *Download KGEN app:*\nhttps://play.google.com/store/apps/details?id=com.indiggcommunity\n\n"
    "3️⃣ *Join the Clan:*\nhttps://link.kgen.io/MEqatT\n\n"
    "4️⃣ *Download X app:*\nhttps://play.google.com/store/apps/details?id=com.twitter.android\n\n"
    "Follow the steps in order and you will be earning KCash in no time! 💪"
)

WALLET_CAPTION = (
    "💰 *This is what your wallet will look like once your task is validated!*\n\n"
    "That green arrow points to your KCash balance — that is real money waiting to be withdrawn.\n"
    "The more tasks you complete, the bigger that number gets 📈\n\n"
    "When you are ready to convert your KCash to Naira, come back here and we will sort you out straight to your bank account. 👊"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *STUDENTS COMPANION* 🎓\n\n"
        "Your gateway to earning with KGEN and building your financial freedom as a student.\n\n"
        "To get started, please *type your full name* below 👇",
        parse_mode="Markdown",
    )
    return WAITING_FOR_NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_counter
    chat_id = update.message.chat_id
    user_name = update.message.text.strip()
    user_counter += 1
    user_number = user_counter
    registered_users[chat_id] = {"name": user_name, "user_number": user_number}
    await context.bot.send_message(
        chat_id=OWNER_TELEGRAM_ID,
        text=f"New user joined STUDENTS COMPANION!\n{user_name} — User {user_number}"
    )
    await update.message.reply_text(
        f"✅ Welcome *{user_name}*! You have been registered as *User {user_number}*.\n\n"
        "Your instructions are below — read carefully before proceeding 👇",
        parse_mode="Markdown",
    )
    keyboard = [[InlineKeyboardButton("✅ I have copied the instructions — NEXT ➡️", callback_data="next_delete")]]
    await update.message.reply_text(
        INSTRUCTIONS,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return ConversationHandler.END

async def handle_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    await query.message.delete()
    await context.bot.send_message(
        chat_id=chat_id,
        text=LINKS_MESSAGE,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    try:
        with open(WALLET_IMAGE_PATH, "rb") as photo:
            await context.bot.send_photo(
chat_id=chat_id,
                photo=photo,
                caption=WALLET_CAPTION,
                parse_mode="Markdown"
            )
    except Exception as e:
        logging.error(f"Failed to send wallet image: {e}")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Type /start to begin your journey with STUDENTS COMPANION 🎓"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={WAITING_FOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)]},
        fallbacks=[MessageHandler(filters.ALL, fallback)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(handle_next, pattern="^next_delete$"))
    app.add_handler(MessageHandler(filters.ALL, fallback))
    print("🤖 STUDENTS COMPANION bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
