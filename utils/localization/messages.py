MESSAGES = {
    'ru': {
        # Start command
        'start_greeting': (
            'Привет, {name}!\n\n'
            '♟ Я помогу проанализировать шахматную позицию по фото.\n\n'
            'Выберите язык:'
        ),
        'language_selected': '🇷🇺 Выбран русский язык',

        # Help
        'help_text': (
            '♟ <b>Как пользоваться ботом:</b>\n\n'
            '1. Отправьте фото шахматной позиции\n'
            '2. Получите анализ лучшего хода с объяснением\n\n'
            '<b>Команды:</b>\n'
            '/start - Начать работу\n'
            '/help - Помощь\n'
            '/language - Сменить язык\n\n'
            '⚠️ <b>Disclaimer:</b> Бот предназначен для обучения и анализа. '
            'Использование во время онлайн-партий может нарушать правила игровых платформ.'
        ),

        # Analysis
        'processing': '⏳ Анализирую позицию...',
        'analysis_result': (
            '♟ <b>Позиция проанализирована</b>\n\n'
            '<b>Лучший ход:</b> {move}\n'
            '<b>Оценка позиции:</b> {evaluation}\n\n'
            '<b>Почему этот ход:</b>\n{explanation}'
        ),

        # Errors
        'error_image_too_large': '❌ Файл слишком большой. Максимум 10 МБ.',
        'error_invalid_format': '❌ Неподдерживаемый формат. Отправьте JPG или PNG.',
        'error_no_board': '❌ Не удалось распознать шахматную доску на изображении. Попробуйте другое фото.',
        'error_invalid_fen': '❌ Распознанная позиция некорректна. Попробуйте другое фото.',
        'error_analysis_failed': '❌ Ошибка анализа. Попробуйте позже.',
        'error_general': '❌ Произошла ошибка. Попробуйте еще раз.',

        # Evaluation
        'eval_white_winning': '(большое преимущество белых)',
        'eval_white_advantage': '(небольшое преимущество белых)',
        'eval_equal': '(равная позиция)',
        'eval_black_advantage': '(небольшое преимущество черных)',
        'eval_black_winning': '(большое преимущество черных)',
        'eval_mate_in': '(мат в {moves})',

        # Buttons
        'btn_russian': '🇷🇺 Русский',
        'btn_uzbek': '🇺🇿 O\'zbekcha',
    },
    'uz': {
        # Start command
        'start_greeting': (
            'Salom, {name}!\n\n'
            '♟ Men rasm orqali shaxmat pozitsiyasini tahlil qilishga yordam beraman.\n\n'
            'Tilni tanlang:'
        ),
        'language_selected': '🇺🇿 O\'zbek tili tanlandi',

        # Help
        'help_text': (
            '♟ <b>Botdan qanday foydalanish:</b>\n\n'
            '1. Shaxmat pozitsiyasi rasmini yuboring\n'
            '2. Eng yaxshi yurish tahlilini tushuntirish bilan oling\n\n'
            '<b>Buyruqlar:</b>\n'
            '/start - Ishni boshlash\n'
            '/help - Yordam\n'
            '/language - Tilni o\'zgartirish\n\n'
            '⚠️ <b>Ogohlantirish:</b> Bot ta\'lim va tahlil uchun mo\'ljallangan. '
            'Onlayn o\'yinlar paytida foydalanish o\'yin platformalari qoidalarini buzishi mumkin.'
        ),

        # Analysis
        'processing': '⏳ Pozitsiyani tahlil qilyapman...',
        'analysis_result': (
            '♟ <b>Pozitsiya tahlil qilindi</b>\n\n'
            '<b>Eng yaxshi yurish:</b> {move}\n'
            '<b>Pozitsiya bahosi:</b> {evaluation}\n\n'
            '<b>Nima uchun bu yurish:</b>\n{explanation}'
        ),

        # Errors
        'error_image_too_large': '❌ Fayl juda katta. Maksimum 10 MB.',
        'error_invalid_format': '❌ Qo\'llab-quvvatlanmaydigan format. JPG yoki PNG yuboring.',
        'error_no_board': '❌ Rasmda shaxmat taxtasini aniqlab bo\'lmadi. Boshqa rasm yuboring.',
        'error_invalid_fen': '❌ Aniqlangan pozitsiya noto\'g\'ri. Boshqa rasm yuboring.',
        'error_analysis_failed': '❌ Tahlil xatosi. Keyinroq urinib ko\'ring.',
        'error_general': '❌ Xatolik yuz berdi. Qaytadan urinib ko\'ring.',

        # Evaluation
        'eval_white_winning': '(oqlarning katta ustunligi)',
        'eval_white_advantage': '(oqlarning ozgina ustunligi)',
        'eval_equal': '(teng pozitsiya)',
        'eval_black_advantage': '(qoralarning ozgina ustunligi)',
        'eval_black_winning': '(qoralarning katta ustunligi)',
        'eval_mate_in': '({moves} yurishda mat)',

        # Buttons
        'btn_russian': '🇷🇺 Ruscha',
        'btn_uzbek': '🇺🇿 O\'zbekcha',
    }
}


def get_message(lang: str, key: str, **kwargs) -> str:
    """
    Get localized message

    Args:
        lang: Language code ('ru' or 'uz')
        key: Message key
        **kwargs: Format arguments

    Returns:
        Localized message string
    """
    message = MESSAGES.get(lang, MESSAGES['ru']).get(key, MESSAGES['ru'].get(key, ''))
    return message.format(**kwargs) if kwargs else message
