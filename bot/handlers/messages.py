"""
Message handlers
"""
from asyncio.log import logger
from logging import config
from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from utils.helpers import format_order_for_admin, get_phone_number, get_user_info, user_exists, set_user_state, add_phone_number
from core.config import get_translation, get_button_text
from bot.keyboards.reply import back_keyboard, cake_menu_keyboard, main_keyboard, phone_request_keyboard, would_image_keyboard, confirmation_keyboard
from bot.states.user import UserStates
import re
from bot.handlers.cake import CAKE_OPTIONS
from aiogram import F

router = Router()

ADMIN_ID = [6589960007, 6343843937]  

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

@router.message(lambda message: message.text == get_button_text("back", language="uz"), StateFilter(UserStates.first_name, UserStates.last_name, UserStates.time))
async def handle_central_back(message: Message, state: FSMContext):
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

@router.message(StateFilter(UserStates.menu), lambda message: message.text == get_button_text("option_2", language="uz"))
async def handle_option_2(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        await message.answer(
            get_translation("contact_info", language=language),
            parse_mode="HTML"
        )
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
                get_translation("would_like_image", language=language),
                reply_markup=would_image_keyboard(language=language),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                get_translation("please_choose_cake", language=language),
                reply_markup=cake_menu_keyboard(language=language),
                parse_mode="HTML"
            )

        await state.set_state(UserStates.would_image)
        await set_user_state(user_id=user_id, state=UserStates.would_image.state)
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(lambda message: message.text == get_button_text("yessir", language="uz"))
async def handle_would_image(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        await message.answer(
            get_translation("please_send_image", language=language),
            parse_mode="HTML"
        )
        await state.set_state(UserStates.waiting_for_image)
        await set_user_state(user_id=user_id, state=UserStates.waiting_for_image.state)
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )


@router.message(StateFilter(UserStates.waiting_for_image), F.photo)
async def handle_image_upload(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"

        photo = message.photo[-1]
        file_id = photo.file_id

        user_data = await state.get_data()
        current_price = user_data.get('cake_price', 0)
        image_price = 15000
        total_price = current_price + image_price

        await state.update_data(
            cake_image_file_id=file_id,
            image_price=image_price,
            total_price=total_price
        )
        
        await message.answer(
            get_translation("image_received", language=language),
            parse_mode="HTML"
        )
        
        await state.set_state(UserStates.first_name)
        await set_user_state(user_id=user_id, state=UserStates.first_name.state)
        
        await message.answer(
            get_translation("please_enter_first_name", language=language),
            reply_markup=back_keyboard(language=language),
            parse_mode="HTML"
        )
        
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )


@router.message(lambda message: message.text == get_button_text("nosir", language="uz"))
async def handle_no_image(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        user_data = await state.get_data()
        cake_price = user_data.get('cake_price', 0)
        await state.update_data(
            cake_image_file_id=None,
            image_price=0,
            total_price=cake_price
        )
        
        await message.answer(
            get_translation("no_image_selected", language=language),
            parse_mode="HTML"
        )
        
        await state.set_state(UserStates.first_name)
        await set_user_state(user_id=user_id, state=UserStates.first_name.state)
        
        await message.answer(
            get_translation("please_enter_first_name", language=language),
            reply_markup=back_keyboard(language=language),
            parse_mode="HTML"
        )
        
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.waiting_for_image))
async def handle_invalid_image(message: Message, state: FSMContext):
    language = "uz"
    await message.answer(
        get_translation("please_send_image", language=language),
        parse_mode="HTML"
    )

@router.message(StateFilter(UserStates.first_name))
async def handle_first_name(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        first_name = message.text.strip()
        await state.update_data(first_name=first_name)
        
        await message.answer(
            get_translation("please_enter_last_name", language=language),
            reply_markup=back_keyboard(language=language),
            parse_mode="HTML"
        )
        
        await state.set_state(UserStates.last_name)
        await set_user_state(user_id=user_id, state=UserStates.last_name.state)
        
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.last_name))
async def handle_last_name(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        last_name = message.text.strip()
        await state.update_data(last_name=last_name)
        
        await message.answer(
            get_translation("please_enter_pickup_time", language=language),
            reply_markup=back_keyboard(language=language),
            parse_mode="HTML"
        )
        
        await state.set_state(UserStates.time)
        await set_user_state(user_id=user_id, state=UserStates.time.state)
        
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.time))
async def handle_pickup_time(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        pickup_time = message.text.strip()
        await state.update_data(pickup_time=pickup_time)
        
        user_data = await state.get_data()
        
        total_price = user_data.get('total_price', user_data.get('cake_price', 0))
        
        confirmation_text = get_translation("order_confirmation", language=language).format(
            cake_name=user_data.get('cake_name', 'N/A'),
            price=f"{total_price:,}",
            image_status="✅ Bor (+15,000 so'm)" if user_data.get('cake_image_file_id') else "❌ Yo'q",
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            pickup_time=pickup_time
        )
        
        await message.answer(
            confirmation_text,
            reply_markup=confirmation_keyboard(language=language),
            parse_mode="HTML"
        )
        
        await state.set_state(UserStates.order_confirmation)
        await set_user_state(user_id=user_id, state=UserStates.order_confirmation.state)
        
    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )
@router.message(lambda message: message.text == get_translation("buttons.confirm", language="uz"), StateFilter(UserStates.order_confirmation))
async def handle_order_confirmation(message: Message, state: FSMContext, bot: Bot):
    try:
        user_id = message.from_user.id
        language = "uz"
        user_data = await state.get_data()
    
        user_info = await get_user_info(user_id)
 
        admin_message = await format_order_for_admin(user_data, user_info)

        admin_ids = ADMIN_ID
        
        for admin_id in admin_ids:
            try:
                if user_data.get('cake_image_file_id'):
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=user_data['cake_image_file_id'],
                        caption=admin_message,
                        parse_mode="HTML"
                    )
                else:
                    await bot.send_message(
                        chat_id=admin_id,
                        text=admin_message,
                        parse_mode="HTML"
                    )
            except Exception as e:
                logger.error(f"Failed to send notification to admin {admin_id}: {e}")
        
        await message.answer(
            get_translation("order_placed", language=language),
            parse_mode="HTML"
        )
        await state.clear()
        await set_user_state(user_id=user_id, state=UserStates.menu.state)
        await state.set_state(UserStates.menu)
        
        await message.answer(
            get_translation("main_message", language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"Error in order confirmation: {e}")
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )
        
@router.message(lambda message: message.text == get_translation("buttons.cancel", language="uz"), StateFilter(UserStates.order_confirmation))
async def handle_order_cancellation(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        language = "uz"
        await message.answer(
            get_translation("order_cancelled", language=language),
            parse_mode="HTML"
        )
        await state.clear()
        await set_user_state(user_id=user_id, state=UserStates.menu.state)
        await state.set_state(UserStates.menu)

        await message.answer(
            get_translation("main_message", language=language),
            reply_markup=main_keyboard(language=language),
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(
            text=f"An error occurred: {e}",
            parse_mode="HTML"
        )

@router.message(StateFilter(UserStates.product_selection, UserStates.would_image))
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
            UserStates.would_image: {
                "text": get_translation('would_like_image', language=language),
                "keyboard": would_image_keyboard(language=language)
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
        if await user_exists(user_id=user_id) and phone_number:
            await message.reply(get_translation('menu_message', language=language), reply_markup=main_keyboard(language=language), parse_mode="HTML")  
            await state.set_state(UserStates.menu)
            await set_user_state(user_id=user_id, state=UserStates.menu.state)

        else:
            await message.reply(get_translation('welcome_phone_request', 'uz'), reply_markup=phone_request_keyboard(language=language), parse_mode='HTML')
            await state.set_state(UserStates.phone_number)
            await set_user_state(user_id=user_id, state=UserStates.phone_number.state)          
    except Exception as e:
        await message.reply(f"Error occured on fallback_handler: {e}")