from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=-Axis.X, broadcast_channel=125)

########### VARIAVEIS ###########
n = 5 #LINHAS (QUANTO O ROBO DESCE)
m = 5 #COLUNAS (QUANTO O ROBO VAI PARA OS LADOS)
tabuleiro = [[Color.NONE for _ in range(m)] for _ in range(n)]
linha, coluna = 0, 0
direcao = 'D'
ANGULOS_DIRECAO = {'C': 0, 'D': 90, 'B': 180, 'E': 270}
vermelhos=[]
verde=[]
amarelos=[]
azul=[]
gray=[]

########### CORES ###########
Color.MY_GRAY = Color(196, 34, 98)
Color.MY_BLACK= Color(195, 31, 20)
Color.MY_BLUE = Color(218, 93, 75)
Color.MY_YELLOW = Color(73, 55, 98)
Color.MY_RED = Color(354, 89, 100)
Color.MY_GREEN = Color(143, 76, 92)
MINHAS_CORES = (Color.WHITE, Color.MY_BLACK, Color.MY_BLUE, Color.MY_GRAY, Color.MY_YELLOW, Color.MY_RED, Color.MY_GREEN)
CORES_DE_PRIORIDADE = (Color.MY_YELLOW, Color.MY_BLUE, Color.MY_GREEN, Color.MY_RED)

########### MOTORES ###########
motorE = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
motorG = Motor(Port.B, Direction.COUNTERCLOCKWISE) #GARRA
drive_base = DriveBase(motorE, motorD, 56, 120)
drive_base.settings(straight_speed=130, turn_rate=50)
drive_base.use_gyro(True)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.D)
color_sensorE = ColorSensor(Port.C)
color_sensorL = ColorSensor(Port.A)
color_sensorE.detectable_colors(MINHAS_CORES)
color_sensorD.detectable_colors(MINHAS_CORES)
color_sensorL.detectable_colors(MINHAS_CORES)

########### FUNCOES ###########
########### FECHA A GARRA COM O BLOCO ###########
def fechar_garra():
    motorG.run_target(200, 200)
    wait(500)

########### ABRE A GARRA E SOLTA O BLOCO ###########
def abrir_garra():
    motorG.run_target(200, 40)
    wait(500)

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
    cor_l = color_sensorL.color()
    cor_lida = Color.NONE

    if cor_e == cor_d and cor_e==cor_l and cor_d==cor_l:
        cor_lida = cor_e
    else: 
        for cor_prioritaria in CORES_DE_PRIORIDADE:
            if cor_l == cor_prioritaria:
                cor_lida = cor_l
            if cor_e == cor_prioritaria:
                cor_lida = cor_e
            if cor_d == cor_prioritaria:
                cor_lida = cor_d

    if cor_lida == Color.MY_BLUE: hub.ble.broadcast(1)
    elif cor_lida == Color.MY_YELLOW: hub.ble.broadcast(2)
    elif cor_lida == Color.MY_RED: hub.ble.broadcast(3)
    elif cor_lida == Color.MY_GREEN: hub.ble.broadcast(4)
    elif cor_lida == Color.WHITE: hub.ble.broadcast(5)
    elif cor_lida == Color.MY_BLACK: hub.ble.broadcast(6)
    elif cor_lida == Color.MY_GRAY: hub.ble.broadcast(7)
    else: hub.ble.broadcast(-1)

    return cor_lida

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
    wait(1000) # Pequena pausa para estabilizar   

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
        drive_base.straight(10, then=Stop.NONE)
    return drive_base.distance()//300

########### ALINHA O ROBO PARALELO A LINHA PRETA ###########
def alinharPreto():
    while ler_cor()!= Color.MY_BLACK and ler_cor()!=Color.MY_BLUE:
            drive_base.drive(100, 0)
    drive_base.stop()

    while color_sensorE.reflection()<60:
        motorE.run(-50)
    motorE.stop()

    while color_sensorD.reflection()<60:
        motorD.run(-50)
    motorD.stop()
    wait(100)
    drive_base.straight(-30)

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

########### RETORNA O CAMINHO PARA O VERMELHO MAIS DISTANTE DE MIM ###########
def encontrar_vermelho_distante(vermelhos, posicao_atual):
    global tabuleiro
    # Se não há mais células desconhecidas, retorna None
    if not vermelhos:
        return None

    melhor_alvo = None
    caminho_mais_longo = None

    # 2. Testa cada célula desconhecida para ver qual tem o caminho mais curto
    for alvo in vermelhos:
        # Usa a função BFS que já temos para encontrar o caminho
        caminho_candidato = encontrar_caminho_bfs(tabuleiro, posicao_atual, alvo)

        # Se um caminho válido foi encontrado para este alvo
        if caminho_candidato:
            # Se é o primeiro caminho válido que encontramos, ou se ele é mais curto que o melhor anterior
            if caminho_mais_longo is None or len(caminho_candidato) > len(caminho_mais_longo):
                caminho_mais_longo = caminho_candidato
                melhor_alvo = alvo

    return caminho_mais_longo

########### MAPEIA O INTERIOR DO TABULEIRO ###########
def explorar_interior(caminho_a_seguir):
    global linha, coluna, direcao, tabuleiro

    # O loop vai até o penúltimo item, pois sempre olhamos para o próximo
    for i in range(len(caminho_a_seguir) - 1):
        pos_atual = caminho_a_seguir[i]
        pos_proxima = caminho_a_seguir[i+1]
        # Garante que o estado lógico do robô corresponde ao início do passo
        linha, coluna = pos_atual
        # 1. Orienta o robô na direção do próximo passo
        direcao_necessaria = direcao
        (alvo_linha, alvo_coluna) = pos_proxima
        if alvo_linha > linha: direcao_necessaria = 'B'
        elif alvo_linha < linha: direcao_necessaria = 'C'
        elif alvo_coluna > coluna: direcao_necessaria = 'E'
        elif alvo_coluna < coluna: direcao_necessaria = 'D'
        virarPara(direcao_necessaria)

        drive_base.reset(0,0)
        while drive_base.distance()<=300:
            drive_base.straight(10, then=Stop.NONE)
            if ler_cor()==Color.MY_YELLOW:
                drive_base.stop()
                drive_base.straight(-drive_base.distance())
                tabuleiro[alvo_linha][alvo_coluna]=Color.MY_YELLOW
                viraAngulo(90)
                drive_base.straight(50)
                return
            elif (ler_cor()==Color.MY_RED or ler_cor()==Color.MY_GREEN) and drive_base.distance()>99:
                drive_base.stop()
                wait(100)
                tabuleiro[alvo_linha][alvo_coluna]=ler_cor()
                drive_base.straight(150)
                break
        linha, coluna = pos_proxima
        if tabuleiro[linha][coluna]==Color.NONE: tabuleiro[linha][coluna]=Color.WHITE
    return

########### ANALISA O TABULEIRO PREENCHIDO E SALVA OS PONTOS NOTAVEIS ###########
def pontos_notaveis():
    global vermelhos, amarelos, verde, azul, gray
    for i in range(n):
        for j in range(m-1,-1,-1):
            if tabuleiro[i][j]==Color.MY_YELLOW:
                amarelos.append((i,j))
            if tabuleiro[i][j]==Color.MY_GREEN:
                verde.append((i,j))
            if tabuleiro[i][j]==Color.MY_BLUE:
                azul.append((i,j))
            if tabuleiro[i][j]==Color.MY_GRAY:
                gray.append((i,j))
            if tabuleiro[i][j]==Color.MY_RED:
                vermelhos.append((i,j))
    #print(vermelhos)
    #print(amarelos)
    #print(verde)
    #print(azul)
    #print(gray)

########### PEGA O BLOCO VERMELHO N E VOLTA PARA PONTO DE ENTRADA  ###########
def pegar_bloco_vermelho(numero):
    while ler_cor()!=Color.MY_BLUE:
        drive_base.straight(10, then=Stop.NONE)
    drive_base.straight(55)
    viraAngulo(90)
    while ler_cor()==Color.MY_BLUE:
        drive_base.straight(10, then=Stop.NONE)
    hub.speaker.beep(500, 100)
    drive_base.straight(-30)
    viraAngulo(-90)
    drive_base.straight(-70)
    #alinharPreto()
    abrir_garra()
    if numero==1:
        drive_base.straight(160)
        fechar_garra()
        drive_base.straight(-210)
    elif numero==2:
        drive_base.straight(320)
        fechar_garra()
        drive_base.straight(-370)
    else:
        drive_base.straight(480)
        fechar_garra()
        drive_base.straight(-530)
    
    viraAngulo(90)
    drive_base.straight(-50)

########### PEGA O BLOCO VERDE E PINTA AZUL DE BRANCO ###########
def pegar_bloco_verde():
    global tabuleiro, linha, coluna, direcao
    while ler_cor()!=Color.MY_BLUE:
        drive_base.straight(10, then=Stop.NONE)
    drive_base.straight(50)
    viraAngulo(-90)
    while ler_cor()!=Color.MY_BLACK:
        drive_base.straight(10, then=Stop.NONE)
    viraAngulo(90)
    
    abrir_garra()
    drive_base.straight(320)
    fechar_garra()
    drive_base.straight(-400)
    '''
    if direcao == 'C': linha = azul[1][0]
    elif direcao == 'B': linha = azul[0][0]
    elif direcao == 'D': coluna = azul[0][1]
    elif direcao == 'E': coluna = azul[1][1]  
    '''
    tabuleiro[azul[0][0]][azul[0][1]]=Color.WHITE
    tabuleiro[azul[1][0]][azul[1][1]]=Color.WHITE

########### ENTREGA O BLOCO SOBRE O CIRCULO ###########
def entregar():
    global tabuleiro, linha, coluna
    ############ VOLTA ATÉ VER A COR ##########
    while ler_cor()!= Color.MY_RED and ler_cor()!=Color.MY_GREEN:
            drive_base.drive(-100, 0)
    drive_base.stop()
    #drive_base.straight(-65)

    drive_base.reset(0,0)
    ####### CASO O SENSOR DA ESQUERDA ESTEJA FORA ##########
    while color_sensorE.color()!=Color.MY_RED and color_sensorE.color()!=Color.MY_GREEN:
        motorD.run(-100)
    motorD.stop()

    ####### CASO O SENSOR DA DIREITA ESTEJA FORA ##########
    while color_sensorD.color()!=Color.MY_RED and color_sensorD.color()!=Color.MY_GREEN:
        motorE.run(-100)
    motorE.stop()
    wait(100)

    angulo_correcao=drive_base.angle()
    ########### VAI PARA O COMEÇO DO CIRCULO PARA ENTREGA CORRETA #########
    while ler_cor()!=Color.WHITE:
        drive_base.drive(-100, 0)
    drive_base.stop()
    drive_base.straight(20)

    ############## SOLTA O BLOCO #######
    abrir_garra()
    tabuleiro[linha][coluna]=Color.MY_YELLOW
    drive_base.straight(-75)
    motorG.run_target(200, 250)
    drive_base.reset(0,0)
    drive_base.turn(-angulo_correcao)
    drive_base.straight(-100)

########### MAIN ###########
########### SOBE A GARRA PARA ANDAR ###########
motorG.run_target(200, 250)

########### SAINDO DO CINZA ###########
while ler_cor()==Color.MY_GRAY:
    drive_base.straight(20, then=Stop.NONE)
hub.speaker.beep(500, 100)

########### ANDANDO PELA BORDA ###########
for lado in range(5):
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

########### EXPLORANDO O INTERIOR ###########
ponto_entrada = (linha, coluna)
desconhecido = encontrar_desconhecido_mais_proximo(tabuleiro, ponto_entrada)
while desconhecido:
    explorar_interior(desconhecido)
    desconhecido = encontrar_desconhecido_mais_proximo(tabuleiro, (linha, coluna))
pontos_notaveis()

########## VOLTA PARA O PONTO DE ENTRADA ############
seguir_caminho(encontrar_caminho_bfs(tabuleiro, (linha, coluna), ponto_entrada))
alinharPreto()
viraAngulo(90)

imprimeTabuleiro()
drive_base.settings(straight_speed=200, turn_rate=50)

########## COLETAR E ENTREGAR OS BLOCOS VERMELHO ############
for i in range(3):
    pegar_bloco_vermelho(i+1)
    caminho= encontrar_vermelho_distante(vermelhos, ponto_entrada)
    seguir_caminho(caminho)
    entregar()
    ######### INVERTER O CAMINHO E RETIRAR A COORDENADA OCUPADA #######
    caminho = caminho[::-1]
    caminho.pop(0)
    ######### ATUALIZAR A POSICAO DO ROBO PARA A CASA ANTERIOR ##########
    linha, coluna = caminho[0]
    ######### VOLTAR AO PONTO DE ENTRADA ###################
    seguir_caminho(caminho)
    alinharPreto()
    viraAngulo(90)

########## COLETAR E ENTREGAR BLOCO VERDE ############
pegar_bloco_verde()
caminho= encontrar_caminho_bfs(tabuleiro, ponto_entrada, verde[0])
seguir_caminho(caminho)
entregar()

######### ATUALIZAR A POSICAO DO ROBO PARA A CASA ANTERIOR ##########
linha, coluna = caminho[-2]

######### VOLTAR AO GRAY ###################
seguir_caminho(encontrar_caminho_bfs(tabuleiro, (linha, coluna), gray[0]))

imprimeTabuleiro()