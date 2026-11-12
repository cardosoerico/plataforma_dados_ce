import os
import time 
import requests 
from dotenv import load_dotenv
import json 
from pathlib import Path
from datetime import date 

load_dotenv()
token = os.getenv("PORTAL_TRANSPARENCIA_TOKEN")

url = "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos"
headers = {"chave-api-dados": token}
params = {
    "uf": "CE",
    "tipoFavorecido": "Administração Pública Municipal",
}

pasta = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos"
pasta.mkdir(parents=True, exist_ok=True)

def baixar_mes(ano, mes):
    mes_ano = f"{mes:02d}/{ano}"
    params["mesAnoInicio"] = mes_ano
    params["mesAnoFim"] = mes_ano
    pagina = 1
    while True:
        nome = f"{ano}{mes:02d}_pagina_{pagina:04d}.json"

        if (pasta / nome).exists():
            pagina += 1
            continue

        params["pagina"] = pagina
        resposta = requests.get(url, headers=headers, params=params)
        print("pagina", pagina, "status", resposta.status_code)

        resposta.raise_for_status() ###quando dá erro, interrompe o script e traz a mensagem erro

        dados = resposta.json()
        print("registros:", len(dados))

        if len(dados) == 0:
            break

        with open(pasta / nome, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        pagina += 1
        time.sleep(0.5)

def mes_anterior(hoje):
    if hoje.month == 1:
        return hoje.year -1, 12
    return hoje.year, hoje.month - 1



if __name__ == "__main__":
    limite = mes_anterior(date.today())
    for ano in range(2014, limite[0] + 1):
        for mes in range(1, 13):
            if (ano, mes) > limite: break 
            print("=== ano", ano, "mês", mes, "===")
            baixar_mes(ano, mes)