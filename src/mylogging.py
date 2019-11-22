import logging
import os


def get_logger_level():
    return os.environ.get("LOGGER_LEVEL", "DEBUG")

# Remove all setup done by aws
root_logger = logging.getLogger()
for h in root_logger.handlers:
    root_logger.removeHandler(h)


def get_logger():
    logger = logging.getLogger("fr.xebia")
    logger.setLevel(get_logger_level())

    # Remove all setup done by aws
    for h in logger.handlers:
        logger.removeHandler(h)

    handler_string = logging.StreamHandler()
    handler_string.setFormatter(
        logging.Formatter('[%(asctime)s | %(levelname)5s | %(filename)s.%(funcName)s#%(lineno)d] %(message)s'))
    logger.addHandler(handler_string)

    return logger