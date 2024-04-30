import os
import ssl
import requests
import uuid
from dotenv import load_dotenv


load_dotenv()
URL_FROM_MODEL = os.getenv("URL")
CERT_PEM = os.getenv(r"PEM")
CERT_KEY = os.getenv(r"CERT_KEY")
__SECRET_KEY = os.getenv(r"SECRET_KEY")

SYSTEM_PROMPT_ROM_IMAGE = """Если тебя просят создать изображение, 
ты должен сгенерировать специальный блок: <fuse>text2image(query: str, style: str)</fuse>,\n
где query — текстовое описание желаемого изображения, style — необязательный параметр, задающий стиль изображения."""

try:
    SSL_CONTEXT = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    SSL_CONTEXT.load_cert_chain(CERT_PEM, CERT_KEY)
except (FileNotFoundError, OSError):
    SSL_CONTEXT = None

try:
    __header = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": str(uuid.uuid4()),
                "Authorization": f"Basic {__SECRET_KEY}"
    }

    __response = requests.request("POST",
                                  "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
                                  headers=__header,
                                  data="scope=GIGACHAT_API_PERS",
                                  verify=False)

    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + __response.json()["access_token"]
    }
    HEADERS_IMAGE = {
        'Accept': 'application/jpg',
        'Authorization': "Bearer " + __response.json()["access_token"]
    }

except requests.RequestException:
    HEADERS = None
    HEADERS_IMAGE = None

if SSL_CONTEXT is not None and HEADERS is not None:
    HEADERS = None
