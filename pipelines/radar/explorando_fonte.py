"""EXPLORAÇÃO DE FONTE DE DADOS

USANDO: explorar_fonte.py + repasses_202607.csv"""

####PARA USAR>>>>>>>> python E:\dev\plataforma_dados_ce\pipelines\radar\explorando_fonte.py ( + COLUNA A SER EXPLORADA AQUI)
# PROCESSO
# 1. Resultado final: um relatório impresso sobre um CSV de repasses (tamanho, colunas,
#    municípios diferentes, funções com contagem, exemplos de valor, quantidade de
#    valores negativos). Nada é gravado.
# 2. Entrada: o caminho de um CSV de repasses, passado na linha de comando (separador ";",
#    codificação UTF-8), por exemplo repasses_202607.csv.
# 3. Regra: ler o arquivo inteiro e conferir os pontos que decidem a modelagem: o número
#    de municípios deve ser 184, o valor vem como texto brasileiro e pode ser negativo.
# 4. Passos: pegar o caminho -> ler o CSV -> contar valores que começam com "-" ->
#    imprimir tamanho e colunas -> contar municípios distintos -> contar linhas por função
#    -> mostrar 5 exemplos de valor -> imprimir os negativos.
# 5. Ferramentas: sys.argv[1] recebe o caminho; pd.read_csv(sep=..., encoding=...) lê;
#    str.startswith("-").sum() conta negativos; nunique() conta distintos;
#    value_counts() conta por categoria; head(5).tolist() mostra exemplos.
# 6. Caso de borda: (lido no código, não testado) sem argumento -> IndexError; arquivo
#    inexistente -> FileNotFoundError; separador errado -> a tabela vira uma coluna só e
#    df["valor"] dá KeyError; codificação errada -> UnicodeDecodeError ou acentos trocados.

import sys 
from pathlib import Path

import pandas as pd 

CODIFICACAO = 'utf-8'
SEPARADOR = ';'

caminho = Path(sys.argv[1])
df = pd.read_csv(caminho, sep=SEPARADOR, encoding=CODIFICACAO)
df_valor = df["valor"].str.startswith("-").sum() ##verifica se existem valores negativos na coluna valor

print(f"Tamanho: {len(df)} linhas x {len(df.columns)} colunas")
print("Colunas:")
for coluna in df.columns:
    print(f" {coluna}")

print("\nMUNICIPIOS DIFERENTES:", df["cod_municipio_siafi"].nunique()) ##valores únicos da coluna cod município (deve dar 184)

print("\nFUNCOES (area | qtd de linhas)")
print(df["funcao"].value_counts())

print("\nEXEMPLOS DE VALOR")
print(df["valor"].head(5).tolist())

print(f"\nVALORES NEGATIVOS: {df_valor}")