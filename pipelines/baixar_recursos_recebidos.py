import os
import time 
import requests 
from dotenv import load_dotenv
import json 
from pathlib import Path
from datetime import date 

# PROCESSO
# 1. Resultado final: um arquivo JSON por página e por mês em data/raw/recursos_recebidos,
#    nomeado AAAAMM_pagina_NNNN.json, de jan/2014 até o mês anterior ao de hoje.
# 2. Entrada: a API do Portal da Transparência (/despesas/recursos-recebidos), o token do
#    .env e os filtros fixos UF = CE e favorecido = Administração Pública Municipal.
# 3. Regra: para cada mês, pedir página 1, 2, 3... até a API devolver uma página vazia;
#    cada página com dados vira um arquivo; páginas já baixadas são puladas.
# 4. Passos: calcular o último mês válido -> para cada ano e mês até o limite -> pedir a
#    página -> parar o script se a API der erro -> se vier vazia, encerrar o mês -> senão
#    gravar o arquivo, avançar a página e esperar 0,5 s.
# 5. Ferramentas: requests.get(..., params=...) consulta; raise_for_status() interrompe em
#    erro HTTP; Path.exists() permite retomar; json.dump(ensure_ascii=False) mantém os
#    acentos; time.sleep(0.5) evita sobrecarregar a API; comparar o par (ano, mes) com o
#    limite funciona porque o Python compara o ano primeiro; "if __name__ == '__main__'"
#    impede o download quando outro script apenas importa baixar_mes.
# 6. Caso de borda: (lido no código, não testado) mês sem dados não gera arquivo; arquivo
#    cortado por interrupção é tratado como página pronta; sem timeout nem nova tentativa;
#    token inválido deve interromper no primeiro pedido.

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