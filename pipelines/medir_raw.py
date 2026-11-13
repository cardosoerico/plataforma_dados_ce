from pathlib import Path 

# PROCESSO
# 1. Resultado final: para cada fonte da raw local, quantos arquivos existem e quantos MB
#    ocupam; e quantos anos (emendas) e meses (repasses) distintos há nos nomes dos arquivos,
#    com os 3 primeiros em ordem.
# 2. Entrada: as pastas data/raw/emendas (nomes AAAA_pagina_NNNN.json) e
#    data/raw/recursos_recebidos (nomes AAAAMM_pagina_NNNN.json).
# 3. Regra: contar os arquivos, somar o tamanho de cada um e extrair o período do início
#    do nome para ver quantos períodos diferentes existem.
# 4. Passos: listar os arquivos de cada pasta -> somar os tamanhos -> converter bytes em MB
#    -> imprimir -> pegar os 4 (ano) ou 6 (mês) primeiros caracteres de cada nome, sem
#    repetição -> imprimir a quantidade e os 3 primeiros.
# 5. Ferramentas: rglob("*") lista tudo, incluindo subpastas; is_file() descarta pastas;
#    stat().st_size dá o tamanho em bytes; 1024**2 converte bytes em MB; as chaves {...}
#    com "for" criam um conjunto (set), que elimina repetições; sorted() ordena.
# 6. Caso de borda: pasta inexistente (não testado: pode devolver zero arquivos em vez de
#    erro; testar e anotar o resultado).

PASTA_EMENDAS = Path(__file__).parents[1] / "data" / "raw" / "emendas" 
PASTA_RECURSOS = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos" 

arquivos_emendas = [a for a in PASTA_EMENDAS.rglob("*") if a.is_file()]
total_bytes = sum(a.stat().st_size for a in arquivos_emendas)
print(f"emendas: {len(arquivos_emendas), total_bytes / 1024**2}")

arquivos_recursos = [a for a in PASTA_RECURSOS.rglob("*") if a.is_file()]
total_bytes = sum(a.stat().st_size for a in arquivos_recursos)
print(f"recursos: {len(arquivos_recursos), total_bytes / 1024**2}")

anos_arquivos_emendas = {a.name[:4] for a in PASTA_EMENDAS.glob("*json")}
print(len(anos_arquivos_emendas), sorted(anos_arquivos_emendas)[:3])

meses_arquivos_recursos = {a.name[:6] for a in PASTA_RECURSOS.glob("*json")}
print(len(meses_arquivos_recursos), sorted(meses_arquivos_recursos)[:3])