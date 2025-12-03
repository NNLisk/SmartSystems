from dotenv import load_dotenv, dotenv_values
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import weather
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
    )


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
            weather.user_locations[user_id] = {
                'latitude': coords['latitude'],
                'longitude': coords['longitude']
            }
            userbase.save_user_location(user_id, coords["latitude"], coords["longitude"])

            # Immediately fetch and show weather
            weather_data = await weather.get_weather(coords['latitude'], coords['longitude'])
            weather_message = weather.format_weather_message(weather_data)
            await update.message.reply_text(weather_message)
        else:
            await update.message.reply_text("Could not find that city. Please try again or use /start")
        return

    # User mentions "weather"
    if 'weather' in text_lower:
        if user_id in weather.user_locations:
            # User has location saved - show weather directly
            loc = weather.user_locations[user_id]
            weather_data = await weather.get_weather(loc['latitude'], loc['longitude'])
            weather_message = weather.format_weather_message(weather_data)
            await update.message.reply_text(weather_message)
        else:
            # First time - show location button
            await weather.show_location_button(update)
    
    elif 'news' in text_lower:
        await update.message.reply_text("lorem ipsum some news to be developed")

    if "morning" in text_lower:
        m = await build_morning_message(user_id)
        await update.message.reply_text(m) 


async def build_morning_message(user_id):
    m = "GOOOOOOOOD MOOOORNINNGG VIETNAAMMM\n\n"

    userLocation = userbase.get_user_location(user_id)
    if userLocation != None:
        weather_data = await weather.get_weather(userLocation["latitude"], userLocation["longitude"])
        weather_message = weather.format_weather_message(weather_data)
        m += weather_message
    else:
        m += "No location given"

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