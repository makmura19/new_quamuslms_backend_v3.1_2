import os
import sys
import logging
from django.conf import settings


def setup_application():
    try:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            os.getenv("DJANGO_SETTINGS_MODULE", "core.settings"),
        )

        import django

        django.setup()

        from utils.logging_util import LoggingUtil

        app_name = "Lebakkinasih API - finance"
        LoggingUtil.configure_logging(app_name)
        logger = logging.getLogger(__name__)
        logger.info(f"APP: STARTING {app_name}")
    except ImportError as e:
        print(f"Error importing logging helper: {e}")
        sys.exit(1)


def main():
    setup_application()

    try:
        from django.core.management import execute_from_command_line

        logger = logging.getLogger(__name__)
        logger.info("Executing Django command line utility...")
        execute_from_command_line(sys.argv)
        logger.info("Django command executed successfully.")
    except ImportError as e:
        logger = logging.getLogger(__name__)
        logger.error(
            "Django import failed. Pastikan Django telah terinstal dan tersedia dalam PYTHONPATH. "
            "Apakah Anda lupa mengaktifkan virtual environment?"
        )
        logger.error(f"ImportError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
