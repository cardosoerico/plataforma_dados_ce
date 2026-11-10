import os 
import requests
from dotenv import load_dotenv
import json 
from pathlib import Path


load_dotenv()
token = os.getenv("PORTAL_TRANSPARENCIA_TOKEN") ## lê o arquivo dovenv e coloca o token a disposição

url = "https://api.portaldatransparencia.gov.br/api-de-dados/despesas/recursos-recebidos"
headers = {"chave-api-dados": token}
params = {
    "mesAnoInicio": "07/2026",
    "mesAnoFim": "07/2026",
    "uf": "CE",
    "tipoFavorecido": "Administração Pública Municipal",
    "pagina": 1,
}

resposta = requests.get(url, headers=headers, params=params)
print(resposta.status_code)

if resposta.status_code == 200:
    dados = resposta.json()
    print(len(dados))

    pasta = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos"
    pasta.mkdir(parents=True, exist_ok=True)
    with open(pasta / "202607_pagina_0001.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

print(resposta.text)