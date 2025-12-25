"""
Authentication middleware
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.helpers import user_exists, add_user, set_user_state
from bot.states.user import UserStates
from core.config import get_translation
from bot.keyboards.reply import phone_request_keyboard


class AuthMiddleware(BaseMiddleware):
    """Middleware for user authentication"""
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        first_name = event.from_user.first_name
        last_name = event.from_user.last_name
        username = event.from_user.username

        if not await user_exists(user_id):
            await add_user(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            await set_user_state(user_id, UserStates.phone_number.state)

            await event.answer(
                get_translation("welcome_phone_request", language="uz"),
                reply_markup=phone_request_keyboard(),
                parse_mode="HTML"
            )
            state = data['state']
            await state.set_state(UserStates.phone_number.state)
            return
        return await handler(event, data)