import os
import time

import requests
import telegram
import logging
from dotenv import load_dotenv


load_dotenv()


PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
print(PRAKTIKUM_TOKEN)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
print(TELEGRAM_TOKEN)
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
print(CHAT_ID)
DZ_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = ('Ревьюеру всё понравилось, '
                   'можно приступать к следующему уроку.')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        current_timestamp = 0
    params = {'from_date': current_timestamp}
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    try:
        homework_statuses = requests.get(DZ_URL, params=params,
                                         headers=headers)
        return homework_statuses.json()
    except requests.RequestException as error:
        logging.exception(error)


def send_message(message, bot_client):
    logging.debug('Момент запуска!')
    logging.info('Отправка сообщения!')
    logging.error('Ошибка!')
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.debug('Момент запуска!')
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status
                             (new_homework.get('homeworks')[0]), bot_client)
            current_timestamp = new_homework.get('current_date',
                                                 current_timestamp)
            time.sleep(1200)

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
