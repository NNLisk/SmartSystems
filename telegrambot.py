from dotenv import load_dotenv, dotenv_values
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


BOT_TOKEN = "token"


# START THE BOT
async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GOOOOOOOOD MOOOORNINNGG VIETNAAMMM")


# BASIC MESSAGE LISTENING AND RESPONSES
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if 'weather' in text:
        await update.message.reply_text("lorem ipsum weather infor to be developed")
    elif 'news' in text:
        await update.message.reply_text("lorem ipsum some news to be developed")

def main():

    # CREATE THE .env FILE AND PUT A TOKEN THERE
    config = dotenv_values(".env")
    BOT_TOKEN = config.get("BOT_TOKEN")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # in here scheduling jobs for sending messages in the morning

    app.run_polling()

if __name__ == "__main__":
    main()