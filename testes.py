n, m= 5, 5 
tabuleiro = [[0 for _ in range(m)] for _ in range(n)]

def encontrar_caminho_bfs(mapa_de_cores, inicio, fim):
    # Lista de quadrados que o robô não deve entrar
    OBSTACULOS = (-1, -2)
    # Fila que armazena os caminhos a serem explorados
    fila = [[inicio]]
    # Conjunto para guardar as posições já visitadas
    visitados = {inicio}
    while fila:
        caminho_atual = fila.pop(0) 
        (r, c) = caminho_atual[-1]
        if (r, c) == fim: return caminho_atual
        # Lógica de vizinhos
        vizinhos = [
            (r - 1, c),  # Cima
            (r + 1, c),  # Baixo
            (r, c - 1),  # Direita
            (r, c + 1)   # Esquerda
        ]
        for prox_pos in vizinhos:
            prox_r, prox_c = prox_pos   
            # Verifica se o vizinho é um caminho válido
            if (0 <= prox_r < len(mapa_de_cores) and 0 <= prox_c < len(mapa_de_cores[0]) and mapa_de_cores[prox_r][prox_c] not in OBSTACULOS and prox_pos not in visitados):
                visitados.add(prox_pos)
                novo_caminho = list(caminho_atual)
                novo_caminho.append(prox_pos)
                fila.append(novo_caminho) 
    return None

def encontrar_primeiro_desconhecido(mapa):
    for r, linha_mapa in enumerate(mapa):
        for c, celula in enumerate(linha_mapa):
            if celula == 0:
                return (r, c)
    return None

def fechar_borda():
    global tabuleiro
    global n,m

    for i in range(n):
        if tabuleiro[i][0]==0: tabuleiro[i][0]=1
        if tabuleiro[i][m-1]==0: tabuleiro[i][m-1]=1

    for i in range(m):
        if tabuleiro[0][i]==0: tabuleiro[0][i]=1
        if tabuleiro[n-1][i]==0: tabuleiro[n-1][i]=1

def encontrar_desconhecido_mais_proximo(mapa_de_cores, posicao_atual):
    desconhecidos = []
    # 1. Cria uma lista de todos os alvos possíveis (células desconhecidas)
    for r, linha_mapa in enumerate(mapa_de_cores):
        for c, celula in enumerate(linha_mapa):
            if celula == 0:
                desconhecidos.append((r, c))

    # Se não há mais células desconhecidas, retorna None
    if not desconhecidos:
        return None

    melhor_alvo = None
    caminho_mais_curto = None

    # 2. Testa cada célula desconhecida para ver qual tem o caminho mais curto
    for alvo in desconhecidos:
        # Usa a função BFS que já temos para encontrar o caminho
        caminho_candidato = encontrar_caminho_bfs(mapa_de_cores, posicao_atual, alvo)

        # Se um caminho válido foi encontrado para este alvo
        if caminho_candidato:
            # Se é o primeiro caminho válido que encontramos, ou se ele é mais curto que o melhor anterior
            if caminho_mais_curto is None or len(caminho_candidato) < len(caminho_mais_curto):
                caminho_mais_curto = caminho_candidato
                melhor_alvo = alvo

    return caminho_mais_curto

tabuleiro[0][2] = 1
tabuleiro[1][4] = -2
tabuleiro[2][4] = -2

fechar_borda()
print(encontrar_desconhecido_mais_proximo(tabuleiro, (3,4)))