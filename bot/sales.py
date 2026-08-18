import sqlite3
import uuid
import time
from datetime import datetime
from typing import Optional, List, Dict
import threading
import requests

DB_PATH = "data/orders.sqlite"

# Default pricing
PER_BOT_PRICE = 50  # ₹ per bot

TRON_API_TX_URL = "https://apilist.tronscan.org/api/transaction"  # simple public endpoint


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            qty INTEGER,
            total INTEGER,
            method TEXT,
            address TEXT,
            status TEXT,
            proof TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def create_order(user_id: int, qty: int, method: str, address: str) -> str:
    order_id = str(uuid.uuid4())[:8]
    total = qty * PER_BOT_PRICE
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (id, user_id, qty, total, method, address, status, proof, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (order_id, user_id, qty, total, method, address, "pending", "", now, now),
    )
    conn.commit()
    conn.close()
    return order_id


def get_order(order_id: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,user_id,qty,total,method,address,status,proof,created_at,updated_at FROM orders WHERE id=?", (order_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    keys = ["id", "user_id", "qty", "total", "method", "address", "status", "proof", "created_at", "updated_at"]
    return dict(zip(keys, row))


def list_orders(status: Optional[str] = None) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT id,user_id,qty,total,method,address,status,proof,created_at,updated_at FROM orders WHERE status=? ORDER BY created_at DESC", (status,))
    else:
        c.execute("SELECT id,user_id,qty,total,method,address,status,proof,created_at,updated_at FROM orders ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    keys = ["id", "user_id", "qty", "total", "method", "address", "status", "proof", "created_at", "updated_at"]
    return [dict(zip(keys, r)) for r in rows]


def add_proof(order_id: str, proof: str) -> bool:
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE orders SET proof=?, status=?, updated_at=? WHERE id=?", (proof, "awaiting_admin", now, order_id))
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def admin_approve(order_id: str) -> bool:
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE orders SET status=?, updated_at=? WHERE id=?", ("approved", now, order_id))
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def admin_reject(order_id: str, reason: str = "rejected") -> bool:
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE orders SET status=?, proof=?, updated_at=? WHERE id=?", ("rejected", reason, now, order_id))
    changed = c.rowcount
    conn.commit()
    conn.close()
    return changed > 0


def verify_tron_tx(txid: str, expected_address: str, expected_amount: int) -> bool:
    # Query Tronscan transaction API for txid and validate
    try:
        resp = requests.get(f"https://apilist.tronscan.org/api/transaction-info?hash={txid}", timeout=10)
        if resp.status_code != 200:
            return False
        data = resp.json()
        # data may contain 'ret' and 'raw_data' etc. For token transfers, check token_info
        # We'll try simple heuristics: receiver address or token transfer list.
        # Convert expected_amount INR to USDT/tron decimals is out of scope; expect user submits tx of exact amount in TRC20 (in smallest unit)
        # For safety, we only check that the tx contains transfer to expected_address in 'to' or events
        to_addr = data.get("to") or data.get("raw_data", {}).get("contract", [{}])[0].get("parameter", {}).get("value", {}).get("to_address")
        if not to_addr:
            # try parsing token transfers
            return False
        # Tronscan returns base58 addresses; we compare case-insensitive
        if expected_address.lower() in str(to_addr).lower():
            return True
    except Exception:
        return False
    return False


# Initialize DB on import
init_db()


# Background worker (optional): simple poll to check pending TRON orders if you want auto-detection
# For reliability we provide /verify_tron command which admins or users can call with TXID

