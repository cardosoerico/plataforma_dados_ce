import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 
from pathlib import Path

load_dotenv()
cliente_s3 = boto3.client("s3") 
PASTA_RAW = Path(__file__).parents[1] / "data" / "raw"
S3_BUCKET = os.getenv("S3_BUCKET")


def montar_chave(fonte, caminho): #definindo uma função com duas entradas
    ano = caminho.name[:4]###caminho nesse caso é um parametro: "caminho.name[:X]"
    return f"raw/{fonte}/ano={ano}/{caminho.name}" #devolve o texto da chave

            
def listar_chaves(prefixo):  ###serve para listar aqueles que já estão inclusos no bloco, e evitar que sejam duplicados.
    chaves = set() ###junta todas as chaves encontradas
    paginador = cliente_s3.get_paginator("list_objects_v2") ##cria o paginador
    for pagina in paginador.paginate(Bucket=S3_BUCKET, Prefix=prefixo): ###vai gerando uma página de cada vez
        for objeto in pagina.get("Contents", []): ##vai passando item por item
            chaves.add(objeto["Key"]) ##guarda o nome completo do arquivo
    return chaves #devolve o conjunto

existentes = listar_chaves("raw/")
enviados = 0 
pulados = 0

for fonte in ["recursos_recebidos", "emendas"]:
    pasta = PASTA_RAW / fonte
    for caminho in sorted(pasta.glob("*.json")): ##varre o que já está no bucket
        chave = montar_chave(fonte, caminho) #define chave com os objetos que estamos trabalhando 
        if chave in existentes: #se a chave já estiver lá, 
            pulados += 1 #pula 
            continue #manda continuar
        cliente_s3.upload_file(str(caminho), S3_BUCKET, chave) #faz o upload do novo
        enviados += 1 #vê quais foram enviados 
        if enviados %200 == 0: #se der 200% do que tem lá (ou seja, duplicados), zera o novo
            print("enviados até agora:", enviados)

print("enviados:", enviados, "| pulados: ", pulados)




#resposta = banco.list_objects_v2(Bucket=os.getenv("S3_BUCKET"), MaxKeys=5)
#chave = f"raw/emendas/ano={ano}/{caminho_emendas.name}"

#print(caminho_emendas)
#print(caminho_emendas.is_file())

#cliente_s3.upload_file(str(caminho_emendas), os.getenv("S3_BUCKET"), chave)
#print("enviado:", chave)