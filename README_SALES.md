# README additions for sales

Add config:
- UPI ID shown to buyers: zervicxplay@okhdfcbank
- TRON address for USDT (TRC20): TLwAWcJ7Tm34jqyYqV6qhizQHy8pe7US1v

Commands (user):
- /buy <qty> — create an order and receive payment instructions
- /paid <method> <txid_or_utr> — report payment (method: upi|tron)
- /verify_tron <order_id> <txid> — attempt automated verification for TRON tx

Commands (admin):
- /orders — list orders
- /approve <order_id> — approve and provision
- /reject <order_id> — reject order
- /setprice <amount> — set per-bot price in ₹

Payment flow:
- Users pay UPI manually and report UTR; admin verifies and approves.
- For TRON, users can provide TXID. The bot can attempt auto-verification using public Tron APIs; if successful the order is auto-approved.

