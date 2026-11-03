# Plataforma de Dados Políticos do Ceará

Plataforma que coleta, trata e disponibiliza dados públicos sobre política no Ceará, com pipelines automatizados e um site que mostra o resultado e o fluxo dos dados.

## Frentes

- **Radar 184:** indicador mensal dos repasses federais aos 184 municípios do Ceará (dado estruturado).
- **RAG dos parlamentares:** busca inteligente sobre discursos e proposições dos 22 deputados federais do Ceará, com dados da API de Dados Abertos da Câmara (dado não estruturado).

## Stack

- **Python:** pipelines de ingestão e transformação
- **GitHub Actions:** agendamento e automação
- **Supabase (PostgreSQL):** armazenamento de tabelas e vetores
- **Site leve:** painel, busca e página de arquitetura

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `pipelines/radar` | ingestão e tratamento dos repasses |
| `pipelines/camara` | ingestão de discursos e proposições |
| `sql` | criação das tabelas no Supabase |
| `tests` | testes de qualidade dos dados |
| `docs` | documentação e diagrama |
| `site` | site da plataforma |

## Status

🚧 Em construção.