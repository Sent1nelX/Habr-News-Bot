# 📰 Habr News Bot

![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-009688?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/license-не%20указана-lightgrey)

Телеграм-бот, который автоматически мониторит раздел новостей [Хабра](https://habr.com/ru/news/), суммаризирует статьи с помощью ИИ (Mistral) и публикует их в указанный Telegram-канал.

---

## 📌 Назначение / Описание

Бот предназначен для автоматического ведения Telegram-канала в стиле новостной ленты. Он самостоятельно:

1. Парсит последние новости с `habr.com/ru/news/`.
2. Извлекает полный текст, изображения и хабы каждой статьи.
3. Пересказывает материал в коротком, живом формате Telegram-поста при помощи модели **Mistral Large**.
4. Публикует пост (с изображением, если оно есть) в нужный канал.
5. Хранит обработанные посты в базе данных, чтобы не публиковать одно и то же дважды.

---

## ✨ Возможности

| Функция | Описание |
|---|---|
| 🤖 Автопарсинг | Проверяет новые посты каждые **5 минут** |
| 🧠 AI-суммаризация | Переписывает длинную статью в короткий Telegram-пост (≤ 500 символов) с хэштегами |
| 🖼 Изображения | Прикрепляет первое изображение из статьи к посту |
| 📊 Статистика | Команда `/status` — аптайм, кол-во обработанных постов, топ хабов с графиком |
| 🔄 Принудительная проверка | Команда `/force_check` — запускает проверку немедленно |
| 🔒 Защита команд | Только администраторы (из `ADMIN_IDS`) могут управлять ботом |
| 💾 Персистентность | SQLite через SQLAlchemy + aiosqlite |

---

## 🛠 Технологии

- **Python 3.11+**
- [aiogram 3](https://docs.aiogram.dev/) — асинхронный Telegram Bot API фреймворк
- [aiohttp](https://docs.aiohttp.org/) — HTTP-клиент для парсинга
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML-парсер
- [Mistral AI SDK](https://docs.mistral.ai/) — генерация суммаризаций
- [SQLAlchemy 2 + aiosqlite](https://docs.sqlalchemy.org/) — ORM и асинхронный доступ к SQLite
- [APScheduler](https://apscheduler.readthedocs.io/) — планировщик задач (интервальный запуск)
- [environs](https://github.com/sloria/environs) — загрузка `.env` файла
- [matplotlib](https://matplotlib.org/) — генерация графика хабов

---

## 📋 Требования

- Python **3.11** или выше
- Telegram-бот (токен от [@BotFather](https://t.me/BotFather))
- Бот должен быть **администратором** целевого канала с правом публикации сообщений
- API-ключ [Mistral AI](https://console.mistral.ai/)
- Доступ в интернет (для парсинга Хабра и обращения к Mistral API)

---

## 🚀 Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/Sent1nelX/Habr-News-Bot.git
cd Habr-News-Bot

# 2. Создайте и активируйте виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# 3. Установите зависимости
pip install -r requirements.txt
```

---

## ⚙️ Настройка

Скопируйте файл-пример и заполните свои значения:

```bash
cp .env.example .env
```

Откройте `.env` и укажите:

```dotenv
# Токен Telegram-бота (получить у @BotFather)
BOT_TOKEN=your_bot_token_here

# ID Telegram-канала, куда публиковать посты (например: -1001234567890)
CHANNEL_ID=-100xxxxxxxxxx

# Telegram ID администраторов через запятую (без пробелов)
ADMIN_IDS=123456789,987654321

# API-ключ Mistral AI (получить на console.mistral.ai)
MISTRAL_API_KEY=your_mistral_api_key_here

# URL базы данных (по умолчанию SQLite в корне проекта)
DATABASE_URL=sqlite+aiosqlite:///posts.db
```

### Как получить `CHANNEL_ID`

1. Добавьте бота [@username_to_id_bot](https://t.me/username_to_id_bot) или перешлите любое сообщение из канала боту [@getidsbot](https://t.me/getidsbot).
2. Для публичных каналов ID имеет вид `-100XXXXXXXXXX`.

### Как получить `ADMIN_IDS`

Отправьте команду `/start` боту [@userinfobot](https://t.me/userinfobot) — он вернёт ваш числовой ID.

---

## ▶️ Запуск

```bash
python bot.py
```

При запуске бот:
- Инициализирует базу данных (создаёт таблицы, если их нет).
- Сразу выполняет первую проверку новых постов.
- Запускает планировщик — проверка каждые **5 минут**.
- Начинает принимать команды `/status` и `/force_check` от администраторов.

Для автоматического перезапуска в продакшене рекомендуется использовать **systemd**, **supervisord** или [Render.com](https://render.com/) (в репозитории уже есть `render.yaml`).

---

## 💬 Пример использования

### Публикация в канале

Каждые 5 минут бот проверяет новые материалы на `habr.com/ru/news/` и публикует пост вида:

```
⚡️ Заголовок новости — КРАТКО И ПО ДЕЛУ

Пара предложений с ключевыми фактами. ВАЖНЫЕ ЦИФРЫ выделены капсом.
Вывод одним предложением.

#Хаб1 #Хаб2 #IT
```

### Команды бота (только для администраторов)

| Команда | Описание |
|---|---|
| `/status` | Показывает аптайм, кол-во постов, топ хабов с графиком и список последних 5 постов |
| `/force_check` | Немедленно запускает проверку и публикацию новых постов |

---

## 📁 Структура проекта

```
Habr-News-Bot/
├── bot/
│   ├── handlers/
│   │   ├── admin.py        # Обработчики команд /status и /force_check
│   │   └── errors.py       # Обработчик ошибок
│   ├── middlewares/        # AdminMiddleware — фильтр по ADMIN_IDS
│   ├── services/
│   │   ├── parser.py       # Парсинг новостей с Хабра (aiohttp + BS4)
│   │   ├── summarizer.py   # Суммаризация через Mistral AI
│   │   └── stats.py        # Сбор статистики и генерация графика
│   └── utils/
│       └── misc.py         # Вспомогательные утилиты (setup_bot и др.)
├── config/
│   └── config.py           # Загрузка конфигурации из .env
├── database/
│   ├── models.py           # SQLAlchemy модели
│   └── storage.py          # Класс Storage — работа с БД
├── bot.py                  # Точка входа
├── requirements.txt        # Зависимости
├── render.yaml             # Конфигурация деплоя на Render.com
├── .env.example            # Пример файла переменных окружения
└── .env                    # Ваши секреты (не коммитить!)
```

---

## 📄 Лицензия

Лицензия не указана. Все права принадлежат автору.

---

## 🤝 Контрибьютинг

Проект молодой, и баги вполне возможны. Если нашли проблему или хотите предложить улучшение:

1. Создайте [issue](https://github.com/Sent1nelX/Habr-News-Bot/issues) с подробным описанием.
2. Или форкните репозиторий, внесите изменения и откройте Pull Request.

По вопросам и предложениям также можно написать автору в Telegram: **[@Sent1nelXC](https://t.me/Sent1nelXC)**
