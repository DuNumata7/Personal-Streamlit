import gspread

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws = sh.worksheet("Treino")

print("=== CELL MATRIX IN TREINO TAB ===")
for r in range(1, 35):
    row_vals = ws.row_values(r)
    print(f"L{r:02d}: {row_vals}")
