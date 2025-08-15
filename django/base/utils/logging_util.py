import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from django.utils import timezone


class LoggingUtil:

    @classmethod
    def get_log_directory(cls):
        today = timezone.now()
        log_dir = os.path.join("logs", today.strftime("%Y"), today.strftime("%m"))
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    @classmethod
    def configure_logging(cls, app_name="Django App"):
        try:
            today = timezone.now()
            log_dir = cls.get_log_directory()
            log_file = os.path.join(log_dir, f"{today.strftime('%Y-%m-%d')}.txt")

            log_level = os.getenv("LOG_LEVEL", "INFO").upper()
            log_level = getattr(logging, log_level, logging.INFO)

            class JakartaFormatter(logging.Formatter):

                def formatTime(self, record, datefmt=None):
                    log_time = timezone.now()
                    return (
                        log_time.strftime(datefmt) if datefmt else log_time.isoformat()
                    )

            root_logger = logging.getLogger()
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
            )
            file_handler.setFormatter(
                JakartaFormatter(
                    fmt="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(
                JakartaFormatter(
                    fmt="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

            logging.basicConfig(
                level=log_level,
                handlers=[stream_handler],
            )

            logging.info(f"LOGGING: INITIALIZED {app_name} with Asia/Jakarta timezone")
        except Exception as e:
            print(f"Error during logging configuration: {e}")

    @staticmethod
    def get_user_log(user):
        return (
            f" [user={getattr(user, user.USERNAME_FIELD)}]"
            if user
            else "[user=anonymous]"
        )

    @staticmethod
    def get_logger(name="default"):
        return logging.getLogger(name)
