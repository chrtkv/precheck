import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
"https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('precheck-5c5daf9891d6.json', SCOPES)

file = gspread.authorize(credentials) # authenticate with Google
sheet = file.open("test") # open sheet

worksheet = sheet.get_worksheet(0)
worksheet.update_acell('C1', 'Lovejodz')
#print(worksheet.get_all_values())