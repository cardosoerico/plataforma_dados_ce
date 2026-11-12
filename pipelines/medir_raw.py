from pathlib import Path 

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