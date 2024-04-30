import aiohttp
import requests
import json


def json_dumps(version: str,
               context: str,
               temperature: float,
               request: str or list[str]) -> list[json]:
    """
    Преобразование итерируемого объекта содержащего строковые объекты или строки текста в список объектов формата json
    """
    payload_json = {
        "model": version,
        "messages": [{
            "role": "system",
            "content": context
        }, {
            "role": "user",
            "content": "***INSERT_RESPONCE***"
        }],
        "temperature": temperature,
    }
    if type(request) == str:
        payload_json["messages"][1]["content"] = request
        yield json.dumps(payload_json)
    else:
        for item in request:
            payload_json["messages"][1]["content"] = item
            yield json.dumps(payload_json)


def request_get_image(url, **kwargs):
    """

    :param url: url к которому обращаемся для получения картинки
    :param kwargs: dict с именованными параметрами запроса
    :return: данные картинки
    """
    if kwargs["sert"]:
        del kwargs["headers"]
        return requests.request("GET", url, **kwargs)
    del kwargs["sert"]
    return requests.request("GET", url, **kwargs)


async def response_requests(session: aiohttp.ClientSession, semaphore: object, url: str, **kwargs) -> json:
    """
    Асинхронная отправка запросов GigaChat api и получение результатов модели в формате json
    """
    async with semaphore:
        try:
            async with session.request("POST", url, **kwargs) as resp:
                return await resp.json()
        except aiohttp.client.ClientConnectorCertificateError:
            raise Exception("Проверьте корректность путей к ключам сертификата pem/key")
        except aiohttp.client.ContentTypeError:
            raise Exception("Проверьте правильность URL-модели")
        except Exception:
            raise Exception("Проверьте правильность SECRET_KEY")
