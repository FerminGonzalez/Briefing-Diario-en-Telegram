"""Punto de entrada del bot de Telegram — Hermes.

Uso:
    python -m bot.main          # Arranca el bot (responde a /briefing)
    python -m bot.main --now    # Genera y envía un briefing inmediato y sale
"""

from __future__ import annotations

import sys

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot import config, hermes


async def comando_briefing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde al comando /briefing con el resumen del momento."""
    await update.message.reply_text("🕰 Hermes está buscando noticias…")
    briefing = hermes.generar_briefing()
    await update.message.reply_text(briefing, parse_mode="Markdown")


async def comando_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Saludo al comando /start."""
    await update.message.reply_text(
        "¡Hola! Soy Hermes 🕰. Envíame /briefing y te traigo las noticias del momento."
    )


def main() -> None:
    errores = config.validar()
    if errores:
        print("Configuración incompleta:")
        for error in errores:
            print(f"  - {error}")
        print("\nCopia .env.example a .env y completa tus valores. Mira el README.md.")
        sys.exit(1)

    # Modo inmediato: genera un briefing y sale (ideal para cron)
    if "--now" in sys.argv:
        briefing = hermes.ejecutar()
        print(briefing)
        return

    # Modo bot: queda escuchando comandos en Telegram
    aplicacion = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    aplicacion.add_handler(CommandHandler("start", comando_inicio))
    aplicacion.add_handler(CommandHandler("briefing", comando_briefing))
    print("Hermes está escuchando… envía /briefing en Telegram.")
    aplicacion.run_polling()


if __name__ == "__main__":
    main()
