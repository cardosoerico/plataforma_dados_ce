import os
import time 
import requests 
from dotenv import load_dotenv
import json 
from pathlib import Path
from datetime import date

# PROCESSO
# 1. Resultado final: um arquivo JSON por página e por ano em data/raw/emendas, nomeado
#    AAAA_pagina_NNNN.json, de 2014 até o ano de hoje.
# 2. Entrada: a API do Portal da Transparência (/emendas), o token do .env e o ano. Não há
#    outros filtros no código (nem UF).
# 3. Regra: para cada ano, pedir página 1, 2, 3... até a API devolver uma página vazia;
#    cada página com dados vira um arquivo; páginas já baixadas são puladas.
# 4. Passos: para cada ano de 2014 até o atual -> pedir a página -> parar o script se a API
#    der erro -> se vier vazia, encerrar o ano -> senão gravar, avançar a página, esperar
#    0,5 s.
# 5. Ferramentas: date.today().year dá o ano atual (+1 porque range não inclui o último
#    valor); requests.get(..., params=...) consulta; raise_for_status() interrompe em erro
#    HTTP; Path.exists() permite retomar; json.dump(ensure_ascii=False) mantém os acentos;
#    time.sleep(0.5) evita sobrecarregar a API; "if __name__ == '__main__'" impede o
#    download quando outro script apenas importa baixar_ano.
# 6. Caso de borda: (lido no código, não testado) as emendas mudam durante o ano, mas uma
#    página já baixada nunca é atualizada, então rodar de novo mantém dados antigos (motivo
#    dos snapshots da Parte 3); ano sem dados não gera arquivo; arquivo cortado por
#    interrupção é tratado como pronto; sem timeout nem nova tentativa.

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
