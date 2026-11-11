import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 
from pathlib import Path

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