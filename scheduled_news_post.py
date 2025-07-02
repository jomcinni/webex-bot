import os
import requests
import feedparser

WEBEX_BOT_TOKEN = os.environ["WEBEX_BOT_TOKEN"]
ROOM_ID = os.environ["ROOM_ID"]

def get_news(topic="Customer Success Artificial Intelligence"):
    rss_url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    top_items = feed.entries[:3]
    if not top_items:
        return f"No news found for '{topic}'."
    message = f"📰 *Top news for '{topic}':*\n"
    for item in top_items:
        message += f"- [{item.title}]({item.link})\n"
    return message

def send_message(room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "roomId": room_id,
        "markdown": message
    }
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    message = get_news()
    send_message(ROOM_ID, message)