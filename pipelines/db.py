###CONEXÃO COM SUPABASE 

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


