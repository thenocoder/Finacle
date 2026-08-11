import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "finacle_super_secret_key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///finacle.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"
    REPORT_FOLDER = "reports"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024