import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Отримання токенів із змінних середовища
bot_token = "8174450246:AAE7XXZTLXrD4B41d-OQSv4LOd_18Gk_520"
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот-помічник YUJIN. Напиши /analyze <текст>, і я допоможу.")

# Команда /analyze
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text(
            "Введи запит після команди. Наприклад: /analyze Що робити з Ретровіль?")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response.choices[0].message.content.strip())

# Ініціалізація бота
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analyze", analyze))
app.run_polling()
