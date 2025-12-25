"""
Command handlers
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.keyboards.reply import main_keyboard
from utils.helpers import get_phone_number, user_exists, set_user_state
from core.config import get_translation, get_button_text
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from bot.states.user import UserStates
from bot.keyboards.reply import phone_request_keyboard


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz" 
        phone_number = await get_phone_number(user_id)
        
        if await user_exists(user_id) and phone_number:
            await message.answer(
                get_translation("welcome_back", language=language),
                reply_markup=main_keyboard(language),
                parse_mode="HTML"
            )
            await state.set_state(UserStates.menu)
            await set_user_state(user_id, UserStates.menu.state)
        else:
            await message.answer(
                get_translation("welcome_phone_request", language=language),
                reply_markup=phone_request_keyboard(),
                parse_mode="HTML"
            )
            await state.set_state(UserStates.phone_number)
            await set_user_state(user_id, UserStates.phone_number.state)
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )