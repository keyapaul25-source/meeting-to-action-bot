import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
GOOGLE_SHEETS_WORKSHEET_NAME = os.getenv("GOOGLE_SHEETS_WORKSHEET_NAME", "Tasks")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_google_credentials_path() -> str | None:
    if not GOOGLE_SHEETS_CREDENTIALS_FILE:
        return None
    path = Path(GOOGLE_SHEETS_CREDENTIALS_FILE)
    if not path.is_absolute():
        path = BASE_DIR / path
    return str(path)
