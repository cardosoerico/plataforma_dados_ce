import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 

# PROCESSO
# 1. Resultado final: um número impresso. Se aparecer sem erro, a conexão com o bucket S3
#    está funcionando (credenciais, região, nome do bucket e permissão de listagem).
# 2. Entrada: as variáveis do .env: chaves de acesso da AWS, região e S3_BUCKET (nome do
#    bucket). Nada disso aparece no código.
# 3. Regra: pedir ao S3 a lista dos primeiros 5 objetos do bucket e mostrar quantos vieram.
# 4. Passos: carregar o .env -> criar o cliente do S3 -> pedir a listagem de até 5 objetos
#    -> imprimir a contagem.
# 5. Ferramentas: load_dotenv() coloca o .env no ambiente (antes de criar o cliente);
#    boto3.client("s3") cria o cliente, que acha as credenciais sozinho no ambiente;
#    list_objects_v2(Bucket=..., MaxKeys=5) lista até 5 objetos; resposta["KeyCount"] é a
#    quantidade de objetos devolvidos NESTA resposta (no máximo 5), não o total do bucket.
# 6. Caso de borda: bucket com nome errado ou sem permissão -> erro do boto3 (anotar o nome
#    do erro depois do teste abaixo).

load_dotenv()

banco = boto3.client("s3") #### s3 é o serviço da AMAZON que a gente quer conectar. sempre vai ser o serviço que conectamos entre aspas
resposta = banco.list_objects_v2(Bucket=os.getenv("S3_BUCKET"), MaxKeys=5)
print(resposta["KeyCount"])

