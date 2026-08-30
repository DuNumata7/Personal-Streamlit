import gspread
import pandas as pd

gc = gspread.service_account('credenciais.json')
template_sh = gc.open_by_key("1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE")
ws_av = template_sh.worksheet("Avaliações Transpostas")
records = ws_av.get_all_records()
print("Template Avaliações Transpostas Columns:")
print(list(records[0].keys()) if records else ws_av.row_values(1))
