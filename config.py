token = "YOUR_TOKEN"

allowed_channel = ["ID_CHANNEL"]

proxy = "ID_PROXY"

gemini_token = "GEMINI_TOKEN"

gemini_prompt = ("Привет! Ты обноружитель вредных картинок, твоя задача ответить мне, содержет ли картинка или картинки"
                 "непристойное содержание такое как: порно, секс, эротический контент. Если фото содержит переписку "
                 "отвечай нет. если имеет ответь да, если неимеет, ответь нет. Ответь кратко, да или нет.")

db_file_path = "user_db.pickle"

start_command_photo_path = "image.png"

extensions_white_list = [
    ".mpeg",
    ".webp"
    ".jpeg",
    ".jpg",
    ".gif",
    ".mp4",
    ".png"
]
