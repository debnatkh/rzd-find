import logging
import os
import sys
import time
from typing import List, NamedTuple

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()


class Class(NamedTuple):
    class_name: str
    count_tickets: int
    price: int


def search_for_ticket(search_time: str = '21:00') -> List[Class]:
    driver.get('https://ticket.rzd.ru/searchresults/v/1/5a3244bc340c7441a0a556ca/5a323c29340c7441a0a556bb/2023-09-03')
    count = 0
    while 'Бетанкур' not in driver.page_source:
        time.sleep(20)
        count += 1
        if count == 60:
            return []
    elems = driver.find_elements(By.XPATH, '//rzd-search-results-card-railway-flat-card')
    logging.info(f'Found {len(elems)} trains')
    elems = [e for e in elems if search_time in e.text]
    logging.info(f'Found {len(elems)} trains matching time {search_time}')
    assert len(elems) == 1
    e = elems[0]
    classes = e.find_elements(By.XPATH, './/rzd-card-class')
    logging.info(f'Found {len(classes)} classes')
    fetched_classes = []
    for x in classes:
        x = x.text.split('\n')
        assert len(x) == 3
        fetched_class = Class(x[0], int(x[1]), int(''.join([c for c in x[2] if c.isdigit()])))
        logging.info(f'Found class: {fetched_class}')
        fetched_classes.append(fetched_class)
    return fetched_classes


TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID', '95671770')


def send_telegram_notification(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    return response.json()


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

if __name__ == '__main__':
    while True:
        tickets = search_for_ticket('21:00')
        for ticket in tickets:
            if ticket.class_name.lower() in ['эконом', 'эконом+', 'базовый']:
                send_telegram_notification(str(ticket))
        time.sleep(60)
    driver.quit()
