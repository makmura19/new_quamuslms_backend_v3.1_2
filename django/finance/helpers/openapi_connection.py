import os
import logging
from openai import OpenAI
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    logger.error("OPENAI_API_KEY is not set.")
                    return None
                try:
                    cls._instance = super().__new__(cls)
                    cls._instance.client = OpenAI(api_key=api_key)
                    logger.info("OpenAI client initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                    cls._instance.client = None
            return cls._instance

    def get_client(self):
        if self.client is None:
            logger.warning("OpenAI client is not available.")
        return self.client


"""
OPENAI = OpenAIConnection().get_client()
"""
