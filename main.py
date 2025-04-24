from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = FastAPI()
bot = Bot("8174450246:AAE7XXZTLXrD4B41d-OQSv4LOd_18Gk_520")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник YUJIN. Напиши /аналіз <текст>, і я допоможу.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Введи запит після команди. Наприклад: /аналіз Що робити з Ретровіль?")
        return
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response.choices[0].message.content.strip())

@app.on_event("startup")
async def startup():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("аналіз", analyze))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
