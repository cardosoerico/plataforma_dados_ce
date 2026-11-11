CREATE TABLE IF NOT EXISTS bronze.recursos_recebidos (
    ano_mes integer,
    codigo_pessoa TEXT,
    tipo_pessoa TEXT, 
    municipio_pessoa TEXT, 
    sigla_uf_pessoa TEXT, 
    codigo_ug TEXT, 
    nome_ug TEXT, 
    codigo_orgao TEXT, 
    nome_orgao TEXT, 
    codigo_orgao_superior TEXT, 
    nome_orgao_superior TEXT, 
    valor numeric(18,2)
);

