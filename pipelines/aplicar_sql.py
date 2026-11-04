###EXECUTA UM ARQUIVO SQL NO SUPABASE

'Uso python pipelines/aplicar_sql.py sql/nome_do_arquivo.sql'

import sys
from pathlib import Path

from db import conectar ##reaproveita a função feita em DB.py para conectar com o banco de dados

caminho = Path(sys.argv[1])
sql = caminho.read_text(encoding="utf-8")

with conectar() as conn:
    cursor = conn.execute(sql) ##manda o banco de dados executar o sql que está no arquivo
    if cursor.description: ##manda o sql para o banco de dados 
        for linha in cursor.fetchall():
            print(linha)

print(f"Arquivo executado{caminho}")

