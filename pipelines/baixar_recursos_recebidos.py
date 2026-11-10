import os
import time 
import requests 
from dotenv import load_dotenv
import json 
from pathlib import Path

load_dotenv()
token = os.getenv("PORTAL_TRANSPARENCIA_TOKEN")

url = "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos"
headers = {"chave-api-dados": token}
params = {"mesAnoInicio": "07/2026",
    "mesAnoFim": "07/2026",
    "uf": "CE",
    "tipoFavorecido": "Administração Pública Municipal",
}

pasta = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos"
pasta.mkdir(parents=True, exist_ok=True)

pagina = 1
while True:
    params["pagina"] = pagina
    resposta = requests.get(url, headers=headers, params=params)
    print("pagina", pagina, "status", resposta.status_code)

    if resposta.status_code != 200:
        break

    dados = resposta.json()
    print("registros:", len(dados))

    if len(dados) == 0:
        break

    nome = f"202607_pagina_{pagina:04d}.json"
    with open(pasta / nome, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    pagina += 1
    time.sleep(0.5)
