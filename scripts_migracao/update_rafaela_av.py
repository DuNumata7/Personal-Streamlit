import gspread

gc = gspread.service_account('credenciais.json')
sh = gc.open_by_key("1_0oUGZmxd4nfoRQHu5bZG1jpbyZ-lub46Zj6OjUTyzk")
ws_av = sh.worksheet("Avaliações Transpostas")

headers = ws_av.row_values(1)

row_data = ["1", "31/01/2023"] + [""] * (len(headers) - 2)

for idx, h in enumerate(headers):
    h_up = h.upper()
    if h_up == "AVALIAÇÃO" or h_up == "AVALIAO":
        row_data[idx] = "1"
    elif "DATA" in h_up:
        row_data[idx] = "31/01/2023"
    elif "MASSA CORPORAL" in h_up:
        row_data[idx] = "98"
    elif "GORDURA" in h_up and "%" in h_up:
        row_data[idx] = "28.5"
    elif "ESQUEL" in h_up:
        row_data[idx] = "26.0"
    elif "CINTURA" in h_up:
        row_data[idx] = "78"

ws_av.update(range_name="A2", values=[row_data])
print("Updated Avaliações Transpostas successfully!")
