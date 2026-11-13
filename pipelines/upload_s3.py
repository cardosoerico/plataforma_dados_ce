import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 
from pathlib import Path

load_dotenv()
cliente_s3 = boto3.client("s3") 
PASTA_RAW = Path(__file__).parents[1] / "data" / "raw"
S3_BUCKET = os.getenv("S3_BUCKET")

# PROCESSO
# 1. Resultado final: todos os arquivos JSON da raw local no S3, em
#    raw/<fonte>/ano=AAAA/<arquivo>, e um resumo: "enviados: N | pulados: M".
# 2. Entrada: data/raw/recursos_recebidos e data/raw/emendas (arquivos *.json) e as
#    variáveis do .env (credenciais da AWS e S3_BUCKET).
# 3. Regra: enviar só os arquivos cuja chave ainda não existe no bucket. Rodar de novo não
#    duplica nada (idempotência).
# 4. Passos: listar uma vez todas as chaves que já estão em raw/ -> para cada fonte e cada
#    arquivo local -> montar a chave -> se já existe, pular -> senão, enviar -> a cada 200
#    enviados, mostrar o andamento -> no fim, imprimir os totais.
# 5. Ferramentas: get_paginator("list_objects_v2") lista o bucket página por página (o S3
#    devolve no máximo 1000 por chamada); set guarda as chaves e responde "já existe?"
#    rápido; pasta.glob("*.json") lista os arquivos locais; sorted() dá ordem fixa;
#    upload_file() envia; continue pula para o próximo arquivo.
# 6. Caso de borda: o script compara só o NOME da chave, não o conteúdo. Se um arquivo local
#    mudar e mantiver o nome, não é reenviado. Pasta local inexistente: não testado.
#    Chave no desenho antigo (sem extraido_em=), substituído na Parte 3.

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
    for caminho in sorted(pasta.glob("*.json")): ##varre os arquivos JSON da pasta local
        chave = montar_chave(fonte, caminho) #define chave com os objetos que estamos trabalhando 
        if chave in existentes: #se a chave já estiver lá, 
            pulados += 1 #pula 
            continue #manda continuar
        cliente_s3.upload_file(str(caminho), S3_BUCKET, chave) #faz o upload do novo
        enviados += 1 #vê quais foram enviados 
        if enviados %200 == 0: #mostra o andamento a cada 200 arquivos enviados
            print("enviados até agora:", enviados)

print("enviados:", enviados, "| pulados: ", pulados)




#resposta = banco.list_objects_v2(Bucket=os.getenv("S3_BUCKET"), MaxKeys=5)
#chave = f"raw/emendas/ano={ano}/{caminho_emendas.name}"

#print(caminho_emendas)
#print(caminho_emendas.is_file())

#cliente_s3.upload_file(str(caminho_emendas), os.getenv("S3_BUCKET"), chave)
#print("enviado:", chave)