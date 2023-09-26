import json
import time
import os
import datetime

from scraper.halooglasi import get_latest_with_retry
from scraper.db import check_if_exists, insert_property
from scraper.discord import send_to_discord
from scraper.logger import logger


def get_local_time():
    """
    convert current time to CEST
    """
    cest_time = datetime.datetime.now() + datetime.timedelta(hours=2)
    return cest_time.strftime("%D %H:%M:%S")


def main():
    CFG_FILE = os.environ.get("CFG_FILE", "config.json")
    # in seconds
    SLEEP_TIME = float(os.environ.get("SLEEP_TIME", 30))

    config = []
    while True:
        with open(CFG_FILE, "r") as f:
            _config = json.load(f)
            if _config != config:
                logger.info(f"New config: {_config}")
                config = _config

        for url, hook_url in config.items():
            logger.info(f"Scraping... {get_local_time()}")
            results = get_latest_with_retry(url, max_retries=5, sleep_time=SLEEP_TIME)
            for link, price, name, location in results[::-1]:
                if not check_if_exists(link):
                    insert_property(link, price, name, location)
                    logger.info(f"Inserted {name} with price {price}")
                    send_to_discord(link, price, name, location, hook_url=hook_url)
            time.sleep(SLEEP_TIME)



if __name__ == "__main__":
    main()
