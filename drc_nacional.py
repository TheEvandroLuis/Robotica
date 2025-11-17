from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=Axis.Y, observe_channels=[120], broadcast_channel=125)

########### VARIAVEIS ###########
n = 5 #LINHAS (QUANTO O ROBO DESCE)
m = 6 #COLUNAS (QUANTO O ROBO VAI PARA OS LADOS)
tabuleiro = [[Color.NONE for _ in range(m)] for _ in range(n)]
linha, coluna = 0, 0
direcao = 'D'
ANGULOS_DIRECAO = {'B': 0, 'D': 270, 'C': 180, 'E': 90}
vermelhos=[]
verde=[]
amarelos=[]

########### CORES ###########
Color.MY_WHITE= Color(0, 0, 100)
Color.MY_BLACK= Color(205, 20, 36)
Color.MY_YELLOW = Color(49, 14, 100)
Color.MY_RED = Color(351, 78, 88)
Color.MY_GREEN = Color(166, 74, 74)
MINHAS_CORES = (Color.MY_YELLOW, Color.MY_RED, Color.MY_GREEN, Color.MY_WHITE, Color.MY_BLACK)
CORES_DE_PRIORIDADE = (Color.MY_YELLOW, Color.MY_RED, Color.MY_GREEN, Color.MY_WHITE, Color.MY_BLACK)

########### MOTORES ###########
motorE = Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
drive_base = DriveBase(motorE, motorD, 56, 185)
drive_base.use_gyro(True)
drive_base.settings(straight_speed=200, turn_rate=50)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.E)
color_sensorE = ColorSensor(Port.A)
color_sensorL = ColorSensor(Port.C)
color_sensorE.detectable_colors(MINHAS_CORES)
color_sensorD.detectable_colors(MINHAS_CORES)
color_sensorL.detectable_colors(MINHAS_CORES)

########### RETORNA A COR EMBAIXO DO ROBÔ ###########
def ler_cor():
    cor_e = color_sensorE.color()
    cor_d = color_sensorD.color()
    cor_l = color_sensorL.color()
    cor_lida = Color.NONE

    #print(f"D: {color_sensorE.color()} | M: {color_sensorL.color()} | E: {color_sensorD.color()}")
    if cor_e == cor_d and cor_e==cor_l and cor_d==cor_l:
        cor_lida = cor_e
    else: 
        cor_e = color_sensorE.color()
        cor_d = color_sensorD.color()
        cor_l = color_sensorL.color()
        for cor_prioritaria in CORES_DE_PRIORIDADE:
            if cor_l == cor_prioritaria:
                cor_lida = cor_l
                break
            elif cor_e == cor_prioritaria:
                cor_lida = cor_e
                break
            elif cor_d == cor_prioritaria:
                cor_lida = cor_d
                break
    
    if cor_lida == Color.MY_WHITE: hub.ble.broadcast(4)
    elif cor_lida == Color.MY_BLACK: hub.ble.broadcast(5)
    #print(cor_lida)
    return cor_lida
    
########### VIRA O ROBO USANDO AS DIRECOES DO TABULEIRO ###########
def virarPara(direcao_destino,num):
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
    drive_base.turn(angulo_giro)
    wait(500) # Pequena pausa para estabilizar
    if(num==1):
        alinharQuadrado()

########### VIRA O ROBO USANDO AS ANGULO MULTIPLOS DE 90 ###########
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
    virarPara(nova_direcao_letra,0)

########### DADO DUAS COORDENADAS ELE VIRA EM DIREÇAO AO ALVO ###############
def virarParaCoordenada (atual, alvo):
    (alvo_linha, alvo_coluna) = alvo
    (atual_linha, atual_coluna) = atual

    ######## VIRA O ROBO PARA A DIRECAO NECESSARIA ##########
    if alvo_linha > atual_linha:
        direcao_necessaria = 'C'  # Baixo
    elif alvo_linha < atual_linha:
        direcao_necessaria = 'B'  # Baixo 
    elif alvo_coluna > atual_coluna:
        direcao_necessaria = 'D'  # Aumentar a coluna = ir para Direita
    elif alvo_coluna < atual_coluna:
        direcao_necessaria = 'E'  # Diminuir a coluna = ir para Esquerda
    virarPara(direcao_necessaria,1)


def alinharVerde():
    while ler_cor()== Color.MY_GREEN:
        drive_base.drive(100, 0)
        drive_base.stop()
    while color_sensorE.color()!=Color.MY_GREEN:
        motorE.run(-50)
    motorE.stop()
    while color_sensorD.color()!=Color.MY_GREEN:
        motorD.run(-50)
    motorD.stop()
    wait(100)
    drive_base.straight(-30)
########### ALINHA O ROBO PARALELO ###########
def alinharQuadrado():
    cor_atual = ler_cor()
    if(cor_atual==Color.MY_WHITE):
        while ler_cor()!= Color.MY_BLACK:
            drive_base.drive(100, 0)
            if(ler_cor()==Color.MY_YELLOW or ler_cor()==Color.MY_GREEN):
                break
        drive_base.stop()

        while color_sensorE.reflection()<60:
            motorE.run(-50)
        motorE.stop()

        while color_sensorD.reflection()<60:
            motorD.run(-50)
        motorD.stop()
    elif (cor_atual==Color.MY_BLACK):
        while ler_cor()!= Color.MY_WHITE:
            drive_base.drive(100, 0)
        drive_base.stop()

        while color_sensorE.reflection()>60:
            motorE.run(-50)
        motorE.stop()

        while color_sensorD.reflection()>60:
            motorD.run(-50)
        motorD.stop()    
    wait(100)
    drive_base.straight(-40)

########### RETORNA UMA LISTA COM O CAMINHO ENTRE DOIS PONTOS ###########
def encontrar_caminho_bfs(mapa_de_cores, inicio, fim):
    # Lista de quadrados que o robô não deve entrar
    OBSTACULOS = (Color.MY_YELLOW)
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
            (r + 1, c),  # Cima
            (r - 1, c),  # Baixo
            (r, c + 1),  # Direita
            (r, c - 1)   # Esquerda
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
        
        virarParaCoordenada(pos_atual, pos_proxima)
        
        ########### FAZ O ROBO AVANCAR UMA CASA ###########
        drive_base.straight(300)

        ########### ATUALIZA A POSICAO DO ROBO ###########
        linha, coluna = pos_proxima

########### RETORNA O CAMINHO PARA O QUADRADO MAIS DISTANTE DE MIM ###########
def encontrar_mais_distante(alvos, posicao_atual):
    global tabuleiro
    # Se não há mais células desconhecidas, retorna None
    if not alvos:
        return None

    melhor_alvo = None
    caminho_mais_longo = None

    # 2. Testa cada célula desconhecida para ver qual tem o caminho mais curto
    for alvo in alvos:
        # Usa a função BFS que já temos para encontrar o caminho
        caminho_candidato = encontrar_caminho_otimizado(tabuleiro, posicao_atual, alvo, 20)

        # Se um caminho válido foi encontrado para este alvo
        if caminho_candidato:
            # Se é o primeiro caminho válido que encontramos, ou se ele é mais curto que o melhor anterior
            if caminho_mais_longo is None or len(caminho_candidato) > len(caminho_mais_longo):
                caminho_mais_longo = caminho_candidato
                melhor_alvo = alvo

    return caminho_mais_longo

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
        caminho_candidato = encontrar_caminho_otimizado(mapa_de_cores, posicao_atual, alvo, 2)

        # Se um caminho válido foi encontrado para este alvo
        if caminho_candidato:
            # Se é o primeiro caminho válido que encontramos, ou se ele é mais curto que o melhor anterior
            if caminho_mais_curto is None or len(caminho_candidato) < len(caminho_mais_curto):
                caminho_mais_curto = caminho_candidato
                melhor_alvo = alvo

    return caminho_mais_curto

########### ANALISA O TABULEIRO PREENCHIDO E SALVA OS PONTOS NOTAVEIS ###########
def pontos_notaveis():
    global vermelhos, amarelos, verde, azul, gray
    for i in range(n):
        for j in range(m-1,-1,-1):
            if tabuleiro[i][j]==Color.MY_YELLOW:
                amarelos.append((i,j))
            if tabuleiro[i][j]==Color.MY_GREEN:
                verde.append((i,j))
            if tabuleiro[i][j]==Color.MY_GRAY:
                gray.append((i,j))
            if tabuleiro[i][j]==Color.MY_RED:
                vermelhos.append((i,j))

########### ENCONTRA O CAMINHO COM MENOS CURVAS NO CAMINHO (TESTAR PENALIDADE DA CURVA) #################
def encontrar_caminho_otimizado(mapa_de_cores, inicio, fim, penalidade_curva):
    OBSTACULOS = (Color.MY_YELLOW)
    total_linhas, total_colunas = len(mapa_de_cores), len(mapa_de_cores[0])

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
        vizinhos = [(r + 1, c, 'C'), (r - 1, c, 'B'), (r, c + 1, 'D'), (r, c - 1, 'E')]

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

########### MAPEIA O TABULEIRO ###########
def explorar_tabuleiro(caminho_a_seguir):
    global linha, coluna, direcao, tabuleiro

    # O loop vai até o penúltimo item, pois sempre olhamos para o próximo
    for i in range(len(caminho_a_seguir) - 1):
        pos_atual = caminho_a_seguir[i]
        pos_proxima = caminho_a_seguir[i+1]

        # Garante que o estado lógico do robô corresponde ao início do passo
        linha, coluna = pos_atual
        alvo_linha, alvo_coluna = pos_proxima

        # 1. Orienta o robô na direção do próximo passo
        virarParaCoordenada(pos_atual, pos_proxima)

        drive_base.reset(0,0)
        cor_atual = ler_cor()
        while ler_cor()==cor_atual:
            drive_base.straight(10, then=Stop.NONE)
        drive_base.stop()
        drive_base.straight(30)

        if ler_cor()==Color.MY_YELLOW :
            hub.ble.broadcast(1)
            tabuleiro[alvo_linha][alvo_coluna]= Color.MY_YELLOW
            amarelos.append((alvo_linha,alvo_coluna))
            drive_base.straight(-150)
            return
        
        if ler_cor()==Color.MY_GREEN:
            drive_base.stop()
            verde.append((alvo_linha,alvo_coluna))
            tabuleiro[alvo_linha][alvo_coluna]= Color.MY_GREEN
            drive_base.straight(-150)
            viraAngulo(90)
            alinharQuadrado()
            viraAngulo(90)
            hub.ble.broadcast(7)
            wait(1500)
            drive_base.settings(straight_speed=150, turn_rate=50)
            drive_base.straight(-420)
            drive_base.settings(straight_speed=200, turn_rate=50)
            drive_base.straight(420)
            viraAngulo(90)
            alinharQuadrado()
            hub.ble.broadcast(7)
            viraAngulo(-90)
            drive_base.settings(straight_speed=150, turn_rate=50)
            drive_base.straight(-420)
            drive_base.settings(straight_speed=200, turn_rate=50)
            drive_base.straight(420)
            viraAngulo(-90)
            drive_base.straight(80)
            viraAngulo(-90)
            drive_base.straight(330)
            hub.ble.broadcast(3)
            wait(2000)
            linha, coluna = pos_proxima
            return
        
        drive_base.straight(150, then=Stop.BRAKE)        
        linha, coluna = pos_proxima
        tabuleiro[linha][coluna]=ler_cor()

        if ler_cor()==Color.MY_RED:
            hub.ble.broadcast(2)
            drive_base.straight(50)
            vermelhos.append((alvo_linha,alvo_coluna))
    
    return

########### FAZ O ROBO SEMPRE APONTAR PARA POSICAO D ###########
def ajustar_direcao():
    reflexao_incial = color_sensorL.reflection()
    cor_inicial= ler_cor()
    drive_base.reset(0,0)
    while drive_base.distance()<=300:
        drive_base.straight(10, then=Stop.NONE)
        if(reflexao_incial!=color_sensorL.reflection()):
            reflexao_frente=color_sensorL.reflection()
            drive_base.stop()
            break
    alinharQuadrado(cor_inicial) # AINDA PRECISA FAZER O DO CINZA
    drive_base.straight(-(drive_base.distance()))
    drive_base.turn(-90)
    while drive_base.distance()<=300:
        drive_base.straight(10, then=Stop.NONE)
        if(reflexao_incial!=color_sensorL.reflection()):
            reflexao_lado=color_sensorL.reflection()
            drive_base.stop()
            break
    alinharQuadrado(cor_inicial)
    drive_base.straight(-(drive_base.distance()))
    print(reflexao_frente)
    print(reflexao_lado)
    if(reflexao_lado>=90 and reflexao_frente<90):
        drive_base.turn(180)
    elif(reflexao_lado<90 and reflexao_frente<90):
        drive_base.turn(90)
    elif(reflexao_lado>=90 and reflexao_frente >=90):
        drive_base.turn(-90)
    alinharQuadrado(cor_inicial)

########### IMPRIME O TABULEIRO FORMATADO ###########
def imprimeTabuleiro():
    global tabuleiro

    print("------------------------------------------------------------------------------------------------")
    for i in range(n-1, -1, -1):
        for j in range (m):
            if tabuleiro[i][j] == Color.MY_BLACK: print("|\tBLACK", end="\t")
            elif tabuleiro[i][j] == Color.MY_WHITE: print("|\tWHITE", end="\t")
            elif tabuleiro[i][j] == Color.MY_RED: print("|\tRED", end="\t")
            elif tabuleiro[i][j] == Color.MY_YELLOW: print("|\tYELLOW", end="\t")
            elif tabuleiro[i][j] == Color.MY_GREEN: print("|\tGREEEN", end="\t")
            else: print("|\tERRO", end="\t")
        print("", end="|")
        print()
        print("------------------------------------------------------------------------------------------------")

########################################### MAIN ###################################3
################ AGUARDA INICIO ###############
while not hub.ble.observe(120):
    wait(10)

################ AJUSTA A POSICAO INCIAL ###############
drive_base.reset(0,0)
tabuleiro[0][0] = ler_cor()
ponto_entrada = (0, 0)

################ COMEÇA EXPLORAR TABULEIRO ###############
desconhecido = encontrar_desconhecido_mais_proximo(tabuleiro, ponto_entrada)
while desconhecido:
    print(f"{linha},{coluna}")
    explorar_tabuleiro(desconhecido)
    desconhecido = encontrar_desconhecido_mais_proximo(tabuleiro, (linha,coluna))
    if(len(verde)==1 and len(vermelhos)==4):
        break
hub.ble.broadcast(6)
imprimeTabuleiro()