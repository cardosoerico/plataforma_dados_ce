import json 
from pathlib import Path

EXTRAIDO_EM = "2026-11-10"

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

def montar_manifesto(fonte, periodo, numeros):
    return {
        "fonte": fonte, 
        "periodo": periodo, 
        "extraido_em": EXTRAIDO_EM,
        "paginas": numeros["paginas"],
        "registros": numeros["registros"]
    }

def chave_do_manifesto(fonte, periodo):
    ano = periodo[:4]
    return f"raw/{fonte}/ano={ano}/extraido_em={EXTRAIDO_EM}/manifesto_{periodo}.json"

if __name__ == "__main__":
    print(montar_manifesto("recursos_recebidos", "202401", {"paginas": 33, "registros": 482}))
    print(chave_do_manifesto("recursos_recebidos", "202401"))
    print(chave_do_manifesto("emendas", "2026"))