# Registro de decisões de arquitetura

Cada decisão segue o mesmo formato: contexto, decisão, alternativas descartadas e consequência. Esse tipo de documento chama-se ADR (Architecture Decision Record).

## D1. Data lake no S3 em camadas, com processamento separado do serving

- **Contexto:** o dado precisa ser reprocessável e o site precisa sobreviver ao fim dos créditos.
- **Decisão:** lake no S3 para guardar e processar; Postgres do Supabase para servir.
- **Alternativas descartadas:** (a) tudo no Supabase; (b) site consultando o Athena (c) Redshift ou RDS, que cobram por hora ligada.
- **Consequência:** há uma etapa a mais (publicar), e o Supabase passa a ter um papel único e claro: receber a camada Gold.

## D2. Raw imutável, com snapshot por data de extração e manifesto

- **Contexto:** a fonte altera dados já publicados. 
- **Decisão:** cada extração grava em `extraido_em=AAAA-MM-DD/` e termina com um arquivo de manifesto. Nada é sobrescrito.
- **Alternativa descartada:** sobrescrever os arquivos. Perde-se o histórico e a capacidade de explicar por que um número mudou.
- **Consequência:** a raw cresce cerca de 500 arquivos por mês. Em volume é desprezível (poucos megabytes).

## D3. Glue com Spark, mesmo com volume pequeno

- **Contexto:** 87 MB cabem numa função Lambda com pandas. Spark é exigido em vagas de engenharia de dados.
- **Decisão:** usar Glue 6.0 (Spark 4.1) com o mínimo de 2 workers G.1X e tempo limite de 20 minutos por job.
- **Alternativa descartada:** Lambda com pandas ou Glue Python Shell. É mais barato e mais simples, mas não cumpre o objetivo de aprendizado.
- **Consequência:** custo estimado abaixo de US$ 1 por mês. 

## D4. Reconstrução completa a cada execução, em vez de carga incremental

- **Contexto:** bronze, silver e gold poderiam processar só o que mudou.
- **Decisão:** cada job relê tudo da camada anterior e sobrescreve a sua camada inteira.
- **Alternativa descartada:** incremental com MERGE. Exige controle de estado e é a principal fonte de erros sutis em pipelines.
- **Consequência:** o job é idempotente por construção: rodar duas vezes produz o mesmo resultado. Quando o volume passar de alguns gigabytes, esta decisão deve ser revista.

## D5. Parquet com tabelas no Glue Data Catalog, sem Iceberg neste volume

- **Contexto:** formatos de tabela como Iceberg oferecem MERGE e viagem no tempo.
- **Decisão:** Parquet simples, particionado por ano.
- **Alternativa descartada:** Iceberg. Resolve problemas que a decisão D4 já evita e adiciona conceitos demais de uma vez.
- **Consequência:** Iceberg fica como evolução natural para uma versão 2.

## D6. Step Functions como orquestrador

- **Contexto:** as etapas têm ordem e dependência. O EventBridge sozinho só dispara por horário.
- **Decisão:** uma máquina de estados no Step Functions, disparada pelo EventBridge Scheduler no dia 5 de cada mês.
- **Alternativas descartadas:** (a) Airflow gerenciado (MWAA), que custa centenas de dólares por mês; (b) Glue Workflows, que não orquestra Lambda; (c) agendar cada etapa por horário e torcer para a anterior ter terminado.
- **Consequência:** o fluxo fica visível como diagrama no console, o que serve de evidência para o portfólio.

## D7. Testes de qualidade escritos no próprio código dos jobs

- **Contexto:** existem ferramentas dedicadas (Great Expectations, Glue Data Quality, dbt tests).
- **Decisão:** uma função `exigir(condicao, mensagem)` que interrompe o job quando a condição é falsa.
- **Alternativa descartada:** adotar um framework agora. Antes de usar a ferramenta, vale entender o que ela faz por baixo.
- **Consequência:** os testes ficam simples de ler. Migrar para um framework depois é direto.

## D8. Segredos no Parameter Store

- **Contexto:** na nuvem não existe arquivo `.env`.
- **Decisão:** token da API e senha do Supabase como parâmetros do tipo SecureString no Systems Manager Parameter Store.
- **Alternativa descartada:** Secrets Manager, que cobra por segredo por mês. O Parameter Store padrão não tem custo.
- **Consequência:** o código lê o segredo em tempo de execução, e a permissão de leitura é dada só à função que precisa.

## D9. Dados de referência do IBGE baixados por script manual, uma vez por ano

- **Contexto:** a lista de municípios e a população mudam, no máximo, uma vez por ano.
- **Decisão:** um script local que grava a resposta do IBGE na raw.
- **Alternativa descartada:** automatizar. O custo de construir e manter não se paga para um dado anual.
- **Consequência:** há um lembrete anual (setembro, depois da publicação das estimativas) no README.

## D10. Console primeiro, Terraform depois

- **Contexto:** recursos criados clicando não são reproduzíveis.
- **Decisão:** criar cada recurso no console para entender o que ele é, e reescrever tudo em Terraform na Parte 12.
- **Consequência:** a Parte 12 inclui a importação dos recursos já existentes.

## D11. Recorte das emendas

- **Contexto:** a API de emendas é nacional e só uma pequena parte aponta para municípios do Ceará.
- **Decisão:** a silver guarda todas as emendas. A gold mostra as que têm gasto localizado no Ceará (estado ou município), por ano, autor e função.
- **Consequência:** o recorte por autor cearense depende da lista de parlamentares e fica para o volume da Câmara.