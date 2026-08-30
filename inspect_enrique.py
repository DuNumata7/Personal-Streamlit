import gspread
import pandas as pd

gc = gspread.service_account(filename="credenciais.json")
try:
    sh = gc.open("Enrique 2")
    print("Spreadsheet Title:", sh.title)
    print("Worksheets:", [ws.title for ws in sh.worksheets()])
except Exception as e:
    print("Error:", e)
