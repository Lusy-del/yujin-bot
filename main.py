import os
import openai
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher
from telegram.ext import MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # напр. https://your-bot-name.onrender.com/webhook

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TOKEN)
app = FastAPI()
application = ApplicationBuilder().token(TOKEN).build()

# Команди
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот YUJIN.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Введи запит після команди. Напр: /аналіз Що робити з Ретровіль?")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response.choices[0].message.content)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("аналіз", analyze))

# FastAPI endpoint
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def startup():
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")
