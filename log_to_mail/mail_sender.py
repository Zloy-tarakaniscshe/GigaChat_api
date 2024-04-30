import logging
import os
import time

from functools import wraps
from .handler import LoggerSendMail, LoggerMailFormatter


class MailExecutor:
    """
    Класс для отправки писем-уведомлений на почту
    """

    @classmethod
    def send_mail(cls, func):
        """
        Декоратор для отправки уведомления о завершении декорируемой функции
        в зависимости от времени ее выполнения
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            if (end_time := int(round(time.time() - start_time, 3))) > 60:
                mail_logger = logging.getLogger('Main')
                mail_logger.setLevel(logging.INFO)
                user_mail = f'{os.getlogin()}@omega.sbrf.ru'

                ch = LoggerSendMail(user_mail)
                ch.setLevel(logging.INFO)
                ch.setFormatter(LoggerMailFormatter())

                mail_logger.addHandler(ch)
                mail_logger.info(f'Функция {func.__name__} завершила свою работу!. \
                                 \nВремя работы составило {end_time} секунд.')
            return result
        return wrapper
