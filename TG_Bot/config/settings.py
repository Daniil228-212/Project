import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Не указан BOT_TOKEN в .env файле")
admin_ids_str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(id_str) for id_str in admin_ids_str.split(",") if id_str.strip()]
PARSE_TIMEOUT = int(os.getenv("PARSE_TIMEOUT", "30"))