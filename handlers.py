import telebot
import config
import utils
import time

queue = []


def queue_handler():
    while True:
        for func in queue:
            func()
            queue.remove(func)
        time.sleep(2)


def handle_photo(message: telebot.types.Message, bot: telebot.TeleBot, gm):
    photo = message.photo[-1]
    queue.append(lambda: utils.censor(message, bot, gm, photo.file_id))


def handle_animation(message: telebot.types.Message, bot: telebot.TeleBot, gm):
    queue.append(lambda: utils.censor(message, bot, gm, message.animation.file_id))


def handle_sticker(message: telebot.types.Message, bot: telebot.TeleBot, gm):
    queue.append(lambda: utils.censor(message, bot, gm, message.sticker.file_id))


def start_text(message: telebot.types.Message, bot: telebot.TeleBot):
    with open(config.start_command_photo_path, "rb") as photo:
        bot.send_photo(message.chat.id, photo, "Приветствую!\nЭтот бот создан для регулирования трафика в"
                                               " Телеграм каналах при помощи нейросети.")