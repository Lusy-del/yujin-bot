import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Отримуємо токен з середовища
bot_token = os.environ.get("BOT_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник YUJIN. Напиши /аналіз <текст>, і я допоможу.")

# Команда /аналіз
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Введи запит після команди. Наприклад: /аналіз Що робити з Ретровіль?")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response.choices[0].message.content.strip())

# Ініціалізація бота
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("аналіз", analyze))
app.run_polling()
