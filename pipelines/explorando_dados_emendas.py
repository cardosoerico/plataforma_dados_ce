import json 
from pathlib import Path 
import pandas as pd


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