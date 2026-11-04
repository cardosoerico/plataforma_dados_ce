"""EXPLORAÇÃO DE FONTE DE DADOS

USANDO: explorar_fonte.py + repasses_202607.csv"""


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