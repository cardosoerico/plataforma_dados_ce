import os 
import requests
from dotenv import load_dotenv



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
} ###p informações da API --parametros 

resposta = requests.get(url, headers=headers, params=params)
print(resposta.status_code)

if resposta.status_code == 200:
    dados = resposta.json()
    print(len(dados))
    for registro in dados:
        print(registro["nomePessoa"], "|", registro["tipoPessoa"])