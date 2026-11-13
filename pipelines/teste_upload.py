import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 
from pathlib import Path

# PROCESSO
# 1. Resultado final: o arquivo 2014_pagina_0001.json das emendas enviado ao bucket S3, e a
#    chave dele impressa ("enviado: raw/emendas/ano=2014/2014_pagina_0001.json").
# 2. Entrada: o arquivo local data/raw/emendas/2014_pagina_0001.json e as variáveis do .env
#    (credenciais da AWS e S3_BUCKET).
# 3. Regra: a chave no S3 é raw/<fonte>/ano=<AAAA>/<nome do arquivo>, com o ano tirado
#    dos 4 primeiros caracteres do nome.
# 4. Passos: carregar o .env -> criar o cliente do S3 -> montar o caminho local -> extrair o
#    ano do nome -> montar a chave -> imprimir o caminho e se o arquivo existe -> enviar ->
#    imprimir a chave.
# 5. Ferramentas: Path(__file__).parents[1] sobe até a raiz do projeto; name[:4] pega o ano;
#    f-string monta a chave; is_file() confere a existência; upload_file(arquivo, bucket,
#    chave) envia (recebe o caminho como texto, por isso o str()).
# 6. Caso de borda: arquivo local inexistente -> imprime False e o upload falha (anotar o
#    erro depois do teste abaixo). Rodar duas vezes sobrescreve o mesmo objeto, sem erro.
#    Chave no desenho antigo (sem extraido_em=), anterior à Parte 3.

load_dotenv()
cliente_s3 = boto3.client("s3") 
caminho_emendas = Path(__file__).parents[1] / "data" / "raw" / "emendas" / "2014_pagina_0001.json"
ano = caminho_emendas.name[:4]
#resposta = banco.list_objects_v2(Bucket=os.getenv("S3_BUCKET"), MaxKeys=5)
chave = f"raw/emendas/ano={ano}/{caminho_emendas.name}"

print(caminho_emendas)
print(caminho_emendas.is_file())

cliente_s3.upload_file(str(caminho_emendas), os.getenv("S3_BUCKET"), chave)
print("enviado:", chave)