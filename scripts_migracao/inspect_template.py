import gspread

gc = gspread.service_account(filename="credenciais.json")
template_sh = gc.open_by_key("1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE")
print("Template title:", template_sh.title)
print("Template worksheets:")
for ws in template_sh.worksheets():
    print(f" - {ws.title} ({ws.row_count}x{ws.col_count})")
    print("   Header:", ws.row_values(1)[:10])
