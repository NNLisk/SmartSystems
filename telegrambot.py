from dotenv import load_dotenv, dotenv_values
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import weather, lunch, news, jokes_quotes, sisu_calendar
import userbase
from AI_advisor import get_funny_day_rating
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler



BOT_TOKEN = "token"

waiting_for_city = set()  

# START THE BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username

    userbase.add_user(user_id, user_name)
    ## User location can also be saved here?

    await update.message.reply_text(
        "GOOOOOOOOD MOOOORNINNGG VIETNAM\n"
        "(Bye the way, it's a good movie, highly recommended!)\n\n"
        "I'm your day brightening bot 😎! Before we get started, I just need a few permissions from you so I can provide **customized info**."       
    )

    await weather.show_location_button(update)



# BASIC MESSAGE LISTENING AND RESPONSES
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text_lower = text.lower()
    user_id = update.effective_user.id

    # User clicked "Type City Name" button
    if text == "✍️ Type City Name" or text=="/city":
        waiting_for_city.add(user_id)
        await update.message.reply_text(
            "Please type your city name:",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    # User is typing city name after clicking the button
    if user_id in waiting_for_city:
        waiting_for_city.remove(user_id)
        coords = await weather.get_coordinates(text)
        
        if coords:
            userbase.save_user_location(user_id, coords["latitude"], coords["longitude"])
            await update.message.reply_text(
                "Awesome! Location saved.\n\n"
                "Next, let's get your Sisu calendar synced. Please use command /ucal to link it."
            )
        else:
            await update.message.reply_text("Hmm, I couldn't find that city. 🤔 Please try again or tap /start to begin fresh.")
        return
    
    if context.user_data.get("waiting_for_calendar_url"):
        # Save the URL in userbase
        userbase.update_calendar_url(user_id, text)
        context.user_data["waiting_for_calendar_url"] = False
        await update.message.reply_text("Got it! Your Sisu calendar is now linked.\n"
            "If you want to see today's **personalized morning message**, just tap /morning!")
        return

    if 'weather' in text_lower:
        weather_message = await weather.get_weather_message(user_id)
        
        if weather_message:
            await update.message.reply_text(weather_message)
        else:
            await weather.show_location_button(update)
    
    if 'news' in text_lower:
        await update.message.reply_text("lorem ipsum some news to be developed")

    if 'lunch' in text_lower:
        lunch_message = await lunch.get_lunch_menu()
        await update.message.reply_text(lunch_message)

    if "morning" in text_lower:
        await send_morning(update, context, user_id)

    if "ucal" in text_lower:
        await update.message.reply_text(
            "Great! To link your Sisu calendar, please answer this message with the URL from Sisu.\n\n"
            "How to get it:\n"
            "1. Log into Sisu\n"
            "2. Go to 'Study Calendar'\n"
            "3. Export into external calendar,  copy the URL and paste it here\n\n"
        )       
        context.user_data["waiting_for_calendar_url"] = True

    if "/attendance" in text_lower:
        keyboard = [
            [
                InlineKeyboardButton("🏫 I went", callback_data="attended_yes"),
                InlineKeyboardButton("💤 I stayed home", callback_data="attended_no")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "How was today? Be honest 😄\nDid you go to campus?",
            reply_markup=reply_markup
        )
    return

async def build_morning_message(user_id):
    m = "GOOOOOOOOD MOOOORNINNGG"

    m += "\n\n=== WEATHER TODAY ===\n"
    weather_message = await weather.get_weather_message(user_id)
    weather_text = weather_message if weather_message else "No location given" #for AI verdict
    if weather_message:
        m += weather_message
    else:
        m += "No location given"

    m += "\n\n=== TODAY'S LECTURES ===\n"
    events = sisu_calendar.get_todays_events(user_id)
    lectures_text = events
    m += events

    m += "\n\n=== TODAY'S LUNCH MENU ===\n"
    lunch_message = await lunch.get_lunch_menu() 
    m += lunch_message if lunch_message else "No lunch menu available\n"
    lunch_text = lunch_message if lunch_message else "No lunch menu available"

    attendance = userbase.get_attendance_summary(user_id) if hasattr(userbase, "get_attendance_summary") else "No logs"

    m += "\n\n=== VERDICT ===\n"
    verdict = await get_funny_day_rating(attendance, lectures_text, weather_text, lunch_text)
    m += verdict + "\n\n"
    
    m += "=== NEWS ===\n"    
    m += news.news_for_user(user_id)

    m += "P. S. Grab your daily dose of positivity by clicking a button below!\n"    
    return m

async def send_morning(update, context, user_id):
    text = await build_morning_message(user_id)
    keyboard = [
        [InlineKeyboardButton("💭 Quote", callback_data="get_quote"),
         InlineKeyboardButton("😂 Joke", callback_data="get_joke")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)



async def morning_buttons_handler(update, context):
    query = update.callback_query
    await query.answer() 

    if query.data == "get_quote":
        quote = await jokes_quotes.get_quote()
        await query.message.reply_text(jokes_quotes.format_quote(quote))
    elif query.data == "get_joke":
        joke = await jokes_quotes.get_joke()
        await query.message.reply_text(jokes_quotes.format_joke(joke))
    elif query.data == "attended_yes":
        userbase.save_attendance(query.from_user.id, True)
        await query.message.reply_text("🏫 Nice! Logged as *attended*. Your campus loyalty is noted 😎")

    elif query.data == "attended_no":
        userbase.save_attendance(query.from_user.id, False)
        await query.message.reply_text("💤 Logged as *stayed home*. A brave choice indeed.")


async def send_to_all(app):
    user_ids = userbase.get_user_ids()

    for uid in user_ids:
        m = build_morning_message(uid)
        try:
            await app.bot.send_message(
                chat_id = int(uid),
                text = m
            )
        except Exception as e:
            print(f"Failed to send to {uid}")
            

def setup_scheduler(app):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_to_all, "cron", hour=13, minutes=30, args=[application])
    scheduler.start()


def main():
    config = dotenv_values(".env")
    BOT_TOKEN = config.get("BOT_TOKEN")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, weather.handle_location))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(CallbackQueryHandler(morning_buttons_handler))


    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()