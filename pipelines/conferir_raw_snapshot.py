import json 
from pathlib import Path


def contagem_por_periodo(fonte): 
    pasta = Path(__file__).parents[1] / "data" / "raw" / fonte
    contagem = {}
    for arquivo in sorted(pasta.glob("*_pagina_*.json")):
        mes = arquivo.name.split("_pagina_")[0]
        registros = json.loads(arquivo.read_text(encoding="utf-8")) #json já converte json em text
        if mes not in contagem: 
            contagem[mes] = {"paginas": 0, "registros": 0}
        contagem[mes]["paginas"] +=1
        contagem[mes]["registros"] += len(registros)
    return contagem 


if __name__ == "__main__":
    for fonte in ["recursos_recebidos", "emendas"]:
        contagem = contagem_por_periodo(fonte)
        total_paginas = sum(v["paginas"] for v in contagem.values())
        total_registros = sum(v["registros"] for v in contagem.values())
        print(fonte, len(contagem), total_paginas, total_registros)