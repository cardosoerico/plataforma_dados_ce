CREATE TABLE IF NOT EXISTS bronze.repasses (
    ano_mes TEXT,
    cod_municipio_siafi TEXT,
    tipo_transferencia TEXT,
    funcao TEXT,
    subfuncao TEXT,
    cod_orgao TEXT,
    orgao TEXT,
    cod_unidade_gestora TEXT,
    unidade_gestora TEXT,
    cod_programa TEXT,
    programa TEXT,
    cod_acao TEXT,
    acao TEXT,
    linguagem_cidada TEXT,
    valor TEXT,
    csv_origem TEXT, 
    importado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

####não usada mais