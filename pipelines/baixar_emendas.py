import os
import time 
import requests 
from dotenv import load_dotenv
import json 
from pathlib import Path
from datetime import date

load_dotenv()
token = os.getenv("PORTAL_TRANSPARENCIA_TOKEN")

url = "https://api.portaldatransparencia.gov.br/api-de-dados/emendas"
headers = {"chave-api-dados": token}
params = {}

pasta = Path(__file__).parents[1] / "data" / "raw" / "emendas"
pasta.mkdir(parents=True, exist_ok=True)

def baixar_ano(ano):
    params["ano"] = ano
    pagina = 1
    while True:
        nome = f"{ano}_pagina_{pagina:04d}.json"

        if (pasta / nome).exists():
            pagina += 1
            continue

        params["pagina"] = pagina
        resposta = requests.get(url, headers=headers, params=params)
        print("pagina", pagina, "status", resposta.status_code)

        resposta.raise_for_status()

        dados = resposta.json()
        print("registros:", len(dados))

        if len(dados) == 0:
            break

        with open(pasta / nome, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        pagina += 1
        time.sleep(0.5)


#for mes in range(1, 4):
#    print("=== mês", mes, "===")
#   baixar_mes(2026, mes)

#for ano in range(2014, 2027):
#   for mes in range(1, 13):
#      if ano == 2026 and mes > 10:
#            break
#        print("=== ano", ano, "mês", mes, "===")
#        baixar_mes(ano, mes)

if __name__ == "__main__":
    for ano in range(2014, date.today().year + 1): ###se colocar só o datetime, vai trazer a data de hoje ocmpleta. precisa só do .year indicando ano 
            print("=== ano", ano, "===")
            baixar_ano(ano)
