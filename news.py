from dotenv import load_dotenv, dotenv_values
import requests
import userbase
import random

token = dotenv_values(".env").get("CURRENTS_TOKEN")

# categories = [
#     "regional", "technology","lifestyle",
#     "business","general","programming",
#     "science","entertainment","world",
#     "sports","finance","academia",
#     "politics","health","opinion",
#     "food","game","fashion",
#     "academic","crap","travel",
#     "culture","economy","environment",
#     "art","music","notsure",
#     "CS","education","redundant",
#     "television","commodity","movie",
#     "entrepreneur","review","auto",
#     "energy","celebrity","medical",
#     "gadgets","design","EE",
#     "security","mobile","estate",
#     "funny"
# ]

news = [
    {'id': '8a4349a1-6383-4832-9274-962f8e769373', 'title': 'Putin Must Have Authorized Novichok Poisoning in Salisbury, UK Inquiry Finds', 'description': 'A police cordon around the residential area where Dawn Sturgess was exposed to the Novichok nerve agent in Salisbury, England, in 2018....', 'url': 'https://www.nytimes.com/2025/12/04/world/europe/putin-novichok-salisbury-skripal-poisoning.html', 'author': 'Lizzie Dearden', 'image': 'None', 'language': 'en', 'category': ['world'], 'published': '2025-12-04 15:25:01 +0000'},
    {'id': '496139a9-0c62-4e15-b4f7-3893c49b140a', 'title': 'Trade Setup For Dec. 5: Nifty Faces Significant Resistance At 26,100 As All Eyes On RBI MPC Decision', 'description': 'A positive policy tone can help the index break above 26,200 and move toward 26,300 on a short covering, while a weak or cautious outcome may drag it below 25,900, opening room for 25,750 or lower.', 'url': 'https://www.ndtvprofit.com/markets/trade-setup-nse-nifty-50-bank-support-resistance-levels-outlook-december-5-2025', 'author': 'Prajwal Jayaraj', 'image': 'https://media.assettype.com/bloombergquint%2F2025-08-04%2Fgjuynl2y%2Fdesk-table-with-laptop-smarthone-and-business-pape-2024-09-16-20-14-24-utc.jpg?w=1200&auto=format%2Ccompress&ogImage=true', 'language': 'en', 'category': ['general', 'business'], 'published': '2025-12-04 15:21:59 +0000'},
    {'id': 'e3d38147-30ef-4391-8c1e-497f801ef37c', 'title': "Brian Cole named as Virginia 'anarchist' accused of planting pipe bombs outside US Capitol on eve of January 6 riots", 'description': 'text/plain...', 'url': 'https://www.dailymail.co.uk/news/article-15353107/January-6-pipe-bombing-suspect-arrested-FBI-Capitol.html?ns_mchannel=rss', 'author': 'Editor', 'image': 'None', 'language': 'en', 'category': ['national'], 'published': '2025-12-04 15:18:36 +0000'},
    {'id': '2a68d55a-3ac7-4fd8-bc89-211834ca042f', 'title': "Travis Kelce trespasser learns punishment for trying to serve Taylor Swift legal papers over Blake Lively and Justin Baldoni's feud", 'description': 'text/plain...', 'url': 'https://www.dailymail.co.uk/sport/nfl/article-15353031/Travis-Kelce-trespasser-punishment-Taylor-Swift-Blake-Lively-Justin-Baldoni.html?ns_mchannel=rss', 'author': 'Editor', 'image': 'None', 'language': 'en', 'category': ['national'], 'published': '2025-12-04 15:16:09 +0000'},
    {'id': 'c267cea1-75cf-487e-b7fe-443f5c5ec09f', 'title': 'England warns people to stop visiting ER for ingrown toenails and hiccups', 'description': 'Emergency rooms are "under siege" from patients with minor ailments, England\'s National Health Service said, ahead of a busy flu season and a doctors\' strike.', 'url': 'https://www.washingtonpost.com/world/2025/12/04/emergency-room-nhs-england/', 'author': 'Victoria Craw', 'image': 'None', 'language': 'en', 'category': ['world'], 'published': '2025-12-04 14:49:57 +0000'}
    ]

def get_recent_news():
    url = (f'https://api.currentsapi.services/v1/latest-news?language=en&apiKey={token}')
    response = requests.get(url)
    data = response.json()

    news_list = data.get("news", [])
    global news
    news = news_list
    
    print(len(news))

def news_for_user(user_id):
    usernews = []
    preferred_categories = userbase.get_preferred_categories(user_id)
    print(preferred_categories)
    if not preferred_categories:
        usernews = random.sample(news, 4)
    
    # for item in news:
    #     print(item.get("category"))

    for category in preferred_categories:
        
        filtered_news = [item for item in news if category in item.get("category")]
        if len(filtered_news) == 0:
            print(f"no news about {category}")
            usernews.append(random.choice(news))
            continue

        usernews.append(filtered_news[0])
    usernews.append(random.choice(news))

    newsmessage = ""

    for new in usernews:
        nm = ""
        nm += f"{new.get('title')}\n"
        nm += f"{new.get('url')}\n\n"
        newsmessage += nm

    return newsmessage

if __name__ == "__main__":
    #get_recent_news()
    news_for_user(6183807289)



