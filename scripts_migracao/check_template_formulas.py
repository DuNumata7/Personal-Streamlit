import gspread

gc = gspread.service_account('credenciais.json')
sh_temp = gc.open_by_key("1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE")
ws_t = sh_temp.worksheet("Treino")
formulas = ws_t.get_all_values(value_render_option='FORMULA')

print("=== TEMPLATE FORMULAS IN TREINO TAB ===")
for idx, r in enumerate(formulas[:35]):
    row_f = [str(x) for x in r if str(x).startswith('=')]
    if row_f:
        print(f"Row {idx+1}: {row_f}")
