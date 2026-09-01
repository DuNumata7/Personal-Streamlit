import gspread
import pandas as pd
import re

print("Iniciando a criação das abas 'Historico_Cargas' nas planilhas dos alunos...")

# Configuração de autenticação local (usando o credenciais.json na raiz)
try:
    gc = gspread.service_account(filename="credenciais.json")
except Exception as e:
    print("Erro ao carregar credenciais.json:", e)
    exit()

# URL do CRM (público via CSV)
url_crm = "https://docs.google.com/spreadsheets/d/17dvnLi1gdz2-OIyzrILI3wtvaom14EfYrUobrAz8lhI/export?format=csv"
try:
    df_crm = pd.read_csv(url_crm)
except Exception as e:
    print("Erro ao ler o CRM:", e)
    exit()

# Função para extrair o ID
def extract_sheet_id(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", str(url))
    return match.group(1) if match else None

criadas = 0
ja_existiam = 0
erros = 0

# Iterar sobre alunos ativos
for index, row in df_crm.iterrows():
    status = str(row.get("Status", "")).strip().lower()
    if status == "ativo":
        link = row.get("Link da Planilha Individual", "")
        nome = row.get("Nome Completo", "Aluno")
        sheet_id = extract_sheet_id(link)
        
        if sheet_id:
            try:
                sh = gc.open_by_key(sheet_id)
                try:
                    # Tenta acessar para ver se já existe
                    sh.worksheet("Historico_Cargas")
                    print(f"[OK] {nome} já possui a aba 'Historico_Cargas'.")
                    ja_existiam += 1
                except gspread.exceptions.WorksheetNotFound:
                    print(f"[CRIANDO] Criando aba para {nome}...")
                    worksheet = sh.add_worksheet(title="Historico_Cargas", rows="1000", cols="5")
                    worksheet.append_row(["Data", "Exercício", "Carga (kg)", "Repetições", "Observações"])
                    worksheet.format("A1:E1", {"textFormat": {"bold": True}})
                    criadas += 1
            except Exception as e:
                print(f"[ERRO] Falha ao acessar planilha de {nome}: {e}")
                erros += 1

print("\n--- RESUMO ---")
print(f"Abas Criadas: {criadas}")
print(f"Abas que Já Existiam: {ja_existiam}")
print(f"Erros: {erros}")
print("Finalizado!")
