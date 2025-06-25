from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=-Axis.X)

########### VARIAVEIS ###########
n = 5 #LINHAS (QUANTO O ROBO DESCE)
m = 5 #COLUNAS (QUANTO O ROBO VAI PARA OS LADOS)
tabuleiro = [[Color.NONE for _ in range(m)] for _ in range(n)]
linha, coluna = 0, 0
direcao = 'D'
ANGULOS_DIRECAO = {'C': 0, 'D': 90, 'B': 180, 'E': 270}

########### CORES ###########
Color.MY_GRAY = Color(207, 27, 96)
Color.MY_BLACK= Color(270, 27, 27)
Color.MY_BLUE = Color(219, 85, 48)
Color.MY_YELLOW = Color(65, 42, 98)
Color.MY_RED = Color(352, 84, 87)
Color.MY_GREEN = Color(138, 49, 88)
MINHAS_CORES = (Color.WHITE, Color.MY_BLACK, Color.MY_BLUE, Color.MY_GRAY, Color.MY_YELLOW, Color.MY_RED, Color.MY_GREEN)
CORES_DE_PRIORIDADE = (Color.MY_YELLOW, Color.MY_BLUE, Color.MY_RED, Color.MY_GREEN)

########### MOTORES ###########
motorE = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
motorG = Motor(Port.B, Direction.COUNTERCLOCKWISE) #GARRA
drive_base = DriveBase(motorE, motorD, 56, 137)
drive_base.use_gyro(True)
drive_base.settings(straight_speed=100)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.D)
color_sensorE = ColorSensor(Port.C)
color_sensorL = ColorSensor(Port.A)
color_sensorE.detectable_colors(MINHAS_CORES)
color_sensorD.detectable_colors(MINHAS_CORES)
color_sensorL.detectable_colors((Color.RED, Color.GREEN))

########### FUNCOES ###########
########### IMPRIME O TABULEIRO FORMATADO ###########
def imprimeTabuleiro():
    global tabuleiro

    print("-----------------------------------------------------------------------------------------------------------------")
    for linha in tabuleiro:
        for j in range (m-1, -1, -1):
            print(linha[j], end="\t|\t")
        print()
        print("-----------------------------------------------------------------------------------------------------------------")

########### RETORNA A COR EMBAIXO DO ROBÔ (ADICIONAR SENSOR DO MEIO) ###########
def ler_cor():
    cor_e = color_sensorE.color()
    cor_d = color_sensorD.color()
   
    if cor_e == cor_d:
        return cor_e
    else: 
        drive_base.straight(5)
        cor_e = color_sensorE.color()
        cor_d = color_sensorD.color()

        for cor_prioritaria in CORES_DE_PRIORIDADE:
            if cor_e == cor_prioritaria:
                return cor_e
            if cor_d == cor_prioritaria:
                return cor_d

########### VIRA O ROBO USANDO AS DIRECOES DO TABULEIRO ###########
def virarPara(direcao_destino):
    global direcao
    if direcao == direcao_destino:
        return direcao_destino
    angulo_atual = ANGULOS_DIRECAO[direcao]
    angulo_destino = ANGULOS_DIRECAO[direcao_destino]
    angulo_giro = angulo_destino - angulo_atual  
    if angulo_giro > 180:
        angulo_giro -= 360
    elif angulo_giro < -180:
        angulo_giro += 360      
    # Executa o giro
    direcao=direcao_destino
    #print(f"Virando para: {direcao}")
    drive_base.turn(angulo_giro, then=Stop.HOLD, wait=True)
    wait(500) # Pequena pausa para estabilizar   

########### VIRA O ROBO USANDO VALORES ABSOLUTOS ###########
def viraAngulo(angulo_relativo):
    global direcao
    angulo_atual = ANGULOS_DIRECAO[direcao]
    novo_angulo_absoluto = angulo_atual + angulo_relativo
    novo_angulo_normalizado = novo_angulo_absoluto % 360
    nova_direcao_letra = None
    for d, ang in ANGULOS_DIRECAO.items():
        if ang == novo_angulo_normalizado:
            nova_direcao_letra = d
            break
    virarPara(nova_direcao_letra)

########### ANDA PELA BORDA ATÉ ENCONTRAR O AZUL OU PRETO RETORNA QTD DE QUADRADOS ###########
def andarBorda():
    drive_base.reset(0,0)
    while ler_cor()!=Color.MY_BLACK and ler_cor()!=Color.MY_BLUE:
        drive_base.straight(20, then=Stop.NONE)
    return drive_base.distance()//300

########### ALINHA O ROBO PARALELO A LINHA PRETA ###########
def alinharPreto():
    while ler_cor()!= Color.MY_BLACK:
            drive_base.drive(100, 0)
    drive_base.stop()

    while color_sensorE.reflection()<50:
        motorE.run(-30)
    motorE.stop()

    while color_sensorD.reflection()<50:
        motorD.run(-30)
    motorD.stop()
    wait(100)
    drive_base.straight(-50)

########### COMPLETA UMA DAS LATERAIS COM BRANCO (TALVEZ REDUNDANTE) ###########
def preencher_borda(linha_inicial, coluna_inicial, direcao_percurso, quadrados_percorridos):
    global tabuleiro # Acessa o tabuleiro global para modificá-lo
    r, c = linha_inicial, coluna_inicial
    # Itera por cada quadrado que o robô acabou de passar
    for _ in range(quadrados_percorridos):
        # Verifica se a célula está dentro dos limites do mapa (segurança extra)
        if 0 <= r < n and 0 <= c < m:
            if tabuleiro[r][c] == Color.NONE:
                tabuleiro[r][c] = Color.WHITE
        # Move a coordenada um passo na direção do percurso
        if direcao_percurso == 'C': r += 1
        elif direcao_percurso == 'B': r -= 1
        elif direcao_percurso == 'D': c += 1
        elif direcao_percurso == 'E': c -= 1

########### FECHA TODOS OS QUADRADOS DA BORDA QUE NÃO SEJAM AZUL/CINZA COM BRANCO ###########
def fechar_borda():
    global tabuleiro
    global n,m

    for i in range(n):
        if tabuleiro[i][0]==Color.NONE: tabuleiro[i][0]=Color.WHITE
        if tabuleiro[i][m-1]==Color.NONE: tabuleiro[i][m-1]=Color.WHITE

    for i in range(m):
        if tabuleiro[0][i]==Color.NONE: tabuleiro[0][i]=Color.WHITE
        if tabuleiro[n-1][i]==Color.NONE: tabuleiro[n-1][i]=Color.WHITE

########### RETORNA UMA LISTA COM O CAMINHO ENTRE DOIS PONTOS ###########
def encontrar_caminho_bfs(mapa_de_cores, inicio, fim):
    # Lista de quadrados que o robô não deve entrar
    OBSTACULOS = (Color.MY_YELLOW, Color.MY_BLUE)
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

########### FAZ O ROBO SEGUIR UM CAMINHO DETERMINADO ###########
def seguir_caminho(caminho_a_seguir):
    global linha, coluna, direcao

    for i in range(len(caminho_a_seguir) - 1):
        pos_atual = caminho_a_seguir[i]
        pos_proxima = caminho_a_seguir[i+1]
        
        (alvo_linha, alvo_coluna) = pos_proxima
        (atual_linha, atual_coluna) = pos_atual

        ######## VIRA O ROBO PARA A DIRECAO NECESSARIA ##########
        if alvo_linha > atual_linha:
            direcao_necessaria = 'B'  # Baixo
        elif alvo_linha < atual_linha:
            direcao_necessaria = 'C'  # Cima
        elif alvo_coluna > atual_coluna:
            direcao_necessaria = 'E'  # Aumentar a coluna = ir para Esquerda
        elif alvo_coluna < atual_coluna:
            direcao_necessaria = 'D'  # Diminuir a coluna = ir para Direita
        virarPara(direcao_necessaria)
        
        ########### FAZ O ROBO AVANCAR UMA CASA ###########
        drive_base.straight(300)

        ########### ATUALIZA A POSICAO DO ROBO ###########
        linha, coluna = pos_proxima

########### RETORNA O CAMINHO PARA O DESCONHECIDO MAIS PROXIMO DE MIM ###########
def encontrar_desconhecido_mais_proximo(mapa_de_cores, posicao_atual):
    desconhecidos = []
    # 1. Cria uma lista de todos os alvos possíveis (células desconhecidas)
    for r, linha_mapa in enumerate(mapa_de_cores):
        for c, celula in enumerate(linha_mapa):
            if celula == Color.NONE:
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

########### MAIN ###########
########### SAINDO DO CINZA ###########
while ler_cor()==Color.MY_GRAY:
    drive_base.straight(20, then=Stop.NONE)
hub.speaker.beep(500, 100)

########### ANDANDO PELA BORDA ###########
for lado in range(4):
    quadrados = andarBorda()
    ########### NA PRIMEIRA LINHA SALVAMOS A POSICAO DO CINZA ###########
    ########### ROBO CHEGOU EM 0,0 NO CANTO SUPERIOR DIREITO  ###########
    if lado==0:
        tabuleiro[0][quadrados] = Color.MY_GRAY
    ########### ATUALIZA AS POSICOES DE LINHA E COLUNA ###########
    else:
        if direcao == 'C': linha -= quadrados
        elif direcao == 'B': linha += quadrados
        elif direcao == 'D': coluna -= quadrados
        elif direcao == 'E': coluna +=quadrados    
    ########### COMPLETA OS QUADRADOS DAQUELA LINHA COM BRACO ###########
    ########### TALVEZ POSSA EXCLUIR ESSA FUNÇÃO PQ ESTA REDUNDANTE ###########
    preencher_borda(linha, coluna, direcao, quadrados)
    hub.speaker.beep(400, 100)
    ########### CASO ENCONTRE O AZUL ENCERRA A BUSCA PELA BORDA ###########
    if ler_cor() == Color.MY_BLUE:
        hub.speaker.beep(300, 100)
        drive_base.straight(-100)
        ########### SALVA A POSICAO DO AZUL ###########
        if direcao == 'C': 
            tabuleiro[linha-1][coluna] = Color.MY_BLUE
            tabuleiro[linha-2][coluna] = Color.MY_BLUE
        elif direcao == 'B':
            tabuleiro[linha+1][coluna] = Color.MY_BLUE
            tabuleiro[linha+2][coluna] = Color.MY_BLUE
        elif direcao == 'D':
            tabuleiro[linha][coluna-1] = Color.MY_BLUE
            tabuleiro[linha][coluna-2] = Color.MY_BLUE
        elif direcao == 'E':
            tabuleiro[linha][coluna+1] = Color.MY_BLUE
            tabuleiro[linha][coluna+2] = Color.MY_BLUE
        ########### COMPLETA A BORDA DE BRANCOS ###########
        fechar_borda()
        break
    else:
        alinharPreto()
        viraAngulo(90)   

imprimeTabuleiro()
print(f"ESTOU EM: {linha}, {coluna}")