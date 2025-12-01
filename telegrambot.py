from dotenv import load_dotenv, dotenv_values
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp

BOT_TOKEN = "token"
user_locations = {}
waiting_for_city = set()  

# START THE BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "GOOOOOOOOD MOOOORNINNGG VIETNAAMMM\n\n"
        "I can help you with weather forecasts! Just mention 'weather' in your message."
    )

# SHOW LOCATION BUTTON
async def show_location_button(update: Update):
    location_button = KeyboardButton(text="📍 Allow access my location", request_location=True)
    #manual_button = KeyboardButton(text="✍️ Type City Name")
    keyboard = ReplyKeyboardMarkup(
        [[location_button]], 
        one_time_keyboard=True, 
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        "📍 Please allow access your location to get weather information:\n\n"
        "• Tap 'Allow access my location' (mobile)\n"
        "• Or enter your /city",
        reply_markup=keyboard
    )

# HANDLE LOCATION
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    user_id = update.effective_user.id
    
    user_locations[user_id] = {
        'latitude': location.latitude,
        'longitude': location.longitude
    }
    
    # Immediately fetch and show weather
    weather_data = await get_weather(location.latitude, location.longitude)
    weather_message = format_weather_message(weather_data)
    await update.message.reply_text(weather_message, reply_markup=ReplyKeyboardRemove())

# GET COORDINATES FROM CITY NAME
async def get_coordinates(city_name: str) -> dict:
    """Get coordinates from city name using geocoding API"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {'name': city_name, 'count': 1, 'language': 'en', 'format': 'json'}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('results'):
                    result = data['results'][0]
                    return {
                        'latitude': result['latitude'],
                        'longitude': result['longitude'],
                        'name': result['name'],
                        'country': result.get('country', '')
                    }
    return None

# GET WEATHER DATA
async def get_weather(lat: float, lon: float) -> dict:
    """Fetch weather data from Open-Meteo API (free, no API key needed)"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m',
        'hourly': 'temperature_2m,precipitation_probability',
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
        'timezone': 'auto',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

# FORMAT WEATHER MESSAGE
def format_weather_message(weather_data: dict) -> str:
    """Format weather data into a readable message"""
    if not weather_data:
        return "Could not fetch weather data. Please try again."
    
    current = weather_data.get('current', {})
    daily = weather_data.get('daily', {})
    
    # Weather code interpretation 
    weather_codes = {
        0: "☀️ Clear sky",
        1: "🌤️ Mainly clear",
        2: "⛅ Partly cloudy",
        3: "☁️ Overcast",
        45: "🌫️ Foggy",
        48: "🌫️ Foggy",
        51: "🌦️ Light drizzle",
        61: "🌧️ Light rain",
        63: "🌧️ Moderate rain",
        65: "🌧️ Heavy rain",
        71: "🌨️ Light snow",
        73: "🌨️ Moderate snow",
        75: "🌨️ Heavy snow",
        95: "⛈️ Thunderstorm"
    }
    
    weather_code = current.get('weather_code', 0)
    weather_desc = weather_codes.get(weather_code, "🌍 Unknown")
    
    if daily and 'temperature_2m_min' in daily and 'temperature_2m_max' in daily:
        min_temp = daily['temperature_2m_min'][0]
        max_temp = daily['temperature_2m_max'][0]
        precipitation = daily['precipitation_sum'][0] if 'precipitation_sum' in daily else 0
        message = (
            f"WEATHER TODAY\n"
            f"{weather_desc}\n"
            f"🌡️ Min: {min_temp}°C | Max: {max_temp}°C 💧 {precipitation} mm"
        )
    else:
        # fallback to current temp if daily not available
        message = (
            f"WEATHER TODAY\n"
            f"{weather_desc}\n"
            f"🌡️ {current.get('temperature_2m', 'N/A')}°C 💧 {current.get('precipitation', 0)} mm"
        )
    
    return message

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
        coords = await get_coordinates(text)
        
        if coords:
            user_locations[user_id] = {
                'latitude': coords['latitude'],
                'longitude': coords['longitude']
            }
            # Immediately fetch and show weather
            weather_data = await get_weather(coords['latitude'], coords['longitude'])
            weather_message = format_weather_message(weather_data)
            await update.message.reply_text(weather_message)
        else:
            await update.message.reply_text("Could not find that city. Please try again or use /start")
        return

    # User mentions "weather"
    if 'weather' in text_lower:
        if user_id in user_locations:
            # User has location saved - show weather directly
            loc = user_locations[user_id]
            weather_data = await get_weather(loc['latitude'], loc['longitude'])
            weather_message = format_weather_message(weather_data)
            await update.message.reply_text(weather_message)
        else:
            # First time - show location button
            await show_location_button(update)
    
    elif 'news' in text_lower:
        await update.message.reply_text("lorem ipsum some news to be developed")

def main():
    config = dotenv_values(".env")
    BOT_TOKEN = config.get("BOT_TOKEN")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()