from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

openai.api_key = 'sk-abc123xyz456...'  # <-- встав сюди ключ з OpenAI

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник YUJIN. Напиши /analysis <текст>, і я допоможу.")

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Введи запит після команди. Наприклад: /analysis Що робити з KPI?")
        return

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    await update.message.reply_text(response.choices[0].text.strip())

app = ApplicationBuilder().token("8174450246:AAE7XXZTLXrD4B41d-OQSv4LOd_18Gk_520").build()  # <-- встав токен з BotFather
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analysis", analyze))
app.run_polling()
