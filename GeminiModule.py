import google.generativeai as genai
import time
import os


def _set_proxy(proxy):
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy


class GeminiModule:
    def __init__(self, proxy: str, gemini_token: str):
        """
        Прокси передавай в таком формате - http://login:password@ip:port/
        Токен ты можешь получить на сайте гугла https://aistudio.google.com/app/apikey когда будешь создавать ключ выбери Generative Language Client
        """
        genai.configure(api_key=gemini_token)
        _set_proxy(proxy)

    def generate(self, prompt: str, images=None, temperature=0.5, model="gemini-1.5-flash-latest",
                 return_none_when_exception=True) -> str | Exception | None:
        """
        генерирует ответ на основе промтпта, изображения кидать списком в формате PIL.Image вернет сгенерированный ответ
        модели можешь найти здесь https://ai.google.dev/gemini-api/docs/models/gemini. По умолчанию стоит лучшая у которой наименьший рейтлимит
        """
        send_prompt = []
        if images is not None:
            send_prompt.extend(images)
        send_prompt.append(prompt)
        model = genai.GenerativeModel(model)
        try:
            response = model.generate_content(
                contents=send_prompt,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_DANGEROUS",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    }
                ],
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=6000,
                    temperature=temperature
                ))
            return response.text
        except Exception as ex:
            if not return_none_when_exception:
                return ex
            else:
                return None

    def upload_file(self, path: str | os.PathLike, return_when_uploaded=False) -> genai.types.File:
        video_file = genai.upload_file(path=path)
        if return_when_uploaded:
            return video_file
        while video_file.state.name == "PROCESSING":
            time.sleep(3)
            video_file = genai.get_file(video_file.name)
        return video_file

    def remove_all_uploaded_files(self) -> list[genai.types.File]:
        deleted_files = []
        for file in genai.list_files():
            deleted_files.append(file)
            file.delete()
        return deleted_files
