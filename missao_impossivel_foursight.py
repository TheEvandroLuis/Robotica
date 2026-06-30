from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# ==========================================
# CONFIGURAÇÃO DE HARDWARE
# ==========================================
hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
motorE = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.B, Direction.CLOCKWISE)
drive_base = DriveBase(motorE, motorD, 68.8, 133)
drive_base.settings(straight_speed=300, turn_rate=100)
drive_base.use_gyro(True)
color_sensorD = ColorSensor(Port.F)
color_sensorE = ColorSensor(Port.E)
color_sensorM = ColorSensor(Port.D)

# ==========================================
# CONSTANTES DE DIREÇÃO E POSIÇÃO
# ==========================================
ANGULOS_DIRECAO = {'B': 0, 'D': 270, 'C': 180, 'E': 90}
direcao = 'C'

# ==========================================
# LÓGICA DO GRAFO 
# ==========================================
mapa = {
    (0,0): {'C': 1, 'D':1, 'E': 0, 'B':0},
    (0,1): {'C': 1, 'D':1, 'E': 1, 'B':0},
    (0,2): {'C': 1, 'D':0, 'E': 1, 'B':0},
    (1,0): {'C': 1, 'D':1, 'E': 0, 'B':1},
    (1,1): {'C': 1, 'D':1, 'E': 1, 'B':1},
    (1,2): {'C': 1, 'D':0, 'E': 1, 'B':1},
    (2,0): {'C': 1, 'D':1, 'E': 0, 'B':1},
    (2,1): {'C': 1, 'D':1, 'E': 1, 'B':1},
    (2,2): {'C': 1, 'D':0, 'E': 1, 'B':1},
    (3,0): {'C': 1, 'D':1, 'E': 0, 'B':1},
    (3,1): {'C': 1, 'D':1, 'E': 1, 'B':1},
    (3,2): {'C': 1, 'D':0, 'E': 1, 'B':1},
    (4,0): {'C': 0, 'D':1, 'E': 0, 'B':1},
    (4,1): {'C': 0, 'D':1, 'E': 1, 'B':1},
    (4,2): {'C': 0, 'D':0, 'E': 1, 'B':1}}

MOVIMENTO = {
    'C': (1, 0),
    'B': (-1, 0),
    'D': (0, 1),
    'E': (0, -1)}
   
visitados = set()
PRIORIDADE = ['C', 'D', 'E', 'B']

########### SEGUIDOR DE LINHA ###########
def seguir_linha(sensor):
    alvo=90
    kp=1.2
    if sensor == 'D':
        erro = color_sensorM.reflection() - alvo
        correcao = erro * kp 
        drive_base.drive(300, correcao)
    elif sensor == 'E':
        erro = alvo - color_sensorM.reflection()
        correcao = erro * kp
        drive_base.drive(300, correcao)

########### IMPRIME MAPA ###########
def imprimir_mapa(mapa):
    if not mapa:
        print("Mapa vazio.")
        return

    # Encontra os limites do mapa dinamicamente
    max_y = max(coord[0] for coord in mapa.keys())
    max_x = max(coord[1] for coord in mapa.keys())

    print("\n" + "="*30)
    print("      MAPA DO LABIRINTO")
    print("="*30)

    # O loop roda de cima para baixo (do maior Y para o menor Y)
    for y in range(max_y, -1, -1):
        linha_nos = ""
        
        # 1. Desenha os nós e as conexões horizontais (Direita)
        for x in range(max_x + 1):
            no = mapa.get((y, x), {'C': 0, 'D': 0, 'E': 0, 'B': 0})
            
            # Formata o nó atual
            linha_nos += f"[{y},{x}]"
            
            # Adiciona a conexão para a Direita (se não for a última coluna)
            if x < max_x:
                if no.get('D') == 1:
                    linha_nos += " -- "
                elif no.get('D') == 2:   # Caso você implemente o estado 'visitado'
                    linha_nos += " == "
                elif no.get('D') == -1:  # Caso você implemente 'armadilha'
                    linha_nos += " XX "
                else:
                    linha_nos += "    "  # Parede / Sem caminho
        
        print(linha_nos)

        # 2. Desenha as conexões verticais (Baixo)
        if y > 0:
            linha_vert = ""
            for x in range(max_x + 1):
                no = mapa.get((y, x), {'C': 0, 'D': 0, 'E': 0, 'B': 0})
                
                # Adiciona a conexão para Baixo
                if no.get('B') == 1:
                    linha_vert += "  |     "
                elif no.get('B') == 2:
                    linha_vert += "  ||    "
                elif no.get('B') == -1:
                    linha_vert += "  X     "
                else:
                    linha_vert += "        "
            print(linha_vert)
            
    print("="*30 + "\n")

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
    drive_base.turn(angulo_giro)
    wait(500) # Pequena pausa para estabilizar

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
    virarPara(nova_direcao_letra)

########### VIRA O ROBO USANDO NOS ADJACENTES ###########
def virar_para_no(origem, destino):
    """
    Recebe dois nós adjacentes no formato (y, x), calcula a direção 
    cardeal correspondente e aciona a função de giro do robô.
    """
    y1, x1 = origem
    y2, x2 = destino
    
    # Calcula a diferença entre as coordenadas
    dy = y2 - y1
    dx = x2 - x1
    
    direcao_destino = None
    
    # Mapeia a diferença matemática para a letra correspondente
    if dy > 0:
        direcao_destino = 'C'  # O Y aumentou, foi para Cima
    elif dy < 0:
        direcao_destino = 'B'  # O Y diminuiu, foi para Baixo
    elif dx > 0:
        direcao_destino = 'D'  # O X aumentou, foi para a Direita
    elif dx < 0:
        direcao_destino = 'E'  # O X diminuiu, foi para a Esquerda
        
    # Se encontrou uma direção válida, aciona a sua função base
    if direcao_destino:
        virarPara(direcao_destino)
    else:
        print(f"Aviso: Os nós {origem} e {destino} são idênticos ou inválidos.")

######################## INDO PARA O 0,0 NO INICIO DO JOGO ########################
while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)
virarPara('E')
while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)
virarPara('C')

# Mapeamento vetorial para saber qual vizinho estamos olhando
posicao_atual = (0, 0) # Ponto de partida
destino = (4, 2)       # Ponto de chegada

visitados = set()
visitados.add(posicao_atual)

pilha = []
pilha.append(posicao_atual)

while len(pilha) > 0:
    # 1. CONDIÇÃO DE PARADA
    if posicao_atual == destino:
        break
   
    avancou = False
    # 2. BUSCA DE NOVOS CAMINHOS
    # Define a ordem exata que o robô deve testar os caminhos
    for direcao_vizinho in PRIORIDADE:
        # Pegamos o estado daquela direção específica no mapa
        estado = mapa[posicao_atual].get(direcao_vizinho)
        if estado == 1: # Caminho existe e é desconhecido
            dy, dx = MOVIMENTO[direcao_vizinho]
            no_destino = (posicao_atual[0] + dy, posicao_atual[1] + dx)

            #Se nao foi visitado ainda por outro nó (talvez excluir se quiser testar todos os caminhos)
            if no_destino not in visitados:
                virarPara(direcao_vizinho)
                #print(f"Avançando para {direcao} -> Nó {no_destino}")
                
                drive_base.reset()
                #Anda ate o cruzamento ou até ver vermelho
                if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
                    while color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                        seguir_linha('E')
                elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
                    while color_sensorE.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                        seguir_linha('D')
                else:  
                    while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                        seguir_linha('D')
                drive_base.stop()
                #Se encontrou vermelho volta (verificar erro caso o vermelho esteja muito perto do cruzamento)
                if color_sensorM.color()==Color.RED:
                    drive_base.straight(-drive_base.distance())
                    if direcao =='C': 
                        direcao_oposta = 'B'
                    elif direcao=='B':
                        direcao_oposta = 'C'
                    elif direcao=='E':
                        direcao_oposta = 'D'
                    elif direcao=='D':
                        direcao_oposta = 'E'
                    #print(f"Direcao: {direcao} / Direcao Vizinho: {direcao_vizinho}")
                    #Marca ida e volta como vermelho
                    mapa[posicao_atual][direcao] = -1
                    mapa[no_destino][direcao_oposta] = -1
                
                #Chegou no destino e atualiza que o caminho é seguro
                else:
                    drive_base.straight(50)
                    mapa[posicao_atual][direcao] = 2
                    if direcao =='C': 
                        direcao_oposta = 'B'
                    elif direcao=='B':
                        direcao_oposta = 'C'
                    elif direcao=='E':
                        direcao_oposta = 'D'
                    elif direcao=='D':
                        direcao_oposta = 'E'
                    mapa[no_destino][direcao_oposta] = 2
                    posicao_atual = no_destino
                    visitados.add(posicao_atual)
                    pilha.append(posicao_atual)
                    avancou = True
                    break # Para o for e recomeça o while no novo nó
             
    #caso fique em um beco sem saida volta para a interseccao anterior
    if not avancou:
        # Se o loop 'for' terminou e 'avancou' continua False, é um beco sem saída.
        no_descartado = pilha.pop()
        print(f"Beco sem saída em {no_descartado}. Voltando...")
        
        if len(pilha) > 0:
            print(pilha)
            # O algoritmo "volta no tempo" para a decisão anterior
            no_destino = pilha[-1]
            virar_para_no(posicao_atual, no_destino)
            if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
                    while color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                        seguir_linha('E')
            elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
                while color_sensorE.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                    seguir_linha('D')
            else:  
                while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                    seguir_linha('E')
            drive_base.straight(50)
            posicao_atual=no_destino
            print(f"Retornou para {posicao_atual}")
        else:
            print("Mapa inteiro explorado, destino não encontrado.")


################### CHEGAMOS NO PONTO 4,2 ###############
virarPara('E')
while color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)
virarPara('C')
drive_base.straight(100)
virarPara('B')
while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)
virarPara('D')
while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)

################## CAMINHO DE VOLTA ########################
pilha.pop()
while len(pilha) > 0:
    print(pilha)
    # O algoritmo "volta no tempo" para a decisão anterior
    no_destino = pilha[-1]
    virar_para_no(posicao_atual, no_destino)
    if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
        while color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
            seguir_linha('E')
    elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
        while color_sensorE.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
            seguir_linha('D')
    else:  
        while color_sensorE.color()!=Color.WHITE and color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
            seguir_linha('E')
    drive_base.straight(50)
    posicao_atual=no_destino
    pilha.pop()

############ CHEGAMOS NO 0,0  NA VOLTA #########################
virarPara('D')
while color_sensorD.color()!=Color.WHITE:
    seguir_linha('D')
drive_base.straight(50)
virarPara('B')
drive_base.straight(80)

imprimir_mapa(mapa)