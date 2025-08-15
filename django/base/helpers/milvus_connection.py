import os
import logging
from pymilvus import MilvusClient
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MilvusConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                uri = os.environ.get("ZILLIZ_URI")
                token = os.environ.get("ZILLIZ_TOKEN")
                if not uri or not token:
                    logger.error("ZILLIZ_URI or ZILLIZ_TOKEN is not set.")
                    return None
                try:
                    cls._instance = super().__new__(cls)
                    cls._instance.client = MilvusClient(uri=uri, token=token)
                    logger.info("Milvus client initialized successfully.")
                except Exception as e:
                    logger.error(f"Failed to initialize Milvus client: {str(e)}")
                    cls._instance.client = None
            return cls._instance

    def get_client(self):
        if self.client is None:
            logger.warning("Milvus client is not available.")
        return self.client


"""
MILVUS = MilvusConnection().get_client()
"""
