CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

COMMENT ON SCHEMA bronze IS 'Camada de ingestão de dados brutos';
COMMENT ON SCHEMA silver IS 'Camada de dados transformados e limpos, prontos para análise';
COMMENT ON SCHEMA gold IS 'Camada de dados agregados e prontos para consumo';

