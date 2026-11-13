import json 
from pathlib import Path 
import pandas as pd

# PROCESSO
# 1. Resultado final: medidas impressas sobre as emendas de 2026 (linhas, duplicatas,
#    totais de empenhado/liquidado/pago, top 10 funções, recorte do Ceará). Nada é gravado.
# 2. Entrada: os arquivos data/raw/emendas/2026_pagina_*.json, com valores em texto
#    brasileiro (ex.: "1.200,50").
# 3. Regra: juntar todas as páginas numa tabela, converter os valores para número e olhar
#    a tabela por vários ângulos antes de decidir como modelá-la.
# 4. Passos: ler e juntar as páginas -> converter valorEmpenhado/valorLiquidado/valorPago
#    -> ver tamanho, emendas distintas e linhas repetidas -> somar os valores -> agrupar
#    por função -> filtrar destino no CE -> olhar a função "Encargos especiais".
# 5. Ferramentas: glob + sorted lê as páginas em ordem; json.load + extend junta as listas;
#    pd.DataFrame monta a tabela; str.replace(regex=False) + astype(float) converte os
#    valores; nunique() e duplicated() medem repetição; groupby(...).sum().sort_values()
#    resume; str.endswith filtra o texto.
# 6. Caso de borda: (lido no código, não testado) sem arquivos do ano, a tabela fica sem
#    colunas e a conversão falha com KeyError; localidadeDoGasto nula quebraria o filtro
#    do Ceará (usar na=False). Conversão com float, não com decimal.

pd.set_option("display.max_columns", None) ##Mostra todas as colunas
pd.options.display.float_format = "{:,.2f}".format ##mostra no formato completo, sem abreviação

PASTA = Path(__file__).parents[1] / "data" / "raw" / "emendas" 
COLUNAS_VALOR = ["valorEmpenhado", "valorLiquidado", "valorPago"]

def carregar_emendas(ano):
    todos = []
    for arquivo in sorted(PASTA.glob(f"{ano}_pagina_*.json")):
        with open(arquivo, encoding="utf-8") as f:
            todos.extend(json.load(f))
    return pd.DataFrame(todos)

def converter_valores(df):
    for coluna in COLUNAS_VALOR:
        df[coluna] = (df[coluna].str.replace(".", "", regex=False).
                      str.replace(",",".", regex=False).astype(float))
    return df

df = carregar_emendas(2026)
df = converter_valores(df)

##verificacoes basicas 
print(df.shape)
print("Linas:", len(df), "| emendas distintas", df["codigoEmenda"].nunique())
print("linhas totalmente repetidas:", df.duplicated().sum())
print(df[COLUNAS_VALOR].sum())

##Para onde o dinheiro está indo?
resumo =(
    df.groupby("funcao")["valorPago"].sum().sort_values(ascending=False).head(10)
)
print(resumo)

###Emendas com destino no Ceara

CE = df[df["localidadeDoGasto"].str.endswith(" - CE")]
print(len(CE))
print(CE["valorPago"].sum())
print(CE["localidadeDoGasto"].head(10))

encargos = df[df["funcao"] == "Encargos especiais"] ###o DF tem mais de 5k de linhas, apresenta uma tabela menor, com linhas de funcao marcadas com Encargos especiais
print(encargos.groupby("subfuncao")["valorPago"].sum().sort_values(ascending=False)) ##aqui usa valor pago porque ele vai funcionar para o ascending
print(encargos.groupby("tipoEmenda")["valorPago"].sum().sort_values(ascending=False))
print(df["localidadeDoGasto"].value_counts().head(5))
print(df["localidadeDoGasto"].sample(15, random_state=1))