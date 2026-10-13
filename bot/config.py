"""Carga de variables de entorno para el bot Hermes.

Requiere python-dotenv. Lee el archivo `.env` (ver `.env.example`).
"""

import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Temas de interés separados por coma
NEWS_TOPICS = [
    t.strip()
    for t in os.getenv("NEWS_TOPICS", "tecnología, ciberseguridad, cloud").split(",")
    if t.strip()
]

# Máximo de noticias a incluir en el briefing
try:
    MAX_NEWS = int(os.getenv("MAX_NEWS", "5"))
except ValueError:
    MAX_NEWS = 5


def validar() -> list[str]:
    """Devuelve una lista de errores de configuración (vacía si todo está bien)."""
    errores = []
    if not TELEGRAM_BOT_TOKEN:
        errores.append("Falta TELEGRAM_BOT_TOKEN (créalo con @BotFather).")
    if not TELEGRAM_CHAT_ID:
        errores.append(
            "Falta TELEGRAM_CHAT_ID (obtenlo con @userinfobot en Telegram)."
        )
    return errores
