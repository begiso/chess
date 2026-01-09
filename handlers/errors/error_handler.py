import logging
from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.exceptions import (
    TelegramUnauthorizedError,
    TelegramBadRequest,
    TelegramNotFound,
    TelegramConflictError,
    TelegramForbiddenError
)

router = Router()


@router.error()
async def error_handler(event: ErrorEvent):
    """
    Глобальный обработчик ошибок для aiogram 3.x
    """
    
    exception = event.exception
    
    if isinstance(exception, TelegramUnauthorizedError):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, TelegramBadRequest):
        if "message is not modified" in str(exception).lower():
            logging.exception('Message is not modified')
            return True
        if "message can't be deleted" in str(exception).lower():
            logging.exception('Message cant be deleted')
            return True
        if "message to delete not found" in str(exception).lower():
            logging.exception('Message to delete not found')
            return True
        if "message text is empty" in str(exception).lower():
            logging.exception('MessageTextIsEmpty')
            return True

    if isinstance(exception, TelegramNotFound):
        logging.exception(f'TelegramNotFound: {exception}')
        return True

    if isinstance(exception, TelegramConflictError):
        logging.exception(f'TelegramConflictError: {exception}')
        return True
        
    if isinstance(exception, TelegramForbiddenError):
        logging.exception(f'TelegramForbiddenError: {exception}')
        return True
    
    logging.exception(f'Update: {event.update} \n{exception}')
    return True
