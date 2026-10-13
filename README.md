# 📬 Briefing Diario en Telegram — "Hermes"

Cada mañana, antes de que te des cuenta, **Hermes** busca las noticias más relevantes sobre los temas que te interesan, las resume con IA y te las envía a **Telegram** como un mensaje limpio y directo.

> **⚠️ Estado:** plantilla inicial funcional — requiere configurar tus propias claves de API para funcionar. Ver [DEVELOPMENT-LOG.md](DEVELOPMENT-LOG.md) para el detalle de lo que falta (fase 2).

## 🧠 Cómo funciona

```
┌──────────────────┐      ┌─────────────────────┐      ┌────────────────────┐      ┌───────────────┐
│  Comando / o     │ ───▶ │  Orquestador Hermes │ ───▶ │  Resumen con LLM   │ ───▶ │   Mensaje a   │
│  cron programado │      │  (busca noticias)   │      │  (OpenAI o fallback)│     │   Telegram    │
└──────────────────┘      └─────────┬───────────┘      └────────────────────┘      └───────────────┘
                                    │
                        ┌───────────▼───────────┐
                        │  Fuente de noticias   │
                        │  RSS vía feedparser   │
                        │  (sin clave requerida)│
                        └───────────────────────┘
```

1. **Orquestador Hermes** (`bot/hermes.py`): coordina el flujo completo.
2. **Fuente de noticias**: por defecto lee feeds RSS con `feedparser` (no requiere API key). El código deja el enganche para añadir NewsAPI o SerpAPI en la fase 2.
3. **Resumen con LLM**: si `OPENAI_API_KEY` está definida, resume cada noticia con un modelo OpenAI. Si no, usa un *fallback* local que trunca el texto a un máximo de caracteres.
4. **Mensaje a Telegram**: envía el briefing con `python-telegram-bot`.

## 🛠 Stack

- **Python** 3.11+
- [python-telegram-bot](https://python-telegram-bot.org/) — bot de Telegram
- [openai](https://github.com/openai/openai-python) — resumen con LLM (opcional)
- [feedparser](https://github.com/kurtmckee/feedparser) — lectura de feeds RSS
- [python-dotenv](https://github.com/theskumar/python-dotenv) — carga de variables `.env`
- Opcionales (fase 2): NewsAPI, SerpAPI

## 📋 Requisitos

- Python 3.11 o superior
- Un bot de Telegram (créalo con [@BotFather](https://t.me/BotFather) y copia el token)
- El **chat ID** donde quieres recibir el briefing (puedes obtenerlo hablando con [@userinfobot](https://t.me/userinfobot))
- (Opcional) Una clave de API de OpenAI para resúmenes con IA

## 🚀 Instalación paso a paso

```bash
# 1. Clonar el repositorio
git clone https://github.com/FerminGonzalez/Briefing-Diario-en-Telegram.git
cd Briefing-Diario-en-Telegram

# 2. Crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env y coloca tus valores reales
```

## ⚙️ Variables de entorno (`.env`)

| Variable | Obligatoria | Descripción |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | Token que te dio @BotFather |
| `TELEGRAM_CHAT_ID` | ✅ | Chat ID donde se envía el briefing |
| `OPENAI_API_KEY` | ❌ | Clave de OpenAI; si falta se usa el resumen por truncamiento |
| `OPENAI_MODEL` | ❌ | Modelo a usar (por defecto: `gpt-4o-mini`) |
| `NEWS_TOPICS` | ❌ | Temas separados por coma (ej: `tecnología, cloud, ciberseguridad`) |
| `MAX_NEWS` | ❌ | Máximo de noticias a incluir (por defecto: `5`) |

## ▶️ Uso

### Manual

```bash
python -m bot.main
```

Esto arranca el bot. En Telegram, envía `/briefing` a tu bot para recibir el resumen del momento. También puedes generar un briefing directamente desde la terminal con:

```bash
python -m bot.main --now
```

### Automático (cron)

Para recibirlo cada mañana sin hacer nada, agrega una entrada en `crontab -e`:

```bash
# Briefing de Hermes todos los días a las 07:30
30 7 * * * cd /ruta/a/Briefing-Diario-en-Telegram && /ruta/a/venv/bin/python -m bot.main --now >> hermes.log 2>&1
```

## 📁 Estructura del proyecto

```
Briefing-Diario-en-Telegram/
├── bot/
│   ├── __init__.py
│   ├── main.py        # Punto de entrada del bot de Telegram
│   ├── hermes.py      # Orquestador: busca → resume → envía
│   └── config.py      # Carga de variables de entorno
├── .env.example       # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
├── DEVELOPMENT-LOG.md # Registro de desarrollo
├── LICENSE            # MIT
└── README.md
```

## 🗺 Roadmap

- **Fase 1 (actual)** ✅ — Esqueleto funcional: bot de Telegram, búsqueda por RSS, resumen con OpenAI (o fallback), envío de mensaje, configuración por `.env`.
- **Fase 2** — Programación nativa del envío diario (dentro del bot), fuentes adicionales (NewsAPI, SerpAPI), filtrado por relevancia con LLM y deduplicación.
- **Fase 3** — Formato enriquecido (Markdown/HTML con botones), estadísticas de lectura y modo "solo titulares".

## 📄 Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).

## ✍️ Autor

**Fermín Gonzalez** — [github.com/FerminGonzalez](https://github.com/FerminGonzalez)
