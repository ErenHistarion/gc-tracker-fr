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
- A Google account with access to Google Sheets.
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
format:
```bash
black --preview .
```
lint:
```bash
black --check .
```
