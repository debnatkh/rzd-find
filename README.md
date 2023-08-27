## Использование:
1. Перейдите на страницу поиска билетов, вставьте ссылку следующего вида: `https://ticket.rzd.ru/searchresults/v/1/5a3244bc340c7441a0a556ca/5a323c29340c7441a0a556bb/2023-09-03` вместо другой ссылки в коде
1. Укажите в коде нужное время (вместо `21:00`)
1. Получите TELEGRAM_API_TOKEN для своего бота
1. Начните переписку с ботом, узнайте свой `chat_id`
1. Установите `selenium`, `requests`
1. Укажите в коде искомые типы билетов (по дефолту: базовый и эконом)
1. Запуск бота:
```bash
CHAT_ID=<your_chat_id_here> TELEGRAM_API_TOKEN=<telegram_bot_token_from_botfather> python3 main.py
```