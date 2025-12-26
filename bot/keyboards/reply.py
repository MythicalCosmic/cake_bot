"""
Reply keyboards
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.config import get_translation
from bot.handlers.cake import CAKE_OPTIONS


def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Get main reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Option 1")],
            [KeyboardButton(text="Option 2")]
        ],
        resize_keyboard=True
    )
    return keyboard


def phone_request_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get keyboard for requesting phone number"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.share_phone_number", language=language), request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def main_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Get main reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.option_1", language=language))],
            [KeyboardButton(text=get_translation("buttons.option_2", language=language))]
        ],
        resize_keyboard=True
    )
    return keyboard


def cake_menu_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """Get cake selection keyboard with prices"""
    buttons = [[KeyboardButton(text=cake)] for cake in CAKE_OPTIONS.keys()]
    buttons.append([KeyboardButton(text=get_translation("buttons.back", language))])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def would_image_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """Get would you like to add an image keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.yessir", language=language))],
            [KeyboardButton(text=get_translation("buttons.nosir", language=language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def confirmation_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """Get order confirmation keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.confirm", language=language))],
            [KeyboardButton(text=get_translation("buttons.cancel", language=language))]
        ],
        resize_keyboard=True
    )
    return keyboard


def back_keyboard(language: str = "uz") -> ReplyKeyboardMarkup:
    """Get back button keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation("buttons.back", language=language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard