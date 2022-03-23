from user_data import user_data
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("python-game-344621-1c97bcf83064.json", scopes) 
file = gspread.authorize(credentials)
sheet = file.open("Python_MUO_Google_Sheet")
sheet = sheet.sheet1

row = list(user_data.values())[0]
sheet.update_acell("F" + str(row), "Offline")
