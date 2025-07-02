import os
import requests
from flask import Flask, request
import feedparser

# Get secrets from environment variables (set in Render dashboard)
WEBEX_BOT_TOKEN = os.environ["WEBEX_BOT_TOKEN"]
ROOM_ID = os.environ["ROOM_ID"]
BOT_EMAIL = os.environ["BOT_EMAIL"]

app = Flask(__name__)

def summarize_article(article_text):
    # Placeholder: just return the first 200 characters for now
    return article_text[:200] + "..." if len(article_text) > 200 else article_text

def get_news(topic="Customer Success Artificial Intelligence"):
    rss_url = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    top_items = feed.entries[:3]
    if not top_items:
        return f"No news found for '{topic}'."
    message = f"📰 *Top news for '{topic}':*\n"
    for item in top_items:
        # Use item.summary if available, otherwise item.title
        article_text = getattr(item, "summary", item.title)
        summary = summarize_article(article_text)
        message += f"- [{item.title}]({item.link})\n  _Summary_: {summary}\n"
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

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Ignore messages from the bot itself
    if data["data"]["personEmail"] == BOT_EMAIL:
        return "OK"
    room_id = data["data"]["roomId"]
    message_id = data["data"]["id"]

    # Get the message text
    msg_url = f"https://webexapis.com/v1/messages/{message_id}"
    headers = {"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"}
    msg_data = requests.get(msg_url, headers=headers).json()
    text = msg_data.get("text", "").strip().lower()
    print(f"Received message: '{text}'")  # For debugging

    # Improved prompt matching
    if text.startswith("news about"):
        topic = text[len("news about"):].strip(" :")
        reply = get_news(topic if topic else "Customer Success Artificial Intelligence")
    elif text.strip(" .!?") == "news":
        reply = get_news()
    else:
        reply = "Hi! Type `news` for general AI Customer Success news, or `news about <topic>` for something specific."

    send_message(room_id, reply)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
