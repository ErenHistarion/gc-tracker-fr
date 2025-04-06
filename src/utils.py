import re
import random

from src.logger import get_logger

logger = get_logger(__name__)

RUPTURE = "RUPTURE"
DISPONIBLE = "DISPONIBLE"
CONFIRMER = "DEBUG"


def clean_price(raw_price):
    if not raw_price:
        return None
    cleaned_price = re.sub(r"[^0-9.,€]", "", raw_price)
    cleaned_price = cleaned_price.replace(",", ".")
    if len(cleaned_price) > 10:
        filtered_price = re.findall(r"(\d+(?:.\d+)?)€", cleaned_price)
        if filtered_price:
            cleaned_price = filtered_price[0]
    cleaned_price = cleaned_price.replace("€", ".")
    cleaned_price = cleaned_price.replace(" ", "")
    cleaned_price = cleaned_price.strip(".")
    if cleaned_price.count(".") > 1:
        cleaned_price = cleaned_price.replace(".", "", cleaned_price.count(".") - 1)

    if len(cleaned_price) > 2:
        return f"{float(cleaned_price):.2f}"
    else:
        return None


def clean_availability(raw_availability):
    if not raw_availability:
        return RUPTURE
    raw_availability = raw_availability.lower()

    rupture_keywords = {
        "rupture",
        "indisponible",
        "sur commande",
        "attente",
        "Nicht verfügbar",
    }
    disponible_keywords = {
        "disponible",
        "stock",
        "ajouter au panier",
        "dernière pièce",
        "jours",
        "auf lager",
    }

    if any(keyword in raw_availability for keyword in rupture_keywords):
        return RUPTURE
    if any(keyword in raw_availability for keyword in disponible_keywords):
        return DISPONIBLE
    else:
        return RUPTURE


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",  # Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.3179.54",  # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0",  # Firefox
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Safari/605.1.15",  # Safari
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/119.0.0.0",  # Opera
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/119.0.0.0"
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Vivaldi/7.3.3635.7",  # Vivaldi
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Vivaldi/7.3.3635.7",
    ]
    return random.choice(user_agents)
