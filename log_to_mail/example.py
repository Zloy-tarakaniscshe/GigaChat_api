from log_to_mail.mail_sender import MailExecutor


@MailExecutor.send_mail
def example():
    """
    Пример использования декоратора для отправки уведомлений на почту
    """
    return 2 + 2


example()
