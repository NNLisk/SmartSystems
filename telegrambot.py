from dotenv import load_dotenv, dotenv_values
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import weather, lunch, news, jokes_quotes

import userbase

BOT_TOKEN = "token"

waiting_for_city = set()  

# START THE BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username

    userbase.add_user(user_id, user_name)
    ## User location can also be saved here?

    await update.message.reply_text(
        "GOOOOOOOOD MOOOORNINNGG VIETNAAMMM\n\n"
        "I can help you with weather forecasts! Just mention 'weather' in your message."

        "please, accept the use of your location"
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

            # Immediately fetch and show weather
            weather_message = await weather.get_weather_message(user_id)
            await update.message.reply_text(weather_message)
        else:
            await update.message.reply_text("Could not find that city. Please try again or use /start")
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
        m = await build_morning_message(user_id)
        await update.message.reply_text(m) 


async def build_morning_message(user_id):
    m = "GOOOOOOOOD MOOOORNINNGG VIETNAAMMM"

    m += "\n\n=== Weather ===\n\n"

    weather_message = await weather.get_weather_message(user_id)
    if weather_message:
        m += weather_message
    else:
        m += "No location given"

    m += "\n\n=== News ===\n\n"

    
    m += news.news_for_user(user_id)

    m += "=== Enterntainment ===\n\n"

    quote = await jokes_quotes.get_quote()
    m += f"{jokes_quotes.format_quote(quote)}\n\n"

    joke = await jokes_quotes.get_joke()
    m += f"{jokes_quotes.format_joke(joke)}"


    return m

    
    




def main():
    config = dotenv_values(".env")
    BOT_TOKEN = config.get("BOT_TOKEN")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, weather.handle_location))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()