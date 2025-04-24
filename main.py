import os
import openai
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Отримання токенів з середовища
bot_token = os.environ.get("BOT_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am the YUJIN assistant bot. Use /analiz <your request>.")

# Команда /analiz
async def analiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Please enter your request after the command. Example: /analiz What should I do with Retroville?")
        return

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    await update.message.reply_text(response.choices[0].message.content.strip())

# Ініціалізація бота
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analiz", analiz))

# Асинхронний запуск (працює на Render)
if __name__ == '__main__':
    async def main():
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    asyncio.run(main())
