# Webex AI News Bot

This project provides:
- **Scheduled news posts** (8am and 5pm Central) to a Webex space using GitHub Actions
- **Interactive news requests** via a Webex bot (hosted on Render) for AI and Customer Success topics

## Features

- **Scheduled Posting:** Top 3 AI/Customer Success news stories posted automatically to your Webex space at 8am and 5pm.
- **Interactive Bot:** Ask the bot for `news` or `news about <topic>` in a 1:1 Webex space and get relevant headlines.

## Setup

### 1. Scheduled News Posting (GitHub Actions)
- `scheduled_news_post.py` posts news to your Webex space.
- `.github/workflows/scheduled-news.yml` runs the script at scheduled times.
- Secrets required: `WEBEX_BOT_TOKEN`, `ROOM_ID` (set in GitHub repo settings).

### 2. Interactive Bot (Render)
- `webex_interactive_bot.py` is deployed to Render.
- Environment variables required: `WEBEX_BOT_TOKEN`, `ROOM_ID`, `BOT_EMAIL` (set in Render dashboard).
- Webhook registered with Webex to point to your Render URL.

## Restore or Re-Deploy

1. Clone the repo:
   ```
   git clone https://github.com/jomcinni/webex-bot.git
   ```
2. Set up secrets/environment variables as above.
3. Deploy to Render for the interactive bot.
4. GitHub Actions will handle scheduled posts automatically.

## Contact

For help, revisit your original chat with the AI assistant or check this README.