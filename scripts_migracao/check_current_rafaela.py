import gspread

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws_t = sh.worksheet("Treino")
vals = ws_t.get_all_values()

with open("current_rafaela_treino.txt", "w", encoding="utf-8") as f:
    for idx, r in enumerate(vals):
        f.write(f"Row {idx+1:2d}: " + " | ".join([str(x) if x else "" for x in r]) + "\n")

print(f"Read {len(vals)} rows from Rafaela's Treino tab.")
