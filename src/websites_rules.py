from urllib.parse import urlparse

SELECTORS = {
    "pccomponentes": {
        "name": {"tag": "h1", "class": "pdp-title"},
        "price": {"tag": "div", "class": "pdp-price-current-integer"},
        "availability": {"tag": "p", "class": "notify-description"},
    },
    "amazon": {
        "name": {"tag": "span", "class": "product-title-word-break"},
        "price": {"tag": "div", "class": "corePrice_feature_div"},
        "availability": {"tag": "input", "class": "add-to-cart-button"},
    },
    "beo-france": {
        "name": {"tag": "h1", "class": "product_title"},
        "price": {"tag": "bdi", "class": None},
        "availability": {"tag": "p", "class": "in-stock"},
    },
    "cdiscount": {
        "name": {"tag": "div", "class": "c-fp-heading__title"},
        "price": {"tag": "span", "class": "DisplayPrice"},
        "availability": {"tag": "input", "class": "fpAddBsk"},
    },
    "cybertek": {
        "name": {"tag": "span", "class": "title_fiche"},
        "price": {"tag": "span", "class": "p-3x"},
        "availability": {"tag": "div", "class": "prodfiche_dispo"},
    },
    "easymultimedia": {
        "name": {"tag": "h1", "class": "namne_details"},
        "price": {"tag": "span", "class": "current-price-value"},
        "availability": {"tag": "button", "class": "add-to-cart"},
    },
    "grosbill": {
        "name": {"tag": "h1", "class": "grb_product-page__title"},
        "price": {"tag": "span", "class": "_ctl0_ContentPlaceHolder1_l_prix"},
        "availability": {
            "tag": "div",
            "class": "_ctl0_ContentPlaceHolder1_div_dispo_enligne",
        },
    },
    "materiel.net": {
        "name": {"tag": "h1", "class": None},
        "price": {"tag": "span", "class": "o-product__price"},
        "availability": {"tag": "span", "class": "o-availability__value"},
    },
    "rueducommerce": {
        "name": {"tag": "h1", "class": "product__title"},
        "price": {"tag": "div", "class": "price"},
        "availability": {"tag": "span", "class": "modal-stock-web"},
    },
    "ldlc": {
        "name": {"tag": "h1", "class": "product__title"},
        "price": {"tag": "div", "class": "price"},
        "availability": {"tag": "div", "class": "modal-stock-web"},
    },
    "topachat": {
        "name": {"tag": "h1", "class": "ps-main__product-title"},
        "price": {"tag": "span", "class": "offer-price__price"},
        "availability": {"tag": "span", "class": "ps-add-cart__label"},
    },
    "hardware.fr": {
        "name": {"tag": "h1", "class": None},
        "price": {"tag": "span", "class": "prix"},
        "availability": {"tag": "div", "class": "stock"},
    },
    "pcandco": {
        "name": {"tag": "h1", "class": "product-detail-name"},
        "price": {"tag": "span", "class": "current-price-value"},
        "availability": {"tag": "div", "class": "si-product-page"},
    },
    "pc21": {
        "name": {"tag": "h1", "class": "titre_produit"},
        "price": {"tag": "span", "class": "prix_produit_ttc"},
        "availability": {"tag": "span", "class": "statut_disponible"},
    },
    "1fodiscount": {
        "name": {"tag": "h1", "class": "product-sheet_title"},
        "price": {"tag": "div", "class": "product-sheet_buybox_offer_price"},
        "availability": {"tag": "div", "class": "product-tile_stock_state"},
    },
    "1foteam": {
        "name": {"tag": "h1", "class": "product-sheet_title"},
        "price": {"tag": "div", "class": "product-sheet_buybox-line_price"},
        "availability": {"tag": "div", "class": "product-sheet_stock-resume"},
    },
    "caseking.de": {
        "name": {"tag": "h1", "class": "product-name"},
        "price": {"tag": "span", "class": "js-unit-price"},
        "availability": {"tag": "div", "class": "product-availability"},
    },
    "compumsa.eu": {
        "name": {"tag": "h1", "class": None},
        "price": {"tag": "span", "class": "ContentPlaceHolderMain_LabelPrice"},
        "availability": {
            "tag": "span",
            "class": "ContentPlaceHolderMain_LabelStock",
        },
    },
    "topbiz": {
        "name": {"tag": "h1", "class": "product-detail-name"},
        "price": {"tag": "span", "class": "current-price-value"},
        "availability": {"tag": "div", "class": "add"},
    },
    "galaxus": {
        "name": {"tag": "h1", "class": "productHeaderTitle_Title__U_0zb"},
        "price": {
            "tag": "button",
            "class": "headerProductPricing_PriceButton__Bm1Hv",
        },
        "availability": {
            "tag": "div",
            "class": "availability_styled_AvailabilityTextWrapper__vhs3S",
        },
    },
    "infomaxparis": {
        "name": {"tag": "h1", "class": "page-heading"},
        "price": {"tag": "span", "class": "product-price"},
        "availability": {"tag": "span", "class": "product-availability"},
    },
    "fr-store.msi.com": {
        "name": {"tag": "h1", "class": "product-title"},
        "price": {"tag": "div", "class": "price__default"},
        "availability": {"tag": "div", "class": "product-info__add-button"},
    },
}

DEFAULT_SELECTORS = {
    "name": {"tag": "h1", "class": "title"},
    "price": {"tag": "div", "class": "price"},
    "availability": {"tag": "span", "class": "availability"},
}


def get_selectors(url):
    domain = urlparse(url).netloc
    for key in SELECTORS:
        if key in domain:
            return SELECTORS[key]
    return DEFAULT_SELECTORS
