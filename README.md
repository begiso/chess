# Chess Position Analyzer Bot

Telegram-бот для анализа шахматных позиций по фотографии.

## Как работает

1. Отправьте фото шахматной доски боту
2. Gemini Vision распознаёт позицию и конвертирует в FEN
3. Stockfish анализирует позицию и находит лучший ход
4. Gemini генерирует объяснение хода
5. Получите результат с лучшим ходом и объяснением

## Технологии

- **aiogram 3.x** — Telegram Bot API
- **Gemini API** — распознавание изображений и генерация объяснений
- **Stockfish** — шахматный движок для анализа
- **SQLite** — хранение данных пользователей и истории анализов

## Возможности

- Распознавание шахматной доски по фото
- Анализ позиции с оценкой (в пешках или мат в N ходов)
- Объяснение лучшего хода на понятном языке
- Поддержка русского и узбекского языков
- История анализов в базе данных

## Установка

### 1. Клонирование

```bash
git clone https://github.com/begiso/chess.git
cd chess
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

или с Pipenv:

```bash
pipenv install
```

### 3. Настройка

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Заполните `.env`:

| Переменная | Описание |
|------------|----------|
| `BOT_TOKEN` | Токен бота от @BotFather |
| `ADMINS` | ID администраторов (через запятую) |
| `GEMINI_API_KEY` | API ключ Google Gemini |

### 4. Запуск

```bash
python app.py
```

## Структура проекта

```
├── app.py                 # Точка входа
├── loader.py              # Инициализация Bot и Dispatcher
├── data/
│   └── config.py          # Конфигурация
├── handlers/
│   └── users/
│       ├── start.py       # /start команда
│       ├── help.py        # /help команда
│       ├── language.py    # Выбор языка
│       └── chess_analysis.py  # Обработка фото
├── services/
│   └── chess/
│       ├── chess_analyzer.py      # Оркестратор анализа
│       ├── gemini_vision_service.py   # Распознавание позиции
│       ├── gemini_text_service.py     # Генерация объяснений
│       └── stockfish_service.py       # Анализ Stockfish
├── middlewares/
│   ├── throttling.py      # Антифлуд
│   └── language_middleware.py
├── utils/
│   ├── db_api/            # Работа с БД
│   └── localization/      # Локализация (ru/uz)
└── bin/
    └── stockfish/         # Движок Stockfish
```

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Начать работу |
| `/help` | Помощь |
| `/language` | Сменить язык |

## Disclaimer

Бот предназначен для обучения и анализа завершённых партий. Использование во время онлайн-игр может нарушать правила игровых платформ.

## Лицензия

MIT
