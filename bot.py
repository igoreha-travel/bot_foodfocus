import os
import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = "eda.jpg"
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f"Здравствуйте, {user_name}!\n\nБольшое спасибо, что Вы помогаете мне со сбором данных для моего алгоритма, который будет определять по фотографии пищевую ценность и стоимость комплексного обеда в столовой МГТУ им. Н.Э. Баумана! Пожалуйста, сфотографируйте поднос с едой, как показано на примере, и отправьте фотографию чат-боту.\n\nПриятного аппетита!")
    await update.message.reply_photo(photo=open(photo_path, 'rb'))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = os.path.join(PHOTO_DIR, f"{photo.file_unique_id}.jpg")
    await file.download_to_drive(file_path)
    await update.message.reply_text("Фото сохранено! Спасибо большое за помощь! Очень жду от Вас следующих фотографий!")


async def run_bot():
    app = ApplicationBuilder().token("7520294945:AAFKyMgsEdrNfxgplvLI5raE6H9tgCl8Vs8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
