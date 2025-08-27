import os
import logging
from pymongo import MongoClient
from threading import Lock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                mongo_uri = (
                    f"mongodb://{os.environ['MONGO_DB_USER']}:"
                    f"{os.environ['MONGO_DB_PASSWORD']}@"
                    f"{os.environ['MONGO_DB_HOST']}:{os.environ['MONGO_DB_PORT']}"
                )
                db_name = os.environ.get("MONGO_DB_NAME", "mydatabase")

                try:
                    cls._instance.client = MongoClient(
                        mongo_uri, serverSelectionTimeoutMS=5000
                    )
                    cls._instance.client.admin.command("ping")
                    cls._instance.db = cls._instance.client[db_name]
                    logger.info("MongoDB connection established successfully.")
                except Exception as e:
                    logger.error(f"Failed to connect to MongoDB: {str(e)}")
                    cls._instance.client = None
                    cls._instance.db = None
            return cls._instance

    def get_database(self):
        if self.db is None:
            logger.warning("Database connection is not available. Returning None.")
        return self.db

    def close(self):
        if self.client:
            try:
                self.client.close()
                logger.info("MongoDB connection closed successfully.")
            except Exception as e:
                logger.error(f"Error while closing MongoDB connection: {str(e)}")
