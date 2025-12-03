import aiohttp
import xml.etree.ElementTree as ET
import re

LUNCH_URL = "https://www.compass-group.fi/menuapi/feed/rss/current-day?costNumber=3424&language=en"

async def get_lunch_menu():
    async with aiohttp.ClientSession() as session:
        async with session.get(LUNCH_URL) as response:
            if response.status == 200:
                xml_data = await response.text()
                return format_lunch_menu(xml_data)
            else:
                return "Could not fetch lunch menu."

def format_lunch_menu(xml_data: str) -> str:
    try:
        root = ET.fromstring(xml_data)
        description = root.find('.//item/description')
        if description is None or not description.text:
            return "No lunch menu for today."
        html_text = description.text
        
        # Remove HTML tags and clean up
        text = re.sub('<[^>]+>', '\n', html_text)
        text = re.sub('\n+', '\n', text)
        
        # Extract menu items (lines that aren't empty and aren't section headers)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "No lunch for today."
        
        message = "🍽️ LUNCH TODAY 11:00–14:00\n"
        
        for line in lines:
            if line.endswith(':'):
                message += f"\n**{line}**\n"
            else:
                # Remove dietary labels in parentheses for cleaner display
                clean_line = re.sub(r'\s*\([^)]*\)\s*$', '', line)
                message += f"• {clean_line}\n"
        
        return message
        
    except Exception as e:
        return f"Error parsing menu: {str(e)}"