"""EXPLORAÇÃO DE FONTE DE DADOS

USANDO: explorar_fonte.py + repasses_202607.csv"""

####PARA USAR>>>>>>>> python E:\dev\plataforma_dados_ce\pipelines\radar\explorando_fonte.py ( + COLUNA A SER EXPLORADA AQUI)

import sys 
from pathlib import Path

import pandas as pd 

CODIFICACAO = 'utf-8'
SEPARADOR = ';'

caminho = Path(sys.argv[1])
df = pd.read_csv(caminho, sep=SEPARADOR, encoding=CODIFICACAO)


print(f"Tamanho: {len(df)} linhas x {len(df.columns)} colunas")
print("Colunas:")
for coluna in df.columns:
    print(f" {coluna}")

print("\nMUNICIPIOS DIFERENTES:", df["cod_municipio_siafi"].nunique()) ##valores únicos da coluna cod município (deve dar 184)

print("\nFUNCOES (area | qtd de linhas)")
print(df["funcao"].value_counts())

print("\nEXEMPLOS DE VALOR")
print(df["valor"].head(5).tolist())