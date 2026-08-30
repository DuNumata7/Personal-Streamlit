import gspread
import pandas as pd

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws_treino = sh.worksheet("Treino")

# Inspect the visual Treino sheet
vals = ws_treino.get_all_values()
print(f"Total rows in Treino: {len(vals)}")
for idx, r in enumerate(vals[:35]):
    row_str = [str(x) for x in r if x.strip()]
    if row_str:
        print(f"Row {idx+1}: {row_str}")
