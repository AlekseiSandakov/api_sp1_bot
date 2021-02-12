import os
import time
import requests
import telegram
import logging
from dotenv import load_dotenv


load_dotenv()


PRAKTIKUM_TOKEN = os.environ['PRAKTIKUM_TOKEN']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
DZ_URL = 'https://praktikum.yandex.ru'
LONG_TIME = 1200
SHORT_TIME = 5


def parse_homework_status(homework):
    try:
        homework_name = homework.get('homework_name')
        if homework['status'] == 'rejected':
            verdict = 'К сожалению в работе нашлись ошибки.'
        else:
            verdict = ('Ревьюеру всё понравилось, '
                       'можно приступать к следующему уроку.')
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'
    except Exception:
        logging.exception()
        bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
        return bot_client.parse_homework_status(CHAT_ID,
                                                'Ошибка получения статуса')


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = int(time.time())
        return dict()
    params = {'from_date': current_timestamp}
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    try:
        api_url = '{}/{}'.format(DZ_URL, 'api/user_api/homework_statuses/')
        homework_statuses = requests.get(api_url, params=params,
                                         headers=headers)
        return homework_statuses.json()
    except Exception:
        logging.exception()
        bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
        return bot_client.get_homework_statuses(CHAT_ID,
                                                'Ошибка получения статуса')


def send_message(message, bot_client):
    logging.debug('Момент запуска!')
    logging.info('Отправка сообщения!')
    logging.error('Ошибка!')
    return bot_client.send_message(CHAT_ID, text=message)


def main():
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.debug('Момент запуска!')
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                var1 = parse_homework_status(new_homework.get('homeworks')[0])
                send_message(var1, bot_client)
            current_timestamp = new_homework.get('current_date',
                                                 current_timestamp)
            time.sleep(LONG_TIME)
        except Exception:
            logging.exception()
            return bot_client.send_message(CHAT_ID, 'Ошибка получения статуса')
            time.sleep(SHORT_TIME)


if __name__ == '__main__':
    main()
