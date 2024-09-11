import gspread
from google.oauth2.service_account import Credentials
import os

# Autenticação
def authSheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_path = os.path.join(os.path.dirname(__file__), 'service-account-file.json')
    creds = Credentials.from_service_account_file(json_path, scopes=scope)
    auth = gspread.authorize(creds)
    return auth