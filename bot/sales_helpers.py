from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sales
import logging

logger = logging.getLogger(__name__)

# Helper decorators / functions to be used in the telegram_bridge handlers

async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text("Usage: /buy <qty> — Example: /buy 1")
        return
    try:
        qty = int(context.args[0])
        if qty <= 0:
            raise ValueError()
    except Exception:
        await update.message.reply_text("Invalid quantity. Use a positive integer.")
        return

    # Payment options: UPI or TRON
    order_id = sales.create_order(user.id, qty, "upi", "zervicxplay@okhdfcbank")
    total = qty * sales.PER_BOT_PRICE

    text = f"🛒 Order ID: {order_id}\n\n" \
           f"👤 User: {user.first_name or user.username}\n" \
           f"🧩 Quantity: {qty} bot(s)\n" \
           f"💰 Total: ₹{total}\n\n" \
           "📌 Payment options:\n" \
           f"1️⃣ UPI: zervicxplay@okhdfcbank (Scan or use UPI app)\n" \
           f"2️⃣ TRON (USDT - TRC20): TLwAWcJ7Tm34jqyYqV6qhizQHy8pe7US1v\n\n" \
           "After payment, reply with: /paid <method> <txn_id_or_UTR> and attach screenshot if UPI.\n" \
           "Example: /paid upi 123456789012 or /paid tron TXID123...\n\n" \
           "Admin will verify and approve. For TRON payments you can also provide TXID for auto-check."

    keyboard = [[InlineKeyboardButton("I paid (report)", callback_data=f"report:{order_id}")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /paid <upi|tron> <txid_or_utr>")
        return
    method = context.args[0].lower()
    proof = context.args[1]
    # If message has photo, we can save file_id as additional proof — but we'll keep proof text
    # Find last pending order for user
    orders = sales.list_orders()
    user_orders = [o for o in orders if o["user_id"] == user.id and o["status"] == "pending"]
    if not user_orders:
        # Try awaiting_admin too
        user_orders = [o for o in orders if o["user_id"] == user.id and o["status"] in ("pending","awaiting_admin")]
    if not user_orders:
        await update.message.reply_text("No pending orders found. Create an order with /buy <qty>")
        return
    # choose most recent
    target = user_orders[0]
    order_id = target["id"]
    added = sales.add_proof(order_id, f"{method}:{proof}")
    if not added:
        await update.message.reply_text("Failed to record proof, try again or contact admin @just_zevric")
        return

    # notify user
    await update.message.reply_text(f"Thanks — proof recorded for order {order_id}. Admin will verify soon. If you paid via TRON you can run /verify_tron {order_id} <txid> to attempt auto-verify.")

    # notify admin(s) — we rely on ADMIN_IDS env and telegram_bridge to route notifications by reading orders table


async def handle_verify_tron(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /verify_tron <order_id> <txid>")
        return
    order_id = context.args[0]
    txid = context.args[1]
    order = sales.get_order(order_id)
    if not order:
        await update.message.reply_text("Order not found.")
        return
    # verify via Tronscan
    await update.message.reply_text(f"Verifying TX {txid} for order {order_id} — please wait...")
    ok = sales.verify_tron_tx(txid, order["address"], order["total"])  # heuristic
    if ok:
        # mark proof and auto-approve
        sales.add_proof(order_id, f"tron:{txid}")
        sales.admin_approve(order_id)
        await update.message.reply_text(f"✅ Payment verified and order {order_id} approved. Admin will finalize adding bots shortly.")
    else:
        await update.message.reply_text("Could not verify the transaction automatically. Admin will check manually.")


# Admin helper functions — these will be registered as handlers in telegram_bridge
async def admin_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = sales.list_orders()
    if not orders:
        await update.message.reply_text("No orders yet.")
        return
    text_lines = []
    for o in orders[:20]:
        text_lines.append(f"ID:{o['id']} | User:{o['user_id']} | Qty:{o['qty']} | ₹{o['total']} | Method:{o['method']} | Status:{o['status']}")
    await update.message.reply_text("\n".join(text_lines))


async def admin_approve_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /approve <order_id>")
        return
    order_id = context.args[0]
    ok = sales.admin_approve(order_id)
    if ok:
        await update.message.reply_text(f"Order {order_id} approved.")
        # Attempt to call glory_main hook if exists
        try:
            import main as glory_main
            order = sales.get_order(order_id)
            if hasattr(glory_main, "process_purchase"):
                glory_main.process_purchase(order)
        except Exception as e:
            logger.info("No glory hook or failed to call: %s", e)
    else:
        await update.message.reply_text("Failed to approve (order not found).")


async def admin_reject_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /reject <order_id>")
        return
    order_id = context.args[0]
    reason = "".join(context.args[1:]) or "rejected"
    ok = sales.admin_reject(order_id, reason)
    if ok:
        await update.message.reply_text(f"Order {order_id} rejected.")
    else:
        await update.message.reply_text("Failed to reject (order not found).")


async def set_price_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setprice <amount> — per bot price in ₹")
        return
    try:
        amount = int(context.args[0])
        sales.PER_BOT_PRICE = amount
        await update.message.reply_text(f"Per-bot price set to ₹{amount}")
    except Exception:
        await update.message.reply_text("Invalid amount")
