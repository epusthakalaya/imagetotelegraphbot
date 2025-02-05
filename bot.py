import os
import logging
import requests

from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def start_cmd(update, context):
    update.message.reply_text(f"Hello {update.message.from_user.first_name}.\n\nI can upload photos from telegram to telegra.ph 🤫 Now send me a picture.")
    update.message.reply_text="""<b>Hey There, I'm SL IMAGE TO TELEGRAPH BOT. 
I can upload photos or videos to telegraph. Made by @Madushanka_bro 🇱🇰
Hit help button to find out more about how to use me</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "DEVELOPER", url="https://t.me/Madushanka_bro"),
                                        InlineKeyboardButton(
                                            "Channel", url="https://t.me/epusthakalaya_bots")
                                    ]
                            ),        


def upload_cmd(update, context):
    photo = context.bot.get_file(update.message.photo[-1].file_id)
    photo.download(f'{str(update.message.from_user.id)}.jpg')

    files = {'files': open(f'{str(update.message.from_user.id)}.jpg', 'rb')}
    r = requests.post("https://telegra.ph/upload", files=files)
    info = r.json()
    if info[0].get("error"):
        return update.message.reply_text("Failed to upload. Reason: {err}".format(err=info[0].get("error")))

    url = "https://telegra.ph" + info[0].get("src")
    update.message.reply_text(url)
    os.remove(f'{str(update.message.from_user.id)}.jpg')


def upload(update, context):
    size = update.message.document.file_size
    if size > 5242880:
        return update.message.reply_text("File size is greater than 5MB")

    photo = context.bot.get_file(update.message.document.file_id)
    mime = update.message.document.file_name[-3:].lower()
    if mime not in ["jpg", "peg", "png", "gif", "mp4"]:
        return update.message.reply_text("This type of file is not supported by telegra.ph")

    photo.download(f'{str(update.message.from_user.id)}.{update.message.document.file_name.rsplit(".", 1)[-1]}')
    files = {'files': open(f'{str(update.message.from_user.id)}.jpg', 'rb')}
    r = requests.post("https://telegra.ph/upload", files=files)
    data = r.json()
    if data[0].get('error'):
        return update.message.reply_text("Failed to upload. Reason: {err}".format(err=data[0].get("error")))

    url = "https://telegra.ph" + data[0].get("src")
    update.message.reply_text(url)
    os.remove(f'{str(update.message.from_user.id)}.jpg')


def error(update, context):
    logger.error(context.error, exc_info=True)


if __name__ == '__main__':
    updater = Updater(token=os.environ.get("BOT_TOKEN", None), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(MessageHandler(Filters.photo, upload_cmd))
    dp.add_handler(MessageHandler(Filters.document, upload))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
