# GC Tracker

GC Tracker is a tool designed to monitor the availability and prices of graphics cards across various online retail websites. It scrapes product information and records it in a Google Sheets spreadsheet for easy tracking.

## Features

- Monitoring of graphics card availability and prices.
- Data extraction from multiple websites.
- Automatic recording of information in Google Sheets.
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

## Compatible e-shop
### Fully compatible
- https://www.ldlc.com
- https://www.rueducommerce.fr
- https://www.materiel.net
- https://www.grosbill.com
- https://www.cybertek.fr
- https://www.1foteam.com
- https://shop.hardware.fr
- https://www.easymultimedia.fr
- https://pcandco.fr
- https://www.pc21.fr
- https://www.caseking.de
- https://www.compumsa.eu

### Partialy compatible
- https://www.amazon.fr
- https://www.amazon.de
- https://www.amazon.es
- https://www.amazon.it
- https://www.cdiscount.com
- https://www.1fodiscount.com
- https://www.beo-france.fr

### Not compatible yet
- https://www.pccomponentes.fr