from datetime import datetime

from loguru import logger


def setup_logger(log_file_name):
    log_file_path = f"logs/{log_file_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
    logger.add(log_file_path, rotation="00:00", retention="1 day",
               level="INFO", backtrace=False, diagnose=False, enqueue=False)
    return logger
