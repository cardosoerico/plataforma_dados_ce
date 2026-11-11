import os 
import boto3 ##essa biblioteca traz a biblioteca da AWS 
from dotenv import load_dotenv 

load_dotenv()

banco = boto3.client("s3") #### s3 é o serviço da AMAZON que a gente quer conectar. sempre vai ser o serviço que conectamos entre aspas
resposta = banco.list_objects_v2(Bucket=os.getenv("S3_BUCKET"), MaxKeys=5)
print(resposta["KeyCount"])

