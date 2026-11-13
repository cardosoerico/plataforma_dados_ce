from pathlib import Path 

pasta = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos"
contagem = {}

for arquivo in pasta.iterdir(): 
    ano_mes = arquivo.name[:6] ####aqui vai separar apenas os valores númericos do nome (AAAAMM_PAGINA_PP)
    contagem[ano_mes] =  contagem.get(ano_mes, 0) + 1

for mes in sorted(contagem):
    if contagem[mes] < 25: ###“mostra os meses com menos de 25 arquivos (possível download incompleto)”
        print(mes, contagem[mes])

print("Meses conferidos:", len(contagem))