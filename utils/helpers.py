from database.database import get_session
from database.models.user import User
from datetime import datetime


def format_user_mention(user_id: int, name: str) -> str:
    """Format user mention for HTML"""
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def user_exists(user_id: int) -> bool:
    """Check if a user exists in the database"""
    async for session in get_session():
        result = await session.get(User, user_id)
        return result is not None
    return False


async def add_user(
    user_id: int,
    first_name: str,
    last_name: str | None = None,
    username: str | None = None,
):
    """Add a user to the database"""
    async for session in get_session():
        user = User(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        session.add(user)
        await session.commit()


async def set_user_state(user_id: int, state: str):
    """Set the state of a user"""
    async for session in get_session():
        user = await session.get(User, user_id)
        if user:
            user.state = state
            await session.commit()


async def get_user_state(user_id: int) -> str | None:
    """Get the state of a user"""
    async for session in get_session():
        user = await session.get(User, user_id)
        if user:
            return user.state
    return None


async def add_phone_number(user_id: int, phone_number: str):
    """Add or update the phone number of a user"""
    async for session in get_session():
        user = await session.get(User, user_id)
        if user:
            user.phone_number = phone_number
            await session.commit()

async def get_phone_number(user_id: int) -> str | None:
    """Get the phone number of a user"""
    async for session in get_session():
        user = await session.get(User, user_id)
        if user:
            return user.phone_number
    return None


async def get_user_info(user_id: int) -> dict | None:
    """Get user information"""
    async for session in get_session():
        user = await session.get(User, user_id)
        if user:
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'phone_number': user.phone_number
            }
    return None


async def format_order_for_admin(user_data: dict, user_info: dict) -> str:
    """Format order details for admin notification"""
    
    user_mention = f'<a href="tg://user?id={user_info["id"]}">{user_info["first_name"]}</a>'
    
    total_price = user_data.get('total_price', user_data.get('cake_price', 0))
    cake_price = user_data.get('cake_price', 0)
    image_price = user_data.get('image_price', 0)
    
    price_breakdown = f"{cake_price:,} so'm"
    if image_price > 0:
        price_breakdown += f" + {image_price:,} so'm (rasm)"
    
    order_text = f"""
🆕 <b>YANGI BUYURTMA!</b>

👤 <b>Mijoz:</b>
├ Ism: {user_data.get('first_name', 'N/A')} {user_data.get('last_name', 'N/A')}
├ Telegram: {user_mention}
├ Username: @{user_info.get('username', 'N/A')}
└ Telefon: <code>{user_info.get('phone_number', 'N/A')}</code>

🎂 <b>Buyurtma tafsilotlari:</b>
├ Tort: {user_data.get('cake_name', 'N/A')}
├ Narx: {price_breakdown}
├ <b>JAMI: {total_price:,} so'm</b>
├ Rasm: {'✅ Bor' if user_data.get('cake_image_file_id') else '❌ Yo\'q'}
└ Olib ketish: {user_data.get('pickup_time', 'N/A')}

⏰ <b>Buyurtma vaqti:</b> {datetime.now().strftime('%d.%m.%Y, %H:%M')}
"""
    
    return order_text.strip()