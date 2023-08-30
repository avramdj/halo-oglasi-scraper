import time
from contextlib import contextmanager
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
import multiprocessing as mp

from scraper.logger import logger


@contextmanager
def autoquit_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_soup(url, driver):
    driver.get(url)
    page_source = driver.page_source
    return BeautifulSoup(page_source, "html.parser")


def get_properties(soup):
    properties = []
    ad_list_2 = soup.find("div", id="ad-list-2")
    rows = ad_list_2.find_all("div", class_="col-md-12 col-sm-12 col-xs-12 col-lg-12")

    for row in rows:
        link_element = row.find("h3", class_="product-title").find("a")
        price_element = row.find("span", {"data-value": True})
        location = row.find(class_="subtitle-places").find_all("li")
        if link_element and price_element and location:
            link = "https://www.halooglasi.com" + link_element["href"]
            link = "".join(link.split("?")[:-1])  # remove query params
            name = link_element.text.strip()
            location = " - ".join([elem.text for elem in location]).replace("\xa0", " ")
            price = float(price_element["data-value"])
            properties.append((link, price, name, location))

    return properties


def scrape(url):
    with autoquit_driver() as driver:
        soup = get_soup(url, driver)
        properties = get_properties(soup)
        return properties


def get_latest_with_retry(url, max_retries=5, sleep_time=5):
    for attempt in range(max_retries):
        try:
            return scrape(url)
        except Exception as e:
            traceback.print_exc()
            logger.warning(f"Attempt {attempt} -- An exception occurred: {e}")
            time.sleep(sleep_time)
    raise SystemExit("Reached max retries. Exiting...")