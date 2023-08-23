import logging

LEVEL = logging.DEBUG

logger = logging.getLogger("scraper")
logger.setLevel(LEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(LEVEL)

logger.addHandler(console_handler)