import logging
from logging import StreamHandler, Formatter
import win32com.client as win32

mail_logger = logging.getLogger(__name__)


class LoggerSendMail(StreamHandler):
    """
    РљР»Р°СЃСЃ РґР»СЏ РїРµСЂРµРЅР°РїСЂР°РІР»РµРЅРёСЏ РїРѕС‚РѕРєР° РІС‹РІРѕРґР° Р»РѕРіР° РІ РїРѕС‡С‚Сѓ
    """

    def __init__(self, user_mail: str) -> None:
        super().__init__()
        self.user_mail = user_mail

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        outlook = win32.Dispatch('outlook.application')
        cur_mail = outlook.CreateItem(0)
        cur_mail.To = self.user_mail
        cur_mail.Body = msg
        cur_mail.Send()


class LoggerMailFormatter(Formatter):
    """
    РљР»Р°СЃСЃ РґР»СЏ РЅР°СЃС‚СЂРѕР№РєРё С„РѕСЂРјР°С‚Р° Р»РѕРіР°
    """

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.INFO: format,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
