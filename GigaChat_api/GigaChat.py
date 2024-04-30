import asyncio
import os
import re
import shutil

import config
from log_to_mail import MailExecutor
from GigaChat_api.functions.request_api import *


class GigaChat:
    """
    Класс GigaChat используется для отправки запросов через api,
    для корректного взаимодействия с моделью необходимо передать при инициализации обязательные параметры:
    - Контекст для модели GigaChat, для выполнения ответа в соответствии с интересующим нас результатом
    - Сам запрос в формате строки либо списка строк.

    Кроме того класс принимает необязательные параметры:
    - Имя используемой модели для отправки запросов (GigaChat-Pro, GigaChat-Lite, GigaChat:latest)
    - Параметр, определяющий вариативность ответов модели (0 <= temperature <= 2)
    - Пути до директории в которой хранятся Ваши ключи для сертификата доступа к модели. При их отсутствии
    следует передать при старте запросов secret_key, который можно получить зарегистрировавшись на сайте GigaChat api.
    """

    semaphore = asyncio.Semaphore(10)
    __ssl_context: object or None = config.SSL_CONTEXT
    __headers: dict or None = config.HEADERS
    __url: str = config.URL_FROM_MODEL

    def __init__(self,
                 version: str = "GigaChat-Pro",
                 temperature: float = 0.01,
                 ):
        self.version = version
        self.temperature = temperature

    async def __sending_message(self, session: aiohttp.ClientSession, payload: json) -> json:
        return await response_requests(session=session,
                                       semaphore=self.semaphore,
                                       url=self.__url,
                                       data=payload,
                                       headers=self.__headers,
                                       verify_ssl=False,
                                       ssl_context=self.__ssl_context)

    async def _main_coro(self, request: str or list[str], context: str) -> list[json]:
        txt_json = json_dumps(version=self.version,
                              context=context,
                              temperature=self.temperature,
                              request=request)
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.__sending_message(session, item)) for item in txt_json]
            await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
        return [res.result() for res in tasks]

    @MailExecutor.send_mail
    def start_request(self, request: str or list[str], context: str = "Проанализируй вопрос") -> list[json]:
        return asyncio.run(self._main_coro(request, context))


class GenerationImage(GigaChat):
    """
    Генерация картинок по запросу и сохранение их в загрузки
    """

    _pattern: re.Pattern = re.compile(r'(?<=src=")[^"]+')
    __headers: dict or None = config.HEADERS_IMAGE
    __sert: tuple or None = (config.CERT_PEM, config.CERT_KEY) if config.SSL_CONTEXT is not None else None

    def __init__(self,
                 image_name: str = "Картинка_от_GigaChat",
                 save_image_flag: bool = False):
        super().__init__()
        self.image_name = image_name
        self.save_image_flag = save_image_flag

    async def _main_coro(self, request: str or list[str], context: str) -> None:
        temp_request = await super()._main_coro(request, context)
        self._generation_for_image(temp_request)

    def start_gen_image(self, request: str or list[str]) -> None:
        super().start_request(request, config.SYSTEM_PROMPT_ROM_IMAGE)

    def _save_image(self, resp) -> None:
        repository = fr"C:\Users\{os.getlogin()}\Downloads"
        with open(fr"{repository}\{self.image_name}.jpg", 'wb') as out_file:
            shutil.copyfileobj(resp.raw, out_file)
            print(f"Картинка с именем {self.image_name} сохранена по адресу {repository}")

    def _generation_for_image(self, temp_request) -> None:
        try:
            print("Запущена генерация картинки")
            id_image = self._pattern.search(temp_request[0]["choices"][0]["message"]["content"])
            url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{id_image[0]}/content"
            answer = request_get_image(url=url,
                                       headers=self.__headers,
                                       sert=self.__sert,
                                       stream=True,
                                       verify=False)
        except (KeyError, TypeError):
            print("Контекст вопроса не корректен")
            exit()
        if self.save_image_flag:
            self._save_image(answer)


if __name__ == "__main__":
    example_class = GenerationImage(image_name="Цветы", save_image_flag=True)
    example_class.start_gen_image(request="Нарисуй пионы в вазе")
