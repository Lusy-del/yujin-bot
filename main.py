import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# РћС‚СЂРёРјСѓС”РјРѕ С‚РѕРєРµРЅ Р· СЃРµСЂРµРґРѕРІРёС‰Р°
bot_token = "8174450246:AAE7XXZTLXrD4B41d-OQSv4LOd_18Gk_520"
openai.api_key = os.environ.get("OPENAI_API_KEY")

# РљРѕРјР°РЅРґР° /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("РџСЂРёРІС–С‚! РЇ Р±РѕС‚-РїРѕРјС–С‡РЅРёРє YUJIN. РќР°РїРёС€Рё /Р°РЅР°Р»С–Р· <С‚РµРєСЃС‚>, С– СЏ РґРѕРїРѕРјРѕР¶Сѓ.")

# РљРѕРјР°РЅРґР° /Р°РЅР°Р»С–Р·
async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Р’РІРµРґРё Р·Р°РїРёС‚ РїС–СЃР»СЏ РєРѕРјР°РЅРґРё. РќР°РїСЂРёРєР»Р°Рґ: /Р°РЅР°Р»С–Р· Р©Рѕ СЂРѕР±РёС‚Рё Р· Р РµС‚СЂРѕРІС–Р»СЊ?")
        return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    await update.message.reply_text(response.choices[0].message.content.strip())

# Р†РЅС–С†С–Р°Р»С–Р·Р°С†С–СЏ Р±РѕС‚Р°
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("Р°РЅР°Р»С–Р·", analyze))

# РђСЃРёРЅС…СЂРѕРЅРЅРёР№ Р·Р°РїСѓСЃРє
import asyncio

if __name__ == '__main__':
    async def main():
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    asyncio.run(main())
