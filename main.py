import concurrent.futures
import time
from datetime import datetime
import random

import yaml
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import playwright_stealth

from src.utils import (
    RUPTURE,
    DISPONIBLE,
    CONFIRMER,
    clean_price,
    clean_availability,
    get_random_user_agent,
)
from src.spreadsheet import get_existing_rows, add_to_spreadsheet, spreadsheet
from src.discord import send_discord_notification
from src.websites_rules import get_selectors
from src.logger import get_logger

logger = get_logger(__name__)

# Google Spreadsheet Access
sheets = {
    # "Tests": spreadsheet.worksheet("Tests"),
    "5080": spreadsheet.worksheet("5080"),
    "5070Ti": spreadsheet.worksheet("5070Ti"),
}

# Constants
MAX_THREADS = 3  ## 3 default value


def fetch_product_info(url):
    try:
        # logger.debug(f"Fetching data from {url}, using requests")
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        validated_price = None
        if response.status_code in [200, 202]:
            soup = BeautifulSoup(response.content, "html.parser")
            product_data = extract_data(url, soup)
            # logger.debug(f"Found with requests:{product_data}")
            validated_price = clean_price(product_data["price"])
            # logger.debug(f"validated_price: {validated_price}")
            if (
                not product_data["name"] and not product_data["price"]
            ) or validated_price is None:
                # logger.debug(f"Data not found using requests, trying Playwright for {url}")
                return fetch_with_playwright(url)
            return product_data
        else:
            return fetch_with_playwright(url)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            # logger.error(f"Error fetching data from {url}: {http_err}")
            logger.warning(f"Trying Playwright for {url}")
            product_data = fetch_with_playwright(url)
        else:
            logger.error(f"Error fetching data from {url}: {http_err}")
            product_data = {"url": url, "error": str(http_err)}
        if not product_data["name"] and not product_data["price"]:
            product_data["error"] = str(http_err)
        return product_data
    except Exception as err:
        logger.error(f"Error fetching data from {url}: {err}")
        return {"url": url, "error": str(err)}


def extract_data(url, soup):
    selectors = get_selectors(url)
    name = (
        soup.find(selectors["name"]["tag"], id=selectors["name"]["class"])
        or soup.find(selectors["name"]["tag"], class_=selectors["name"]["class"])
        or soup.find(selectors["name"]["tag"])
    )
    price = soup.find(
        selectors["price"]["tag"], id=selectors["price"]["class"]
    ) or soup.find(selectors["price"]["tag"], class_=selectors["price"]["class"])
    if not price:
        price = price or soup.find(selectors["price"]["tag"])
    availability = soup.find(
        selectors["availability"]["tag"], id=selectors["availability"]["class"]
    ) or soup.find(
        selectors["availability"]["tag"], class_=selectors["availability"]["class"]
    )

    return {
        "name": name.get_text(strip=True) if name else None,
        "price": price.get_text(strip=True) if price else None,
        "availability": availability.get_text(strip=True) if availability else None,
        "url": url,
    }


def fetch_with_playwright(url):
    selectors = get_selectors(url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=get_random_user_agent(),
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        playwright_stealth.stealth_sync(page)
        page.goto(url, timeout=20000)
        time.sleep(5)

        name = (
            page.query_selector(
                f"{selectors['name']['tag']}.{selectors['name']['class']}"
            )
            or page.query_selector(f"#{selectors['name']['class']}")
            or page.query_selector(selectors["name"]["tag"])
        )
        price = page.query_selector(
            f"{selectors['price']['tag']}.{selectors['price']['class']}"
        ) or page.query_selector(f"#{selectors['price']['class']}")
        availability = page.query_selector(
            f"{selectors['availability']['tag']}.{selectors['availability']['class']}"
        ) or page.query_selector(f"#{selectors['availability']['class']}")

        product_data = {
            "name": name.text_content().strip() if name else None,
            "price": price.text_content().strip() if price else None,
            "availability": (
                availability.text_content().strip() or availability.input_value()
                if availability
                else None
            ),
            "url": url,
        }
        # logger.debug(f"Found with Playwright:{product_data}")
        browser.close()
        return product_data


def main():
    with open("./src/config/urls.yml", "r") as file:
        configs = yaml.safe_load(file)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            for gc in configs:
                futures = []
                current_sheet = sheets[str(gc)]
                existing_entries = get_existing_rows(current_sheet)
                for config in configs[gc]:
                    for urls in config.values():
                        for url in urls:
                            futures.append(executor.submit(fetch_product_info, url))
                # logger.debug(f"{len(futures)} urls to check for {gc}")

                for future in concurrent.futures.as_completed(futures):
                    try:
                        product_data = future.result()
                        if "error" not in product_data:
                            # logger.debug(f"Data retrieved: {product_data}")
                            clean_availability_v = clean_availability(
                                product_data["availability"]
                            )
                            clean_price_v = clean_price(
                                product_data["price"], product_data["url"]
                            )

                            if clean_availability_v == DISPONIBLE:
                                message = f"🚨 {product_data['name']} available at {clean_price_v}€ on {product_data['url']}."
                                
                                key = (product_data["name"], product_data["url"])
                                if key not in existing_entries:
                                    logger.info(f"🚨 NEW {message}")
                                    send_discord_notification(f"🚨 NEW {message}")
                                else:
                                    current_line = current_sheet.row_values(
                                        existing_entries[key]
                                    )
                                    if current_line[2] == RUPTURE:
                                        logger.info(f"🚨 RESTOCK {message}")
                                        send_discord_notification(f"🚨 RESTOCK {message}")
                                    if float(current_line[3]) > float(clean_price_v):
                                        logger.info(f"🚨 PRICE DROP {message}")
                                        send_discord_notification(f"🚨 PRICE DROP {message}")

                            add_to_spreadsheet(
                                existing_entries=existing_entries,
                                sheet=current_sheet,
                                url=product_data["url"],
                                name=product_data["name"],
                                price=clean_price_v,
                                availability=clean_availability_v,
                            )
                        else:
                            logger.error(f"Missing data retrieved: {product_data}")
                            add_to_spreadsheet(
                                existing_entries=existing_entries,
                                sheet=current_sheet,
                                url=product_data["url"],
                                availability=CONFIRMER,
                                error=product_data["error"],
                            )
                    except Exception as err:
                        logger.error(f"Error processing {future}: {err}")

            logger.debug(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            logger.debug(f"Waiting for the next loop...")
            logger.debug(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            time.sleep(random.randint(550, 650))


if __name__ == "__main__":
    main()
