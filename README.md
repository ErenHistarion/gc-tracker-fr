# GC Tracker

GC Tracker is a tool designed to monitor the availability and prices of graphics cards across various online retail websites. It scrapes product information and records it in a Google Sheets spreadsheet for easy tracking.

## Features

- Monitoring of graphics card availability and prices.
- Data extraction from multiple websites.
- Automatic recording of information in Google Sheets.
- Send Discord notification
- Use of `playwright` for rendering dynamic web pages.
- Management of concurrent requests for increased efficiency.

## Prerequisites

Before installing the project, ensure you have the following:
- Python 3.x installed on your machine.
- A [Google Service Account](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts) with an active API key to Google Sheets.
- A Discord [Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- [uv](https://github.com/astral-sh/uv) Python package manager

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ErenHistarion/gc-tracker-fr.git

# Step 1: Create and activate a virtual environment through uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Step 2: Install project dependencies
uv sync
playwright install-deps
playwright install

# Run the project
uv run main.py
```

By completing these steps, you'll ensure your environment is properly configured and ready for development.

## Dev
lint:
```bash
black --check .
```
format:
```bash
black --preview .
```

## TODO
- **Add PCComponentes**: Integrate PCComponentes as a new source for product data.
- **Save results into a database instead of overwriting a spreadsheet**: Implement a database to store results, ensuring data persistence and easier querying.
- **Improve the method of listing URLs to check (database as well?)**: Enhance URL management by storing and retrieving URLs from a database, allowing for better organization and scalability.
- **Automatically detect products in a store**: Implement a feature to automatically detect and list products available in a store, enhancing the application's functionality and ease of use.
- **Optionally generate affiliate links for content creators**: Add functionality to generate affiliate links for products, enabling content creators to earn commissions.
- **Create a user interface**: Develop a user-friendly interface to interact with the application, making it accessible to non-technical users.
- **Package everything into a Docker image**: Containerize the application using Docker to ensure consistent deployment across different environments.

## Compatible e-shops
### Compatible
- https://www.ldlc.com
- https://www.rueducommerce.fr
- https://www.materiel.net
- https://www.grosbill.com
- https://www.cybertek.fr
- https://www.1foteam.com
- https://www.1fodiscount.com   # No price when there is no stock
- https://shop.hardware.fr
- https://www.easymultimedia.fr
- https://www.topbiz.fr
- https://pcandco.fr
- https://www.pc21.fr
- https://www.caseking.de
- https://www.compumsa.eu
- https://www.cdiscount.com
- https://infomaxparis.com

### Partialy compatible
- https://www.amazon.fr         # Issue detecting price when there is no stock
- https://www.amazon.de         # Issue detecting price when there is no stock
- https://www.amazon.es         # Issue detecting price when there is no stock
- https://www.amazon.it         # Issue detecting price when there is no stock
- https://www.beo-france.fr     # Issue detecting price
- https://www.galaxus.fr        # Often an ERR_HTTP2_PROTOCOL_ERROR error
- https://fr-store.msi.com      # Rare false positive availability alert

### Not compatible yet
- https://www.pccomponentes.fr  # Error 403