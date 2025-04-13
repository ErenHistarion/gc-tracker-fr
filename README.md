# GC Tracker

GC Tracker is a tool designed to monitor the availability and prices of graphics cards across various online retail websites. It extracts product information and records it in a PostgreSQL database for easy tracking and analysis.

## Features

- **Monitoring**: Track the availability and prices of graphics cards.
- **Multi-Source Data Extraction**: Extract data from multiple retail websites.
- **Database Integration**: Automatically record information in a PostgreSQL database or Google Sheets.
- **Notifications**: Send Discord notifications for restock and price drop alerts.
- **Dynamic Web Rendering**: Use `playwright` for rendering dynamic web pages when `requests` is insufficient.
- **Concurrent Requests**: Manage concurrent requests for increased efficiency.

## Prerequisites

Before installing the project, ensure you have the following:
- Python 3.x installed on your machine.
- [uv](https://github.com/astral-sh/uv) Python package manager
- A Discord [Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- A [PostgreSQL](https://www.postgresql.org/) database
- (Optional) A [Google Service Account](https://console.cloud.google.com/projectselector2/iam-admin/serviceaccounts) with an active API key for Google Sheets integration.

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

# Run the retrieve project
uv run main.py

# Run the User Interface
streamlit run streamlit.py
```

By completing these steps, you'll ensure your environment is properly configured and ready for development.

## Dev
format:
```bash
black --preview .
```

## TODO
- **Add PCComponentes**: Integrate PCComponentes as a new source for product data.
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
- https://www.topachat.com

### Partialy compatible
- https://www.amazon.fr         # Issue detecting price when there is no stock
- https://www.amazon.de         # Issue detecting price when there is no stock
- https://www.amazon.es         # Issue detecting price when there is no stock
- https://www.amazon.it         # Issue detecting price when there is no stock
- https://www.beo-france.fr     # Issue detecting price
- https://www.galaxus.fr        # Often an ERR_HTTP2_PROTOCOL_ERROR error
- https://fr-store.msi.com      # Rare false positive availability alert
- https://www.topbiz.fr         # Improve test

### Not compatible yet
- https://www.pccomponentes.fr  # Error 403

### License
This project is licensed under the MIT License.