# Telegram Bot (Zevric-Glory-Bot scaffold)

This repository contains a simple Telegram bot scaffold using python-telegram-bot v20.

Features:
- /start (registers chat for broadcasts)
- /help
- /status
- /broadcast <message> (admin-only)
- /addbalance (generates UPI/USDT QR payment codes)
- Echo for normal text messages
- Simple subscriber storage in data/subscribers.txt

Setup (local):
1. Copy `.env.example` to `.env` and set `TELEGRAM_TOKEN`, `ADMIN_IDS`, `UPI_ID`, and `USDT_ADDRESS`.
2. Create and activate a virtualenv:
   python -m venv venv
   source venv/bin/activate   # (Windows: venv\\Scripts\\activate)
3. Install:
   pip install -r requirements.txt
4. Run:
   python bot/main.py

Docker:
1. Build: docker build -t zevric-bot .
2. Run: docker run --env-file .env zevric-bot

Deploy:
- Heroku: `Procfile` is included. Add TELEGRAM_TOKEN, ADMIN_IDS, UPI_ID, and USDT_ADDRESS to Heroku config vars.
- GitHub Actions / VPS: set env vars in your server or CI.

Security:
- Never commit `.env` with real tokens. Use secrets in CI/deployment.
