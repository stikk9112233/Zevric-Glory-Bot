import os
import logging
from pathlib import Path
from typing import Set

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Config
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x}
DATA_DIR = Path("data")
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.txt"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SUBSCRIBERS_FILE.exists():
        SUBSCRIBERS_FILE.write_text("")


def read_subscribers() -> Set[int]:
    ensure_data_dir()
    text = SUBSCRIBERS_FILE.read_text().strip()
    if not text:
        return set()
    return {int(line) for line in text.splitlines() if line.strip()}


def add_subscriber(chat_id: int):
    subs = read_subscribers()
    if chat_id in subs:
        return
    subs.add(chat_id)
    SUBSCRIBERS_FILE.write_text("\n".join(str(x) for x in sorted(subs)))


def remove_subscriber(chat_id: int):
    subs = read_subscribers()
    if chat_id in subs:
        subs.remove(chat_id)
        SUBSCRIBERS_FILE.write_text("\n".join(str(x) for x in sorted(subs)))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    add_subscriber(chat_id)
    await update.message.reply_text(
        f"Salam {user.first_name or 'friend'}!\nMain ready hoon. /help likho commands ke liye."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start - Register and start the bot\n"
        "/help - Show this message\n"
        "/status - Bot status\n"
        "/broadcast <message> - (admin only) send message to all registered users\n"
        "Any text message will be echoed back."
    )
    await update.message.reply_text(text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subs = len(read_subscribers())
    await update.message.reply_text(f"Bot is running ✅\nSubscribers: {subs}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None or user.id not in ADMIN_IDS:
        await update.message.reply_text("Yeh command sirf admin ke liye hai.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return

    message = " ".join(context.args)
    subs = read_subscribers()
    if not subs:
        await update.message.reply_text("No subscribers to send to.")
        return

    sent = 0
    failed = 0
    for chat_id in subs:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
            sent += 1
        except Exception as e:
            logger.warning("Failed to send to %s: %s", chat_id, e)
            failed += 1

    await update.message.reply_text(f"Broadcast done. Sent: {sent}, Failed: {failed}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(update.message.text)


def main():
    if TOKEN is None:
        logger.error("TELEGRAM_TOKEN not set. Set environment variable TELEGRAM_TOKEN.")
        return

    ensure_data_dir()

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Echo non-command text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Starting bot (polling)...")
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
