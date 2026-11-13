###CONEXÃO COM SUPABASE 
# PROCESSO
# 1. Resultado final: uma função conectar() que devolve uma conexão aberta com o banco do
#    Supabase. Rodado direto, o arquivo imprime "Conexão OK" e a versão do PostgreSQL.
# 2. Entrada: a variável SUPABASE_DB_URL no arquivo .env (a URL de conexão; o .env fica só
#    na máquina, fora do GitHub).
# 3. Regra: ler a URL do ambiente, nunca escrita no código; se não existir, parar com
#    erro; se existir, conectar.
# 4. Passos: carregar o .env -> ler a variável -> checar se existe -> abrir a conexão.
#    Teste (só quando rodado direto): executar SELECT version() e imprimir o resultado.
# 5. Ferramentas: load_dotenv() carrega o .env; os.getenv() lê a variável; psycopg.connect()
#    abre a conexão; "with" fecha a conexão ao sair do bloco; execute().fetchone() roda a
#    consulta e pega a primeira linha.
# 6. Caso de borda: sem SUPABASE_DB_URL no .env, levanta RuntimeError com a mensagem
#    "SUPABASE_DB_URL não encontrado no arquivo .env" (lido no código, ainda não testado).

import os 

import psycopg 
from dotenv import load_dotenv 

load_dotenv()

def conectar():
    ##usa o env para conectar com o banco de dados
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        raise RuntimeError("SUPABASE_DB_URL não encontrado no arquivo .env")
    return psycopg.connect(url)

if __name__ == "__main__":
    with conectar() as conn:
        versao = conn.execute("SELECT version();").fetchone()[0]
        print("Conexão OK")
        print(versao)


