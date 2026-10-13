# 📔 Development Log — Briefing Diario en Telegram (Hermes)

## 2026-10-13 — Fase 1: plantilla inicial

### Estado inicial

El repositorio solo contenía un `README.md` de 229 bytes con una frase describiendo la idea: un bot que cada mañana busca noticias relevantes, las resume y las envía a Telegram ("Hermes"). No había código, ni configuración, ni licencia.

### Qué se añadió y por qué

| Archivo | Por qué |
|---|---|
| `README.md` (ampliado) | Documentación profesional: qué hace, arquitectura (Orquestador Hermes → fuente de noticias → resumen LLM → Telegram), stack, instalación paso a paso, variables `.env`, uso manual y por cron, estructura, roadmap y nota de estado honesta. |
| `bot/config.py` | Carga centralizada de variables de entorno con `python-dotenv` y validación básica (token y chat ID obligatorios). |
| `bot/hermes.py` | El orquestador: busca noticias en feeds RSS con `feedparser` (fuente por defecto sin clave), resume con OpenAI si hay `OPENAI_API_KEY` y con fallback local (truncamiento) si no, y envía el briefing a Telegram vía Bot API con `requests`. |
| `bot/main.py` | Punto de entrada: modo bot (`/briefing`, `/start` con polling) y modo `--now` para generar y enviar un briefing inmediato (útil para cron). |
| `requirements.txt` | Dependencias mínimas: python-telegram-bot, openai, feedparser, python-dotenv, requests. |
| `.env.example` | Plantilla de todas las variables necesarias con comentarios. |
| `.gitignore` | Ignora `.env` (claves), `__pycache__`, venvs, logs y artefactos comunes de Python. |
| `LICENSE` | Licencia MIT a nombre de Fermín Gonzalez. |

### Decisiones de diseño

- **RSS como fuente por defecto**: no requiere API key, es suficiente para la fase 1 y permite probar el flujo completo sin costes. NewsAPI/SerpAPI quedan para la fase 2.
- **Fallback sin LLM**: el briefing nunca debe fallar por la API de OpenAI; si no hay clave o falla la llamada, se trunca el texto y se avisa por consola.
- **Envío por `requests` + Bot API**: evita complicar el flujo programático con la API asíncrona de `python-telegram-bot`; la librería se usa para el modo polling interactivo.

### Cómo ejecutarlo

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # completa TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID
python -m bot.main --now   # briefing inmediato
python -m bot.main         # modo bot interactivo (/briefing)
```

Verificación hecha: cada archivo `.py` compiló sin errores con `python3 -m py_compile`.

### ⚠️ Nota honesta

Esta es una **plantilla inicial funcional**. El código está escrito y compila, pero **no se ha probado end-to-end contra la API real de Telegram ni contra OpenAI** (requiere claves propias). El flujo está diseñado para funcionar una vez configures tus claves en `.env`.

### Pendiente — Fase 2

- [ ] Programación nativa del envío diario dentro del propio bot (sin depender del cron del SO).
- [ ] Fuentes adicionales: NewsAPI, SerpAPI, filtros por `NEWS_TOPICS`.
- [ ] Filtrado por relevancia con LLM y deduplicación de titulares.
- [ ] Formato enriquecido en Telegram (HTML/MarkdownV2, botones inline).
- [ ] Tests unitarios (búsqueda, resumen fallback, composición del briefing).
- [ ] Contenedor Docker y despliegue (por ejemplo, en un plan gratuito de Azure/Fly.io).
