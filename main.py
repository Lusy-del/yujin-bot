from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

openai.api_key = 'YOUR_OPENAI_API_KEY'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник YUJIN. Напиши /analysis <текст>, і я допоможу.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Введи запит після команди. Наприклад: /analysis Що робити з Ретровіль?")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response['choices'][0]['message']['content'])

app = ApplicationBuilder().token(8174450246:AAE7XXZTLXrD4B41d-OQSv4LOd_18Gk_520.build
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analysis", analyze))
app.run_polling()
