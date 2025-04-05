def get_selectors(url):
    if "amazon" in url:
        return {
            "name": {"tag": "span", "class": "product-title-word-break"},
            "price": {"tag": "div", "class": "corePrice_feature_div"},
            "availability": {"tag": "input", "class": "add-to-cart-button"},
        }
    elif "beo-france" in url:
        return {
            "name": {"tag": "h1", "class": "product_title"},
            "price": {"tag": "bdi", "class": None},
            "availability": {"tag": "p", "class": "in-stock"},
        }
    elif "cdiscount" in url:
        return {
            "name": {"tag": "div", "class": "c-fp-heading__title"},
            "price": {"tag": "span", "class": "DisplayPrice"},
            "availability": {"tag": "input", "class": "fpAddBsk"},
        }
    elif "cybertek" in url:
        return {
            "name": {"tag": "span", "class": "title_fiche"},
            "price": {"tag": "span", "class": "p-3x"},
            "availability": {"tag": "div", "class": "prodfiche_dispo"},
        }
    elif "easymultimedia" in url:
        return {
            "name": {"tag": "h1", "class": "namne_details"},
            "price": {"tag": "span", "class": "current-price-value"},
            "availability": {"tag": "button", "class": "add-to-cart"},
        }
    elif "grosbill" in url:
        return {
            "name": {"tag": "h1", "class": "grb_product-page__title"},
            "price": {"tag": "span", "class": "_ctl0_ContentPlaceHolder1_l_prix"},
            "availability": {
                "tag": "div",
                "class": "_ctl0_ContentPlaceHolder1_div_dispo_enligne",
            },
        }
    elif "materiel" in url:
        return {
            "name": {"tag": "h1", "class": None},
            "price": {"tag": "span", "class": "o-product__price"},
            "availability": {"tag": "span", "class": "o-availability__value"},
        }
    elif "rueducommerce" in url:
        return {
            "name": {"tag": "h1", "class": "product__title"},
            "price": {"tag": "div", "class": "price"},
            "availability": {"tag": "span", "class": "modal-stock-web"},
        }
    elif "ldlc" in url:
        return {
            "name": {"tag": "h1", "class": "product__title"},
            "price": {"tag": "div", "class": "price"},
            "availability": {"tag": "div", "class": "modal-stock-web"},
        }
    elif "topachat" in url:
        return {
            "name": {"tag": "h1", "class": "ps-main__product-title"},
            "price": {"tag": "span", "class": "offer-price__price"},
            "availability": {"tag": "div", "class": "ps-main__stock--available"},
        }
    elif "hardware" in url:
        return {
            "name": {"tag": "h1", "class": None},
            "price": {"tag": "span", "class": "prix"},
            "availability": {"tag": "div", "class": "stock"},
        }
    elif "pcandco" in url:
        return {
            "name": {"tag": "h1", "class": "product-detail-name"},
            "price": {"tag": "span", "class": "current-price-value"},
            "availability": {"tag": "div", "class": "si-product-page"},
        }
    elif "pc21" in url:
        return {
            "name": {"tag": "h1", "class": "titre_produit"},
            "price": {"tag": "span", "class": "prix_produit_ttc"},
            "availability": {"tag": "span", "class": "statut_disponible"},
        }
    elif "1fodiscount" in url:
        return {
            "name": {"tag": "h1", "class": "product-sheet_title"},
            "price": {"tag": "div", "class": "product-sheet_buybox_offer_price"},
            "availability": {"tag": "div", "class": "product-tile_stock_state"},
        }
    elif "1foteam" in url:
        return {
            "name": {"tag": "h1", "class": "product-sheet_title"},
            "price": {"tag": "div", "class": "product-sheet_buybox-line_price"},
            "availability": {"tag": "div", "class": "product-sheet_stock-resume"},
        }
    elif "pccomponentes" in url:
        return {
            "name": {"tag": "h1", "class": "pdp-title"},
            "price": {"tag": "div", "class": "pdp-price-current-integer"},
            "availability": {"tag": "p", "class": "notify-description"},
        }
    elif "caseking" in url:
        return {
            "name": {"tag": "h1", "class": "product-name"},
            "price": {"tag": "span", "class": "js-unit-price"},
            "availability": {"tag": "div", "class": "product-availability"},
        }
    elif "compumsa" in url:
        return {
            "name": {"tag": "h1", "class": None},
            "price": {"tag": "span", "class": "ContentPlaceHolderMain_LabelPrice"},
            "availability": {
                "tag": "span",
                "class": "ContentPlaceHolderMain_LabelStock",
            },
        }
    elif "topbiz" in url:
        return {
            "name": {"tag": "h1", "class": "product-detail-name"},
            "price": {"tag": "span", "class": "current-price-value"},
            "availability": {"tag": "div", "class": "add"},
        }
    elif "galaxus" in url:
        return {
            "name": {"tag": "h1", "class": "productHeaderTitle_Title__U_0zb"},
            "price": {
                "tag": "button",
                "class": "headerProductPricing_PriceButton__Bm1Hv",
            },
            "availability": {
                "tag": "div",
                "class": "availability_styled_AvailabilityTextWrapper__vhs3S",
            },
        }
    else:
        return {
            "name": {"tag": "span", "class": "productTitle"},
            "price": {"tag": "span", "class": "a-price-whole"},
            "availability": {"tag": "p", "class": "availability"},
        }

