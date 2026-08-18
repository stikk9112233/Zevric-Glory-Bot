# Telegram Bot (Zevric-Glory-Bot)

This branch adds the ported features from LuckDucapa/Glory-Bot and config to run the Telegram bot.

IMPORTANT SECURITY NOTE
- Do NOT commit your real bot token into the repository. Treat it as a secret.
- The token you posted in chat is exposed now; please rotate the token in BotFather immediately and do not reuse it.

ENVIRONMENT
- Create a `.env` file (not committed) or set environment variables on your server:
  TELEGRAM_TOKEN=your_real_token
  ADMIN_IDS=8981733976

Running 24/7 (recommended options)
1) VPS / Server with Docker (recommended):
   - Build locally or on server:
     docker build -t zevric-bot .
   - Run with env file:
     docker run -d --restart unless-stopped --env-file .env zevric-bot
   - This keeps the container running 24/7; use a VPS (DigitalOcean, Vultr, AWS EC2, etc.)

2) Heroku (if you have an app):
   - Set TELEGRAM_TOKEN and ADMIN_IDS in Heroku Config Vars (do NOT commit to repo).
   - Push the repo to Heroku or connect GitHub and enable automatic deploys.
   - Heroku worker will run `python bot/main.py` (Procfile provided).

3) Railway / Render / Fly / Docker-based platforms:
   - Use the Dockerfile and set environment variables in the platform's secret/config UI.

Automatic deployment via GitHub Actions
- I can add a workflow to build and push a Docker image to a registry or deploy to a platform, but you must add the registry / platform secrets (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, HEROKU_API_KEY, etc.) in GitHub repository Secrets. I cannot add secrets for you.

What I changed
- bot/main.py now loads environment variables from `.env` using python-dotenv.
- README updated with 24/7 deployment options and security guidance.

Next steps I can take for you (pick one)
- A) Create a GitHub Actions workflow that builds the Docker image and pushes to Docker Hub (you must add Docker Hub creds to repo secrets). Then you can run the container on any host.
- B) Create a workflow that deploys to Heroku (you must add HEROKU_API_KEY to secrets).
- C) Set up a systemd unit file and instructions to run the Docker container on a VPS (I can provide the file and commands).

Tell me which of A/B/C you want and I will create the workflow/files on branch `feature/port-glory-main` and open a PR. If you want me to use the token you posted, I will NOT commit it; instead tell me where you will store it (Heroku config / VPS env / GitHub secret) and I'll wire the deployment to read it from secrets.
