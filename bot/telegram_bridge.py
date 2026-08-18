import os
import logging
from pathlib import Path
from typing import Set
from dotenv import load_dotenv
import threading

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load .env if present
load_dotenv()

# Config
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x}

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot connected. Use /help to see commands. Support: @just_zevric")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - Bot status\n"
        "/help - This message\n"
        "/run <id> <password> - Start FF_CLIENT for given id and password (admin only)\n"
        "/glori <uid> - Trigger in-repo /glori behavior if implemented\n"
        "Support: @just_zevric\n"
        "YouTube: https://youtube.com/@zevricxplay?si=YoV2zn0G6XzI_oKV"
    )
    await update.message.reply_text(text)


async def run_client_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None or user.id not in ADMIN_IDS:
        await update.message.reply_text("Only admin can run this command. Contact @just_zevric for help.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /run <id> <password>")
        return

    uid = context.args[0]
    pwd = context.args[1]

    # Import and call run_client from ported main
    try:
        import main as glory_main
    except Exception as e:
        await update.message.reply_text(f"Error importing main module: {e}")
        return

    try:
        thread = threading.Thread(target=glory_main.run_client, args=(uid, pwd))
        thread.daemon = True
        thread.start()
        await update.message.reply_text(f"Started client for {uid}")
    except Exception as e:
        await update.message.reply_text(f"Failed to start client: {e}")


async def glori_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Proxy command to in-repo functionality if exists
    user = update.effective_user
    if user is None or user.id not in ADMIN_IDS:
        await update.message.reply_text("Only admin can run this command. Contact @just_zevric for help.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Usage: /glori <uid>")
        return

    uid = context.args[0]
    try:
        import main as glory_main
        # Here we attempt to trigger a /glori-like behavior by sending to FF_CLIENT instances
        # This requires the ported main.py to support such invocation. We'll call run_client for now.
        thread = threading.Thread(target=glory_main.run_client, args=(uid, ""))
        thread.daemon = True
        thread.start()
        await update.message.reply_text(f"Triggered glori for {uid}")
    except Exception as e:
        await update.message.reply_text(f"Error triggering glori: {e}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Unknown command. Use /help or contact @just_zevric for support.")


def main():
    if TOKEN is None:
        logger.error("TELEGRAM_TOKEN not set in environment or secrets.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("run", run_client_cmd))
    app.add_handler(CommandHandler("glori", glori_cmd))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Starting Telegram bridge (polling)...")
    app.run_polling()


if __name__ == "__main__":
    main()
