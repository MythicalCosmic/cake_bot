"""
Main bot entry point - FastAPI webhook mode
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from dotenv import load_dotenv

from core.config import config
from core.logging import setup_logging
from database.database import init_db, engine
from bot.handlers import register_handlers
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(
    token=config.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Register middlewares
dp.message.middleware(ThrottlingMiddleware())
dp.message.middleware(AuthMiddleware())

# Register handlers
register_handlers(dp)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    try:
        await init_db()
        logger.info("Database initialized")
        logger.info("Bot started in webhook mode")
        logger.info("Webhook endpoint available at /webhook")
        logger.info("Remember to set your webhook URL manually using Telegram Bot API")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    
    try:
        await bot.session.close()
        logger.info("Bot session closed")
    except Exception as e:
        logger.error(f"Error closing bot session: {e}")
    
    try:
        await engine.dispose()
        logger.info("Database engine disposed")
    except Exception as e:
        logger.error(f"Error disposing engine: {e}")
    
    logger.info("Resources cleaned up")


# Create FastAPI app
app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> Response:
    """Handle incoming webhook updates"""
    try:
        update = Update.model_validate(await request.json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return Response(status_code=500)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )