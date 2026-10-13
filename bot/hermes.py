"""Orquestador Hermes: busca noticias, las resume y las envía a Telegram.

Flujo:
1. Busca noticias en feeds RSS (feedparser, sin clave requerida).
2. Resume cada noticia con OpenAI si OPENAI_API_KEY está definida;
   si no, usa un fallback que trunca el texto.
3. Compone el briefing y lo devuelve como texto listo para Telegram.
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass

import feedparser

from bot import config

# Feeds RSS por defecto. Puedes agregar más URLs según tus temas.
FEEDS_RSS = [
    "https://hnrss.org/frontpage",
    "https://www.xataka.com/rss",
    "https://feeds.arstechnica.com/arstechnica/technology-lab",
]

# Longitud máxima del resumen de fallback (sin LLM)
FALLBACK_MAX_CARACTERES = 280


@dataclass
class Noticia:
    titulo: str
    enlace: str
    resumen: str


def buscar_noticias(max_noticias: int | None = None) -> list[Noticia]:
    """Lee los feeds RSS configurados y devuelve las noticias más recientes."""
    limite = max_noticias or config.MAX_NEWS
    noticias: list[Noticia] = []

    for url_feed in FEEDS_RSS:
        feed = feedparser.parse(url_feed)
        for entrada in feed.entries:
            if len(noticias) >= limite:
                break
            titulo = getattr(entrada, "title", "").strip()
            enlace = getattr(entrada, "link", "")
            texto = getattr(entrada, "summary", "") or titulo
            if titulo:
                noticias.append(Noticia(titulo=titulo, enlace=enlace, resumen=texto))
        if len(noticias) >= limite:
            break

    return noticias


def _resumir_con_openai(texto: str) -> str:
    """Resume el texto con la API de OpenAI."""
    from openai import OpenAI

    cliente = OpenAI(api_key=config.OPENAI_API_KEY)
    respuesta = cliente.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres Hermes, un asistente que resume noticias en español. "
                    "Resume el texto en un máximo de 2 frases, claras y directas."
                ),
            },
            {"role": "user", "content": texto},
        ],
        temperature=0.3,
    )
    return respuesta.choices[0].message.content.strip()


def _resumir_fallback(texto: str) -> str:
    """Resumen local sin LLM: trunca el texto plano."""
    limpio = " ".join(texto.split())
    if len(limpio) <= FALLBACK_MAX_CARACTERES:
        return limpio
    return textwrap.shorten(limpio, width=FALLBACK_MAX_CARACTERES, placeholder="…")


def resumir(texto: str) -> str:
    """Resume con OpenAI si hay clave; si no, usa el fallback."""
    if config.OPENAI_API_KEY:
        try:
            return _resumir_con_openai(texto)
        except Exception as exc:  # noqa: BLE001 — el briefing no debe fallar por el LLM
            print(f"[Hermes] Aviso: falló el resumen con OpenAI ({exc}); usando fallback.")
    return _resumir_fallback(texto)


def generar_briefing(max_noticias: int | None = None) -> str:
    """Genera el texto del briefing diario."""
    noticias = buscar_noticias(max_noticias)

    if not noticias:
        return "🕰 **Hermes** — no encontré noticias en este momento. Inténtalo más tarde."

    lineas = ["🕰 **Hermes — Tu briefing diario**", ""]
    for i, noticia in enumerate(noticias, start=1):
        resumen = resumir(noticia.resumen)
        lineas.append(f"**{i}. {noticia.titulo}**")
        lineas.append(resumen)
        if noticia.enlace:
            lineas.append(f"🔗 {noticia.enlace}")
        lineas.append("")

    return "\n".join(lineas).strip()


def enviar_a_telegram(mensaje: str) -> None:
    """Envía el briefing al chat configurado usando la Bot API."""
    import requests

    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        raise RuntimeError("Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el .env")

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    respuesta = requests.post(
        url,
        json={
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": mensaje,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True,
        },
        timeout=30,
    )
    respuesta.raise_for_status()


def ejecutar(max_noticias: int | None = None) -> str:
    """Ejecuta el flujo completo: buscar → resumir → enviar. Devuelve el briefing."""
    briefing = generar_briefing(max_noticias)
    enviar_a_telegram(briefing)
    return briefing
