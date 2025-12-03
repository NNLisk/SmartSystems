import aiohttp
from typing import Dict, Any

# quotes
async def get_quote() -> Dict[str, Any]:
    url = "https://zenquotes.io/api/random"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    quote_data = data[0]
                    return {
                        'success': True,
                        'content': quote_data.get('q', ''),
                        'author': quote_data.get('a', 'Unknown')
                    }
                else:
                    return {
                        'success': False,
                        'error': 'API request failed'
                    }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

#jokes
async def get_joke() -> Dict[str, Any]:
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'setup': data.get('setup', ''),
                        'punchline': data.get('punchline', ''),
                        'type': data.get('type', 'general')
                    }
                else:
                    return {
                        'success': False,
                        'error': 'API request failed'
                    }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def format_quote(quote_data: Dict[str, Any]) -> str:
    if not quote_data.get('success'):
        return f"Couldn't get a quote. ({quote_data.get('error', 'Unknown error')})"
    
    content = quote_data.get('content', '')
    author = quote_data.get('author', 'Unknown')
    return f"💭 \"{content}\"\n\n— {author}"


def format_joke(joke_data: Dict[str, Any]) -> str:
    if not joke_data.get('success'):
        return f"Couldn't get a joke. ({joke_data.get('error', 'Unknown error')})"
    
    setup = joke_data.get('setup', '')
    punchline = joke_data.get('punchline', '')
    return f"{setup}\n\n{punchline}"


if __name__ == "__main__":

    import asyncio
    async def test():
        print("Quote of the day is")
        quote = await get_quote()
        print(format_quote(quote))
        print()
        
        print("Joke of the day is")
        joke = await get_joke()
        print(format_joke(joke))
    
    asyncio.run(test())