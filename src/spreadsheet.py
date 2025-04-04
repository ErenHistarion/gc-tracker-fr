import gspread                                                      # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials  # pip install oauth2client

SHEET_KEY = "***"
CREDENTIALS_PATH = "***"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SHEET_KEY)

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