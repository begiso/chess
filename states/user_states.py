from aiogram.fsm.state import State, StatesGroup


class LanguageSelection(StatesGroup):
    """Language selection flow"""
    waiting_for_language = State()


class ChessAnalysis(StatesGroup):
    """Chess analysis flow (for future extensions)"""
    waiting_for_image = State()
