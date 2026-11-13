import os 
import requests
from dotenv import load_dotenv
import json 
from pathlib import Path

# PROCESSO
# 1. Resultado final: o código de status da resposta da API (200 = deu certo), a quantidade
#    de registros da página e, se deu certo, a página salva em
#    data/raw/recursos_recebidos/202607_pagina_0001.json.
# 2. Entrada: o token PORTAL_TRANSPARENCIA_TOKEN do .env e os filtros da consulta:
#    julho de 2026, UF = CE, favorecido = Administração Pública Municipal, página 1.
# 3. Regra: chamar o endpoint /despesas/recursos-recebidos com o token no cabeçalho
#    "chave-api-dados" e guardar a resposta só se o status for 200.
# 4. Passos: carregar o .env e ler o token -> montar URL, cabeçalho e filtros -> fazer a
#    requisição -> imprimir o status -> se 200, converter em JSON, imprimir a quantidade e
#    gravar o arquivo -> imprimir o texto da resposta.
# 5. Ferramentas: os.getenv() lê o token; requests.get(url, headers=..., params=...) faz a
#    consulta; .status_code e .json() leem a resposta; Path.mkdir(parents=True,
#    exist_ok=True) garante a pasta; json.dump(..., ensure_ascii=False, indent=2) grava o
#    arquivo mantendo os acentos.
# 6. Caso de borda: token inválido ou ausente -> status diferente de 200 e nada é gravado
#    (anotar o status real depois do teste abaixo). Atenção: o script grava na pasta da
#    raw e sobrescreve o arquivo se rodar de novo. Sem timeout na requisição.


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