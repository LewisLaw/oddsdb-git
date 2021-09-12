import os
import telegram
import configparser
from logging import Handler, LogRecord


class TelegramBotHandler(Handler):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read('./config.ini')
        config = config['telegram_bot']
        
        self.token = config['Token']
        self.chat_id = config['Group_ChatId']

    def emit(self, record: LogRecord):
        bot = telegram.Bot(token=self.token)
        bot.send_message(
            self.chat_id,
            self.format(record)
        )