import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN yo‘q")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID yo‘q")