"""
Source package initialization.
Loads environment configuration on import for backward compatibility.
"""
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

try:
    load_dotenv()
except Exception:
    logger.exception("Failed to load .env file from current working directory")
