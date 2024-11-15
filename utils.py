import telebot
import config
import pickle
import uuid
import os

from datetime import datetime
from colorama import Fore
from colorama import init
from PIL import Image


init(autoreset=True)


def log(string, end="\n"):
    print(f"[{datetime.now()}] {string}", end=end)


def _gif_disassembler(path):
    gif = Image.open(path)
    total_frames = gif.n_frames
    frames_paths = []
    for frame_num in range(total_frames):
        gif.seek(frame_num)
        new_frame = gif.copy()
        temp_path = f"frame_{uuid.uuid4()}_{frame_num}.png"
        new_frame.save(temp_path, optimize=True)
        frames_paths.append(temp_path)
    return frames_paths


def censor(message: telebot.types.Message, bot:telebot.TeleBot, gm, file_id):
    file_info = bot.get_file(file_id)
    if file_info.file_size / 1024 / 1024 >= 25:
        log(f"{Fore.RED} Censor: запрос отклонен: вес > 25 мб")
        return
    downloaded_file = bot.download_file(file_info.file_path)
    basename, extension = os.path.splitext(file_info.file_path)
    if extension not in config.extensions_white_list:
        print(extension)
        return
    save_path = f'{uuid.uuid4()}{extension}'
    try:
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        if extension in ".gif":
            paths = _gif_disassembler(save_path)
            files = []
            for path in paths:
                files.append(gm.upload_file(path))
        else:
            files = [gm.upload_file(save_path)]
        text_gm = gm.generate(config.gemini_prompt, files)
        gm.remove_all_uploaded_files()
        if not text_gm:
            log(f"{Fore.GREEN}удалил сообщение от {message.from_user.username} (if not text_gm)")
            bot.reply_to(message, f'{message.from_user.username}, выше изображение было удаленно из-за непристойного содержания')
            bot.delete_message(message.chat.id, message.id)
        if type(text_gm) == str:
            if "да" in text_gm.lower():
                log(f"{Fore.GREEN}удалил сообщение от {message.from_user.username} (text_gm)")
                bot.reply_to(message, f'{message.from_user.username}, выше изображение было удаленно из-за непристойного содержания')
                bot.delete_message(message.chat.id, message.id)
        os.remove(save_path)
        log(f"{Fore.BLUE}Debug: text_gm:{text_gm}")
    except Exception as ex:
        log(f"{Fore.RED}Censor ошибка: {ex}")
        if os.path.exists(save_path):
            os.remove(save_path)


def read_db():
    if os.path.getsize(config.db_file_path) > 0:
        with open(config.db_file_path, "rb") as f:
            return pickle.loads(f.read())


def add_to_db(user_id):
        if not user_id:
            return True
        if not os.path.exists(config.db_file_path):
            with open(config.db_file_path, "wb") as f:
                f.write(pickle.dumps([]))
        users:list = read_db()
        with open(config.db_file_path, "wb") as f:
            if user_id not in users:
                users.append(user_id)
                return False
            f.write(pickle.dumps(users))
            return True