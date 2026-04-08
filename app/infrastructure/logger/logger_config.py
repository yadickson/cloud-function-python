import logging


def logger_config() -> logging.Logger:
    formatter = logging.Formatter(fmt="[%(levelname)5s] [%(logger_info)s] - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger("application")
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger
