###EXECUTA UM ARQUIVO SQL NO SUPABASE
# PROCESSO
# 1. Resultado final: o conteúdo de um arquivo .sql executado no Supabase. Se o comando
#    devolver linhas (ex.: um SELECT), elas são impressas. No fim, imprime o arquivo executado.
# 2. Entrada: o caminho de um arquivo .sql passado na linha de comando, por exemplo:
#    python pipelines/aplicar_sql.py sql/001_criar_camadas.sql
# 3. Regra: ler o texto do arquivo, mandá-lo inteiro ao banco e mostrar o resultado só
#    quando houver resultado.
# 4. Passos: pegar o caminho informado -> ler o arquivo -> conectar -> executar o SQL ->
#    se houver linhas de retorno, imprimir cada uma -> imprimir a confirmação.
# 5. Ferramentas: sys.argv[1] é o primeiro argumento depois do nome do script; Path.read_text()
#    lê o arquivo; conectar() vem do db.py; conn.execute() envia o SQL; cursor.description
#    é vazio (None) quando o comando não devolve linhas, como um CREATE; fetchall() devolve
#    as linhas; o "with" confirma as mudanças ao sair sem erro e desfaz se houver erro.
# 6. Caso de borda: sem informar o arquivo, sys.argv não tem o item 1 e dá IndexError;
#    com um arquivo que não existe, dá FileNotFoundError (lido no código, não testado).

'Uso python pipelines/aplicar_sql.py sql/nome_do_arquivo.sql'

import sys
from pathlib import Path

from db import conectar ##reaproveita a função feita em DB.py para conectar com o banco de dados

caminho = Path(sys.argv[1])
sql = caminho.read_text(encoding="utf-8")

with conectar() as conn:
    cursor = conn.execute(sql) ##se o comando devolveu linhas, mostra cada uma
    if cursor.description: ##manda o sql para o banco de dados 
        for linha in cursor.fetchall():
            print(linha)

print(f"Arquivo executado{caminho}")

