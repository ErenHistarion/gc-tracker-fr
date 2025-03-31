import concurrent.futures
import time
import re
from datetime import datetime

import yaml                                                         # pip install pyyaml
import gspread                                                      # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials  # pip install oauth2client
import requests                                                     # pip install requests
from bs4 import BeautifulSoup                                       # pip install beautifulsoup4
from playwright.sync_api import sync_playwright                     # pip install playwright | playwright install-deps | playwright install
import playwright_stealth                                           # pip install playwright-stealth setuptools 

# Google Spreadsheet Access
SHEET_KEY = "***"
CREDENTIALS_PATH = "***"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_KEY)
sheets = {
    "5080": spreadsheet.worksheet("5080"),
    "5070Ti": spreadsheet.worksheet("5070Ti"),
}

# Constants
MAX_THREADS = 3 ## 3 default value
RUPTURE = "RUPTURE"
DISPONIBLE = "DISPONIBLE"
CONFIRMER = "DEBUG"

def log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

def clean_price(raw_price):
    if not raw_price:
        return None
    cleaned_price = re.sub(r'[^0-9.,€]', '', raw_price)
    cleaned_price = cleaned_price.replace(',', '.')
    cleaned_price = cleaned_price.replace('€', '.')
    cleaned_price = cleaned_price.replace(' ', '')
    cleaned_price = cleaned_price.strip(".")
    if cleaned_price.count('.') > 1:
        cleaned_price = cleaned_price.replace('.', '', cleaned_price.count('.') - 1)

    if len(cleaned_price) > 2:
        return f"{float(cleaned_price):.2f}"
    else:
        return None

def clean_availability(raw_availability):
    if not raw_availability:
        return RUPTURE
    raw_availability = raw_availability.lower()
    
    rupture_keywords = {"rupture", "indisponible", "sur commande", "attente", "Nicht verfügbar"}
    disponible_keywords = {"disponible", "stock", "ajouter au panier", "dernière pièce", "jours", "auf lager"}
    
    if any(keyword in raw_availability for keyword in rupture_keywords):
        return RUPTURE
    if any(keyword in raw_availability for keyword in disponible_keywords):
        return DISPONIBLE
    else:
        return RUPTURE

def get_existing_rows(sheet):
    rows = sheet.get_all_values()
    existing_entries = {}
    for i, row in enumerate(rows[1:], start=2):
        if len(row) >= 2:
            key = (row[0], row[1]) 
            existing_entries[key] = i
    return existing_entries

def add_to_spreadsheet(existing_entries, sheet, url=None, name=None, availability=None, price=None, error=None):
    if not name:
        name = "NAME NOT FOUND, CHECK MANUALLY"
    key = (name, url)
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if key not in existing_entries:
            sheet.append_row([name, url, availability, price, current_time, error])
            existing_entries[key] = len(existing_entries) + 2
        else:
            row_index = existing_entries[key]
            sheet.update_cell(row_index, 5, current_time)
            if availability:
                sheet.update_cell(row_index, 3, availability)
            if price:
                sheet.update_cell(row_index, 4, price)
            if error:
                sheet.update_cell(row_index, 6, error)
    except gspread.exceptions.APIError as err:  # Beware the 'Write requests per minute per user' of service 'sheets.googleapis.com': https://developers.google.com/workspace/sheets/api/limits
        time.sleep(3)
        add_to_spreadsheet(existing_entries, sheet, url, name, availability, price, error)
    except Exception as err:
        pass

def get_selectors(url):
    if 'amazon' in url:
        return {
            'name': {'tag': 'span', 'class': 'product-title-word-break'},
            'price': {'tag': 'span', 'class': 'a-price-whole'},
            'availability': {'tag': 'div', 'class': 'submit.add-to-cart-announce'}
        }
    elif 'beo-france' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product_title'},
            'price': {'tag': 'bdi', 'class': None},
            'availability': {'tag': 'p', 'class': 'in-stock'}
        }
    elif 'cdiscount' in url:
        return {
            'name': {'tag': 'div', 'class': 'c-fp-heading__title'},
            'price': {'tag': 'span', 'class': 'DisplayPrice'},
            'availability': {'tag': 'input', 'class': 'fpAddBsk'}
        }
    elif 'cybertek' in url:
        return {
            'name': {'tag': 'span', 'class': 'title_fiche'},
            'price': {'tag': 'span', 'class': 'p-3x'},
            'availability': {'tag': 'div', 'class': 'prodfiche_dispo'}
        }
    elif 'easymultimedia' in url:
        return {
            'name': {'tag': 'h1', 'class': 'namne_details'},
            'price': {'tag': 'span', 'class': 'current-price-value'},
            'availability': {'tag': 'button', 'class': 'add-to-cart'}
        }
    elif 'grosbill' in url:
        return {
            'name': {'tag': 'h1', 'class': 'grb_product-page__title'},
            'price': {'tag': 'span', 'class': '_ctl0_ContentPlaceHolder1_l_prix'},
            'availability': {'tag': 'div', 'class': '_ctl0_ContentPlaceHolder1_div_dispo_enligne'}
        }
    elif 'materiel' in url:
        return {
            'name': {'tag': 'h1', 'class': None},
            'price': {'tag': 'span', 'class': 'o-product__price'},
            'availability': {'tag': 'span', 'class': 'o-availability__value'}
        }
    elif 'rueducommerce' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product__title'},
            'price': {'tag': 'div', 'class': 'price'},
            'availability': {'tag': 'span', 'class': 'modal-stock-web'}
        }
    elif 'ldlc' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product__title'},
            'price': {'tag': 'div', 'class': 'price'},
            'availability': {'tag': 'div', 'class': 'modal-stock-web'}
        }
    elif 'topachat' in url:
        return {
            'name': {'tag': 'h1', 'class': 'ps-main__product-title'},
            'price': {'tag': 'span', 'class': 'offer-price__price'},
            'availability': {'tag': 'div', 'class': 'offer-stock__label'}
        }
    elif 'hardware' in url:
        return {
            'name': {'tag': 'h1', 'class': None},
            'price': {'tag': 'span', 'class': 'prix'},
            'availability': {'tag': 'div', 'class': 'stock'}
        }
    elif 'pcandco' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product-detail-name'},
            'price': {'tag': 'span', 'class': 'current-price-value'},
            'availability': {'tag': 'div', 'class': 'si-product-page'}
        }
    elif 'pc21' in url:
        return {
            'name': {'tag': 'h1', 'class': 'titre_produit'},
            'price': {'tag': 'span', 'class': 'prix_produit_ttc'},
            'availability': {'tag': 'span', 'class': 'statut_disponible'}
        }
    elif '1fodiscount' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product-sheet_title'},
            'price': {'tag': 'div', 'class': 'product-sheet_buybox_offer_price'},
            'availability': {'tag': 'div', 'class': 'product-tile_stock_state'}
        }
    elif '1foteam' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product-sheet_title'},
            'price': {'tag': 'div', 'class': 'product-sheet_buybox-line_price'},
            'availability': {'tag': 'div', 'class': 'product-sheet_stock-resume'}
        }
    elif 'pccomponentes' in url:
        return {
            'name': {'tag': 'h1', 'class': 'pdp-title'},
            'price': {'tag': 'div', 'class': 'pdp-price-current-integer'},
            'availability': {'tag': 'p', 'class': 'notify-description'}
        }
    elif 'caseking' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product-name'},
            'price': {'tag': 'span', 'class': 'js-unit-price'},
            'availability': {'tag': 'div', 'class': 'product-availability'}
        }
    elif 'compumsa' in url:
        return {
            'name': {'tag': 'h1', 'class': None},
            'price': {'tag': 'span', 'class': 'ContentPlaceHolderMain_LabelPrice'},
            'availability': {'tag': 'span', 'class': 'ContentPlaceHolderMain_LabelStock'}
        }
    elif 'topbiz' in url:
        return {
            'name': {'tag': 'h1', 'class': 'product-detail-name'},
            'price': {'tag': 'span', 'class': 'current-price-value'},
            'availability': {'tag': 'div', 'class': 'add'}
        }
    elif 'galaxus' in url:
        return {
            'name': {'tag': 'h1', 'class': 'productHeaderTitle_Title__U_0zb'},
            'price': {'tag': 'button', 'class': 'headerProductPricing_PriceButton__Bm1Hv'},
            'availability': {'tag': 'div', 'class': 'availability_styled_AvailabilityTextWrapper__vhs3S'}
        }
    else:
        return {
            'name': {'tag': 'span', 'class': 'productTitle'},
            'price': {'tag': 'span', 'class': 'a-price-whole'},
            'availability': {'tag': 'p', 'class': 'availability'}
        }

def fetch_product_info(url):
    try:
        log(f"Fetching data from {url}, using requests")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        validated_price = None
        if response.status_code in [200, 202]:
            soup = BeautifulSoup(response.content, 'html.parser')
            product_data = extract_data(url, soup)
            #log(f"Found with requests:{product_data}")
            validated_price = clean_price(product_data['price'])
            #log(f"validated_price: {validated_price}")
            if (not product_data['name'] and not product_data['price']) or validated_price is None:
                log(f"Data not found using requests, trying Playwright for {url}")
                return fetch_with_playwright(url)
            return product_data
        else:
            return fetch_with_playwright(url)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            log(f"🚨 Error fetching data from {url}: {http_err}")
            log(f"Trying Playwright for {url}")
            product_data = fetch_with_playwright(url)
        else:
            log(f"🚨 Error fetching data from {url}: {http_err}")
            product_data = {
                'url': url,
                'error': str(http_err)
            }
        if (not product_data['name'] and not product_data['price']):
            product_data['error'] = str(http_err)
        return product_data
    except Exception as err:
        log(f"🚨 Error fetching data from {url}: {err}")
        return {
            'url': url,
            'error': str(err)
        }

def extract_data(url, soup):
    selectors = get_selectors(url)
    name = soup.find(selectors['name']['tag'], id=selectors['name']['class']) or soup.find(selectors['name']['tag'], class_=selectors['name']['class']) or soup.find(selectors['name']['tag'])
    price = soup.find(selectors['price']['tag'], id=selectors['price']['class']) or soup.find(selectors['price']['tag'], class_=selectors['price']['class'])
    if not price:
        price = price or soup.find(selectors['price']['tag'])
    availability = soup.find(selectors['availability']['tag'], id=selectors['availability']['class']) or soup.find(selectors['availability']['tag'], class_=selectors['availability']['class'])
      
    return {
        'name': name.get_text(strip=True) if name else None,
        'price': price.get_text(strip=True) if price else None,
        'availability': availability.get_text(strip=True) if availability else None,
        'url': url,
    }

def fetch_with_playwright(url):
    selectors = get_selectors(url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        playwright_stealth.stealth_sync(page)
        page.goto(url, timeout=20000)
        time.sleep(5)

        name = page.query_selector(f"{selectors['name']['tag']}.{selectors['name']['class']}") or page.query_selector(selectors['name']['class']) or page.query_selector(selectors['name']['tag'])
        price = page.query_selector(f"{selectors['price']['tag']}.{selectors['price']['class']}") or page.query_selector(selectors['price']['class'])
        availability = page.query_selector(f"{selectors['availability']['tag']}.{selectors['availability']['class']}") or page.query_selector(selectors['availability']['class'])

        product_data = {
            'name': name.text_content().strip() if name else None,
            'price': price.text_content().strip() if price else None,
            'availability': availability.text_content().strip() if availability else None,
            'url': url,
        }
        #log(f"Found with Playwright:{product_data}")
        browser.close()
        return product_data

def main():
    with open("./src/config/urls.yml", "r") as file:
        configs = yaml.safe_load(file)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            for cg in configs:
                futures = []
                current_sheet = sheets[str(cg)]
                existing_entries = get_existing_rows(current_sheet)
                for config in configs[cg]:
                    for urls in config.values():
                        for url in urls:
                            futures.append(executor.submit(fetch_product_info, url))
                log(f"{len(futures)} urls to check for {cg}")

                for future in concurrent.futures.as_completed(futures):
                    try:
                        product_data = future.result()
                        if 'error' not in product_data:
                            log(f"Data retrieved: {product_data}")
                            add_to_spreadsheet(existing_entries=existing_entries, sheet=current_sheet, url=product_data['url'], name=product_data['name'],
                                            price=clean_price(product_data['price']), availability=clean_availability(product_data['availability']))
                        else:
                            log(f"🚨 Data retrieved: {product_data}")
                            add_to_spreadsheet(existing_entries=existing_entries, sheet=current_sheet, url=product_data['url'], availability=CONFIRMER, error=product_data['error'])
                    except Exception as err:
                        log(f"🚨 Error processing URL {futures[future]}: {err}")

            log(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            log(f"Waiting for the next loop...")
            log(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            time.sleep(600)

if __name__ == "__main__":
    main()
