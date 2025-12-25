"""
Message handlers
"""
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from utils.helpers import get_phone_number, user_exists, set_user_state, add_phone_number
from core.config import get_translation, get_button_text
from bot.keyboards.reply import cake_menu_keyboard, main_keyboard, phone_request_keyboard
from bot.states.user import UserStates
import re
from bot.handlers.cake import CAKE_OPTIONS

router = Router()

# @router.message()
# async def echo_message(message: Message):
#     """Echo all text messages"""
#     await message.answer(f"You said: {message.text}")


@router.message(StateFilter(UserStates.phone_number))
async def handle_phone_number(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        phone_number = None
        if message.contact and message.contact.phone_number:
            phone_number = message.contact.phone_number

        elif message.text:
            cleaned_number = re.sub(r'[\s\-\(\)]', '', message.text)
            if re.match(r'^\+998[0-9]{9}$', cleaned_number):
                phone_number = cleaned_number
            elif re.match(r'^998[0-9]{9}$', cleaned_number):
                phone_number = '+' + cleaned_number
            elif re.match(r'^[0-9]{9}$', cleaned_number):
                phone_number = '+998' + cleaned_number
        if phone_number:
            await add_phone_number(user_id=user_id, phone_number=phone_number)
            await set_user_state(user_id=user_id, state=UserStates.menu.state)
            await state.set_state(UserStates.menu)
            await message.answer(
                get_translation("phone_received", language=language),
                reply_markup=main_keyboard(language=language),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                get_translation("phone_invalid", language=language),
                reply_markup=phone_request_keyboard(language=language),
                parse_mode="HTML"
            )
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.menu), lambda message: message.text == get_button_text("option_1", language="uz"))
async def handle_option_1(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        await message.answer(
            get_translation("please_choose_cake", language=language),
            reply_markup=cake_menu_keyboard(language=language),
            parse_mode="HTML"
        )
        await state.set_state(UserStates.product_selection)
        await set_user_state(user_id=user_id, state=UserStates.product_selection.state)

    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.product_selection), lambda message: message.text == get_button_text("back", language="uz"))
async def handle_back_to_menu(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        await message.answer(
            get_translation("main_message", language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode="HTML"
        )
        await state.set_state(UserStates.menu)
        await set_user_state(user_id=user_id, state=UserStates.menu.state)

    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.product_selection))
async def handle_cake_selection(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        selected_cake = message.text
        if selected_cake in CAKE_OPTIONS:
            cake_info = CAKE_OPTIONS[selected_cake]
            await state.update_data(
                cake_name=cake_info["name"],
                cake_price=cake_info["price"],
                cake_full_text=selected_cake
            )
            await message.answer(
                get_translation("cake_selected", language=language).format(
                    cake=cake_info["name"],
                    price=f"{cake_info['price']:,}"
                ),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                get_translation("please_choose_cake", language=language),
                reply_markup=cake_menu_keyboard(language=language),
                parse_mode="HTML"
            )

    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )


@router.message(StateFilter(UserStates.product_selection))
async def handle_unrecognized_input(message: Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        user_id = message.from_user.id
        language = "uz"
        state_responses = {
            UserStates.product_selection: {
                "text": get_translation('please_choose_cake', language=language),
                "keyboard": cake_menu_keyboard(language=language)
            },
        }
        response = state_responses.get(current_state, {
            "text": get_translation('main_message', language=language),
            "keyboard": main_keyboard(language=language)
        })
        
        await message.reply(
            response['text'],
            reply_markup=response['keyboard'],
            parse_mode='HTML'
        )

    except Exception as e:
        await message.reply(f'Error occured on handle_unrecognized_input handler: {e}')

@router.message()
async def fallback_handler(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        phone_number = await get_phone_number(user_id=user_id)
        if user_exists(user_id=user_id) and phone_number:
            await message.reply(get_translation('menu_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")  
            await state.set_state(UserStates.menu)
            set_user_state(user_id=user_id, state=UserStates.menu.state)

        else:
            await message.reply(get_translation('welcome_phone_request', 'uz'), reply_markup=phone_request_keyboard(language=language), parse_mode='HTML')
            await state.set_state(UserStates.phone_number)
            await set_user_state(user_id=user_id, state=UserStates.phone_number.state)          
    except Exception as e:
        await message.reply(f"Error occured on fallback_handler: {e}")