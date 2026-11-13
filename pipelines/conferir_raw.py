from pathlib import Path 

# PROCESSO
# 1. Resultado final: lista dos meses da raw com menos de 25 arquivos (ex.: "201601 2") e,
#    no fim, o total de meses conferidos (esperado: 154).
# 2. Entrada: arquivos em data/raw/recursos_recebidos, nomeados AAAAMM_pagina_NNNN.json
#    (ex.: 202403_pagina_0007.json).
# 3. Regra: contar quantos arquivos existem por mês; um mês com menos de 25 é suspeito,
#    porque um mês completo tem de 28 a 37 páginas.
# 4. Passos: listar os arquivos -> pegar o AAAAMM do nome -> somar 1 na contagem do mês ->
#    percorrer os meses em ordem -> imprimir os abaixo de 25 -> imprimir o total.
# 5. Ferramentas: Path.iterdir() lista os arquivos; nome[:6] pega os 6 primeiros caracteres;
#    um dicionário com .get() faz a contagem; sorted() ordena os meses; len() dá o total.
# 6. Caso de borda: pasta inexistente -> FileNotFoundError; pasta vazia -> imprime
#    "Meses conferidos: 0" (lido no código, ainda não testado).

pasta = Path(__file__).parents[1] / "data" / "raw" / "recursos_recebidos"
contagem = {}

for arquivo in pasta.iterdir(): 
    ano_mes = arquivo.name[:6] ####aqui vai separar apenas os valores númericos do nome (AAAAMM_PAGINA_PP)
    contagem[ano_mes] =  contagem.get(ano_mes, 0) + 1

for mes in sorted(contagem):
    if contagem[mes] < 25: ###“mostra os meses com menos de 25 arquivos (possível download incompleto)”
        print(mes, contagem[mes])

print("Meses conferidos:", len(contagem)) ###devolve a quantidade de chaves do dicionario

