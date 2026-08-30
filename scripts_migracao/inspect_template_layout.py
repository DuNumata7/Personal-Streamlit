import gspread

gc = gspread.service_account('credenciais.json')
sh_temp = gc.open_by_key("1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE")
ws_t = sh_temp.worksheet("Treino")
vals = ws_t.get_all_values()

with open("template_treino_layout.txt", "w", encoding="utf-8") as f:
    for idx, r in enumerate(vals[:35]):
        f.write(f"Row {idx:2d}: " + " | ".join([str(x) if x else "" for x in r]) + "\n")

print("Saved template_treino_layout.txt")
