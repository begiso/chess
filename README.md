# Aiogram 3.x Bot Template

Готовый шаблон для создания Telegram-ботов на **aiogram 3.15**.

## Возможности

- ✅ Модульная структура (handlers, middlewares, utils)
- ✅ Router-based архитектура
- ✅ Антифлуд middleware
- ✅ Глобальная обработка ошибок
- ✅ Автоматическое уведомление админов при запуске
- ✅ Настройка команд бота
- ✅ FSM (Finite State Machine) ready

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

или с Pipenv:

```bash
pipenv install
```

### 2. Настройка

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env`:
- `BOT_TOKEN` - токен от @BotFather
- `ADMINS` - ID администраторов (через запятую)
- `ip` - IP адрес хоста

### 3. Запуск

```bash
python app.py
```

## Структура проекта

```
├── app.py                      # Точка входа
├── loader.py                   # Инициализация Bot и Dispatcher
├── data/
│   └── config.py              # Конфигурация
├── handlers/
│   ├── users/                 # Обработчики для пользователей
│   │   ├── start.py          # /start команда
│   │   ├── help.py           # /help команда
│   │   └── echo.py           # Эхо-бот
│   └── errors/               # Обработка ошибок
│       └── error_handler.py
├── middlewares/
│   └── throttling.py         # Антифлуд
├── keyboards/
│   ├── default/              # Обычные клавиатуры
│   └── inline/               # Inline клавиатуры
├── filters/                  # Кастомные фильтры
├── states/                   # FSM состояния
└── utils/
    ├── set_bot_commands.py   # Настройка команд
    └── notify_admins.py      # Уведомления админам
```

## Добавление новых handlers

### Пример handler'а:

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("mycommand"))
async def my_handler(message: Message):
    await message.answer("Hello!")
```

### Подключение:

В `handlers/__init__.py`:

```python
from . import my_new_handler

def setup_routers() -> Router:
    router = Router()
    router.include_router(my_new_handler.router)
    return router
```

## Миграция с aiogram 2.x

Если у вас есть бот на aiogram 2.x, см. [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

## Документация

- [Официальная документация aiogram 3.x](https://docs.aiogram.dev/en/latest/)
- [Примеры](https://github.com/aiogram/aiogram/tree/dev-3.x/examples)

## Лицензия

MIT
