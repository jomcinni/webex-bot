import os
import requests
import feedparser
import json

# Get secrets from environment variables (set as GitHub Actions secrets)
WEBEX_BOT_TOKEN = os.environ["WEBEX_BOT_TOKEN"]
ROOM_ID = os.environ["ROOM_ID"]
CIRCUIT_API_KEY = os.environ["CIRCUIT_API_KEY"]
CIRCUIT_APP_KEY = os.environ["CIRCUIT_APP_KEY"]
def summarize_article(article_text):
    API_URL = "https://chat-ai.cisco.com/openai/deployments/gpt-4o-mini/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "api-key": CIRCUIT_API_KEY
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
            {"role": "user", "content": f"Summarize this article: {article_text}"}
        ],
        "user": json.dumps({"appkey": CIRCUIT_APP_KEY}),
        "stop": ["<|im_end|>"]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"Summarization API error: {response.status_code} {response.text}")
            return "Summary unavailable."
    except Exception as e:
        print(f"Summarization API exception: {e}")
        return "Summary unavailable."
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
    print("Message to send:\n", message)  # Debug print
    response = requests.post(url, headers=headers, json=data)
    print("Webex API response:", response.status_code, response.text)  # Debug print
def get_news(topic="Customer Success Artificial Intelligence"):
    print("Fetching news for topic:", topic)
    RSS_URL = f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(RSS_URL)
    top_items = feed.entries[:3]
    if not top_items:
        return f"No news found for '{topic}'."
    message = f"📰 *Top news for '{topic}':*\n"
    for item in top_items:
        article_text = getattr(item, "summary", item.title)
        summary = summarize_article(article_text)
        message += f"- [{item.title}]({item.link})\n  _Summary_: {summary}\n"
    return message

if __name__ == "__main__":
    print("Starting scheduled news post script...")
    message = get_news()
    send_message(ROOM_ID, message)
