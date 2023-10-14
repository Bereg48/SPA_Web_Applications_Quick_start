import telegram


class TelegramNotifier:
    def __init__(self, token):
        """Метод __init__ инициализирует объект класса TelegramNotifier. Он принимает один аргумент - токен,
        необходимый для взаимодействия с Telegram API. """
        self.bot = telegram.Bot(token=token)

    def send_notification(self, chat_id, message):
        """Метод send_notification отправляет уведомление через Telegram. Он принимает два аргумента - идентификатор
        чата (chat_id) и текст сообщения (message).Внутри метода send_notification вызывается метод send_message
        объекта bot, передавая ему идентификатор чата и текст сообщения. Это позволяет отправить сообщение через
        Telegram API."""
        self.bot.send_message(chat_id=chat_id, text=message)
