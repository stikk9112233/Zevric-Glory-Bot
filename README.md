# Telegram Bot (Zevric-Glory-Bot scaffold)

This repository contains a simple Telegram bot scaffold using python-telegram-bot v20.

Features:
- /start (registers chat for broadcasts)
- /help
- /status
- /broadcast <message> (admin-only)
- Echo for normal text messages
- Simple subscriber storage in data/subscribers.txt

Setup (local):
1. Copy `.env.example` to `.env` and set `TELEGRAM_TOKEN` and `ADMIN_IDS`.
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
- Heroku: `Procfile` is included. Add TELEGRAM_TOKEN and ADMIN_IDS to Heroku config vars.
- GitHub Actions / VPS: set env vars in your server or CI.

Add to your repo:
- Create a new branch (recommended): feature/telegram-bot
- Add the files and open a Pull Request.

Security:
- Never commit `.env` with real tokens. Use secrets in CI/deployment.

If you want, I can try to push these files into your repository directly — grant repo write access (add collaborator or make repo accessible) and tell me the branch name you'd like (recommended: feature/telegram-bot).
