import GeminiModule
import threading
import handlers
import telebot
import config
import utils

gm = GeminiModule.GeminiModule(config.proxy, config.gemini_token)

bot = telebot.TeleBot(token=config.token)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    if message.chat.id not in config.allowed_channel:
        return
    threading.Thread(target=lambda: handlers.handle_photo(message, bot, gm)).start()


@bot.message_handler(content_types=['animation'])
def handle_animation(message: telebot.types.Message):
    if message.chat.id not in config.allowed_channel:
        return
    threading.Thread(target=lambda: handlers.handle_animation(message, bot, gm)).start()


@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: telebot.types.Message):
    if message.chat.id not in config.allowed_channel:
        return
    threading.Thread(target=lambda: handlers.handle_sticker(message, bot, gm)).start()


@bot.message_handler(commands=["start"])
def say_start(message: telebot.types.Message):
    if not utils.add_to_db(message.from_user.id):
        threading.Thread(target=lambda: handlers.start_text(message, bot)).start()


if __name__ == "__main__":
    threading.Thread(target=handlers.queue_handler).start()
    bot.infinity_polling()
