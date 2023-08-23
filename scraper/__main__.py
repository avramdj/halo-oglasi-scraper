import json
import time
import os

from scraper.halooglasi import get_latest
from scraper.db import check_if_exists, insert_property
from scraper.discord import send_to_discord
from scraper.logger import logger

if __name__ == "__main__":
        
    HALOOGLASI_URLS_FILE = os.environ.get("HALOOGLASI_URLS_FILE")
    SLEEP_TIME = float(os.environ.get("SLEEP_TIME"))

    urls = []
    while True:

        with open(HALOOGLASI_URLS_FILE, "r") as f:
            _urls = json.load(f)
            if _urls != urls:
                logger.info(f"New urls: {_urls}")
                urls = _urls

        for url in urls:
            logger.info(f"Scraping...")
            results = get_latest(url)
            for link, price, name, location in results[::-1]:
                if not check_if_exists(link):
                    insert_property(link, price, name, location)
                    logger.info(f"Inserted {name} with price {price}")
                    send_to_discord(link, price, name, location)
                else:
                    logger.info(f"Already exists: {name} with price {price}")
            time.sleep(SLEEP_TIME)
