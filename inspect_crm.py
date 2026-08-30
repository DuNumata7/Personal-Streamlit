import gspread
import pandas as pd

gc = gspread.service_account('credenciais.json')
crm_sh = gc.open_by_key('17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI')
ws = crm_sh.sheet1
records = ws.get_all_records()
df = pd.DataFrame(records)
print("CRM rows:", len(df))
print(df.to_string())
