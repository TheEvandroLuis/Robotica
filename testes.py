vermelhos=[]
verde=[]
amarelos=[]
azul=[]
gray=[]

def encontrar_caminho_bfs(mapa_de_cores, inicio, fim):
    OBSTACULOS = (-1, -2)

    # Verificações de segurança para os pontos de início e fim
    if not (0 <= inicio[0] < len(mapa_de_cores) and 0 <= inicio[1] < len(mapa_de_cores[0])):
        print(f"Erro: Ponto de partida {inicio} está fora do mapa.")
        return None
    if not (0 <= fim[0] < len(mapa_de_cores) and 0 <= fim[1] < len(mapa_de_cores[0])):
        print(f"Erro: Ponto de destino {fim} está fora do mapa.")
        return None
    fila = [[inicio]]
    visitados = {inicio}

    while fila:
        caminho_atual = fila.pop(0) 
        (r, c) = caminho_atual[-1]

        if (r, c) == fim:
            return caminho_atual

        # Lógica de vizinhos (adaptada para o seu sistema de coordenadas)
        vizinhos = [
            (r - 1, c),  # Cima
            (r + 1, c),  # Baixo
            (r, c - 1),  # Direita
            (r, c + 1)   # Esquerda
        ]

        for prox_pos in vizinhos:
            prox_r, prox_c = prox_pos
            
            ### A MUDANÇA ESTÁ AQUI ###
            # Verifica se o vizinho é um caminho válido
            if (0 <= prox_r < len(mapa_de_cores) and 0 <= prox_c < len(mapa_de_cores[0]) and
                    mapa_de_cores[prox_r][prox_c] not in OBSTACULOS and  # Não pode ser amarelo NEM azul
                    prox_pos not in visitados):
                
                visitados.add(prox_pos)
                novo_caminho = list(caminho_atual)
                novo_caminho.append(prox_pos)
                fila.append(novo_caminho) 
    
    return None


def imprimeTabuleiro():
    global tabuleiro

    print("-----------------------------------------------------------------------------------------------------------------")
    for linha in tabuleiro:
        for j in range (m-1, -1, -1):
            print(linha[j], end="\t|\t")
        print()
        print("-----------------------------------------------------------------------------------------------------------------")

def encontrar_caminho_otimizado(mapa_de_cores, inicio, fim, penalidade_curva=10):
    """
    Encontra o caminho de menor custo entre dois pontos, penalizando curvas.
    Esta versão usa apenas listas padrão do Python, sem a biblioteca heapq.
    """
    OBSTACULOS = (-1, -2)
    total_linhas, total_colunas = len(mapa_de_cores), len(mapa_de_cores[0])

    # A "fila de prioridade" agora é uma lista simples.
    # Armazena tuplas de: (custo, posição, caminho_lista)
    fila = [(0, inicio, [inicio])]
    
    # Dicionário para guardar o menor custo já encontrado para cada célula
    custos = {inicio: 0}

    while fila:
        # --- MUDANÇA PRINCIPAL: ENCONTRAR O MENOR CUSTO MANUALMENTE ---
        # 1. Encontra o índice do item com o menor custo na lista 'fila'
        menor_custo_encontrado = float('inf')
        indice_do_menor = -1
        for i, (custo, pos, caminho) in enumerate(fila):
            if custo < menor_custo_encontrado:
                menor_custo_encontrado = custo
                indice_do_menor = i
        
        # 2. Remove esse item de menor custo da lista para processá-lo
        custo_atual, pos_atual, caminho_atual = fila.pop(indice_do_menor)
        # ----------------------------------------------------------------

        if custo_atual > custos[pos_atual]:
            continue

        if pos_atual == fim:
            return caminho_atual

        direcao_anterior = None
        if len(caminho_atual) > 1:
            (r_anterior, c_anterior), (r_atual, c_atual) = caminho_atual[-2], pos_atual
            if r_atual > r_anterior: direcao_anterior = 'B'
            elif r_atual < r_anterior: direcao_anterior = 'C'
            elif c_atual > c_anterior: direcao_anterior = 'E'
            elif c_atual < c_anterior: direcao_anterior = 'D'

        (r, c) = pos_atual
        vizinhos = [(r - 1, c, 'C'), (r + 1, c, 'B'), (r, c - 1, 'D'), (r, c + 1, 'E')]

        for prox_r, prox_c, direcao_nova in vizinhos:
            prox_pos = (prox_r, prox_c)
            
            if (0 <= prox_r < total_linhas and 0 <= prox_c < total_colunas and
                    mapa_de_cores[prox_r][prox_c] not in OBSTACULOS):
                
                custo_movimento = 1
                if direcao_anterior and direcao_anterior != direcao_nova:
                    custo_movimento += penalidade_curva

                novo_custo_total = custo_atual + custo_movimento

                if prox_pos not in custos or novo_custo_total < custos[prox_pos]:
                    custos[prox_pos] = novo_custo_total
                    novo_caminho = caminho_atual + [prox_pos]
                    # Adiciona o novo caminho na lista. Não precisa de heappush.
                    fila.append((novo_custo_total, prox_pos, novo_caminho))

    return None

n, m= 5, 5 
tabuleiro = [[1 for _ in range(m)] for _ in range(n)]
tabuleiro[0][2] = 0
tabuleiro[3][4] = -2
tabuleiro[2][4] = -2
tabuleiro[1][3] = 2
tabuleiro[3][3] = 2
tabuleiro[3][1] = 2
tabuleiro[1][1] = 3
tabuleiro[2][2] = -1
posicao_atual=(4,4)
caminho = encontrar_caminho_bfs(tabuleiro,posicao_atual, (3,1))
print(caminho)
caminho = encontrar_caminho_otimizado(tabuleiro, posicao_atual, (3,1), 20)
print(caminho)