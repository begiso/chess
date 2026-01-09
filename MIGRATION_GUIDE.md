# Руководство по миграции на aiogram 3.x

## Основные изменения

### 1. Зависимости
- **aiogram**: `2.14` → `3.15`
- **environs**: `8.0.0` → `11.0.0`
- **Добавлено**: `cachetools` (для middleware)

### 2. Loader (loader.py)
- Убрано: `from aiogram.contrib.fsm_storage.memory import MemoryStorage`
- Добавлено: `from aiogram.fsm.storage.memory import MemoryStorage`
- Добавлено: `DefaultBotProperties` для настройки parse_mode
- Изменено: `Dispatcher(bot, storage=storage)` → `Dispatcher(storage=storage)`

### 3. Запуск бота (app.py)
- Убрано: `from aiogram import executor`
- Добавлено: `import asyncio`
- Изменено: `executor.start_polling()` → `asyncio.run(main())` с `await dp.start_polling(bot)`
- Добавлено: подключение роутеров через `dp.include_router()`

### 4. Handlers
- **Router-based архитектура**: каждый handler теперь использует свой Router
- Убрано: декораторы через `@dp.message_handler()`
- Добавлено: `router = Router()` и `@router.message()`
- Фильтры: `CommandStart()`, `Command()`, `F.text` вместо `state=None`

### 5. Middlewares
- Изменена структура: наследование от `BaseMiddleware`
- Новый метод: `async def __call__(self, handler, event, data)`
- Throttling: используется `cachetools.TTLCache` вместо встроенного механизма

### 6. Error Handler
- Изменены импорты: `from aiogram.exceptions import ...`
- Новые классы исключений: `TelegramUnauthorizedError`, `TelegramBadRequest`, и т.д.
- Декоратор: `@router.error()` вместо `@dp.errors_handler()`
- Параметр: `ErrorEvent` вместо `update, exception`

### 7. Utils
- Изменены сигнатуры: принимают `Bot` вместо `Dispatcher`
- BotCommand: теперь использует именованные параметры `command=` и `description=`

## Как запустить

1. Установите зависимости:
```bash
pip install -r requirements.txt
# или
pipenv install
```

2. Создайте файл `.env`:
```env
BOT_TOKEN=your_token_here
ADMINS=123456789,987654321
ip=localhost
```

3. Запустите бота:
```bash
python app.py
```

## Структура проекта

```
chesscheat/
├── app.py                  # Точка входа
├── loader.py               # Инициализация Bot, Dispatcher
├── requirements.txt        # Зависимости
├── Pipfile                # Pipenv зависимости
├── data/
│   └── config.py          # Конфигурация (.env)
├── handlers/
│   ├── __init__.py        # Подключение роутеров
│   ├── users/             # Обработчики пользователей
│   │   ├── start.py
│   │   ├── help.py
│   │   └── echo.py
│   └── errors/            # Обработчик ошибок
│       └── error_handler.py
├── middlewares/
│   ├── __init__.py
│   └── throttling.py      # Антифлуд
└── utils/
    ├── set_bot_commands.py
    └── notify_admins.py
```

## Полезные ссылки
- [Официальная документация aiogram 3.x](https://docs.aiogram.dev/en/latest/)
- [Migration guide](https://docs.aiogram.dev/en/latest/migration_2_to_3.html)
