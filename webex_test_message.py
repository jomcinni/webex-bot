import os
import requests
from flask import Flask, request
import feedparser

# Replace these with your actual values
WEBEX_BOT_TOKEN = os.environ"NTM1YjBlZjAtMTM4Ny00OThiLTk4ZTctMzJjZTBjYWNjMGZiOTg1ZjAzNGMtNTQ1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
ROOM_ID = os.environ"Y2lzY29zcGFyazovL3VzL1JPT00vNzY1YTllMjAtNTZjZC0xMWYwLThlYTQtMDc4NDI3Y2RhNzYz"
RSS_URL = os.environ"https://news.google.com/rss/search?q=Customer+Success+Artificial+Intelligence&hl=en-US&gl=US&ceid=US:en"

# File to keep track of posted URLs for the current day
today = datetime.now().strftime("%Y-%m-%d")
posted_file = f"/Users/jomcinni/Desktop/posted_news_{today}.txt"

# Load already posted URLs
if os.path.exists(posted_file):
    with open(posted_file, "r") as f:
        posted_urls = set(line.strip() for line in f)
else:
    posted_urls = set()

# Fetch and parse the RSS feed
feed = feedparser.parse(RSS_URL)
fresh_items = [item for item in feed.entries if item.link not in posted_urls]
top_items = fresh_items[:3]  # Get up to 3 new news items

if not top_items:
    message = "No new news found for Customer Success and Artificial Intelligence."
else:
    message = "📰 *Fresh AI in Customer Success News:*\n"
    for item in top_items:
        message += f"- [{item.title}]({item.link})\n"
        posted_urls.add(item.link)

    # Save the new posted URLs
    with open(posted_file, "w") as f:
        for url in posted_urls:
            f.write(url + "\n")

url = "https://webexapis.com/v1/messages"
headers = {
    "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "roomId": ROOM_ID,
    "markdown": message
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    print("News posted successfully!")
else:
    print(f"Failed to post news: {response.status_code} {response.text}")
