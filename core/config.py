"""
Configuration management
"""
import logging
import os
from dataclasses import dataclass
from dotenv import load_dotenv
import yaml

load_dotenv()
@dataclass
class Config:
    """Bot configuration"""
    bot_token: str
    database_url: str
    admin_ids: list[int]
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot_database.db"),
            admin_ids=[int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
        )

config = Config.from_env()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LANGUAGES_FILE = os.path.join(BASE_DIR, "languages", "translations.yaml") 

with open(LANGUAGES_FILE, "r", encoding="utf-8") as file:    
    LANGUAGES = yaml.safe_load(file)

logging.info("Configuration loaded successfully")

def get_translation(key: str, language: str) -> str:
    keys = key.split(".")
    data = LANGUAGES.get(language, LANGUAGES['uz'])

    try:
        for k in keys:
            data = data[k]
        if isinstance(data, str):
            return data
    except (KeyError, TypeError):
        pass

    return f"[{language}:{key}]"

def get_button_text(button_key: str, language: str) -> str:
    return get_translation(f"buttons.{button_key}", language)