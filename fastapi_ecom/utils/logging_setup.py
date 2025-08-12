from click import style

from fastapi_ecom.config.config import logger

SUCCESS = style("PASS:", fg="green", bold=True)
FAILURE = style("FAIL:", fg="red", bold=True)
WARNING = style("WARN:", fg="yellow", bold=True)
GENERAL = style("INFO:", fg="white", bold=True)
STDS = "     "

def success(message):
    logger.info(SUCCESS + STDS + style(message, fg="green", bold=True))

def failure(message):
    logger.error(FAILURE + STDS + style(message, fg="red", bold=True))

def warning(message):
    logger.warning(WARNING + STDS + style(message, fg="yellow", bold=True))

def general(message):
    logger.info(GENERAL + STDS + message)
