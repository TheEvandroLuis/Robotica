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


cor_linha= Color.WHITE

# ==========================================
# CONSTANTES DE DIREÇÃO E POSIÇÃO
# ==========================================
ANGULOS_DIRECAO = {'B': 0, 'D': 270, 'C': 180, 'E': 90}
direcao = 'C'

# ==========================================
# LÓGICA DO GRAFO 
# ==========================================
mapa = {(0,0): {'C': 1, 'D':1, 'E': 0, 'B':0},
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
MOVIMENTO = { 'C': (1, 0),
            'B': (-1, 0),
            'D': (0, 1),
            'E': (0, -1)}
PRIORIDADE = ['C', 'D', 'E', 'B']

# ==========================================
# FUNÇOES
# ==========================================
########### SEGUIDOR DE LINHA ###########
def seguir_linha():
    alvo=90
    kp=1.2
    erro = alvo - color_sensorM.reflection()
    correcao = erro * kp
    drive_base.drive(250, correcao)
def seguir_linha2():
    alvo=90
    kp=1.2
    erro = alvo - color_sensorM.reflection()
    correcao = erro * kp
    drive_base.drive(500, correcao) #400

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

########### ENCONTRAR MENOR CAMINHO ENTRE DOIS PONTOS #############
########### RETORNA UMA LISTA COM AS COORDENADAS A SEREM SEGUIDAS ##########
def calcular_menor_caminho(mapa, inicio, destino): 
    fila = []
    fila.append((inicio, [inicio]))
    
    visitados_bfs = set()
    visitados_bfs.add(inicio)

    while len(fila) > 0:
        # Pega o primeiro elemento da fila
        no_atual, caminho_atual = fila.pop(0)

        # Condição de vitória
        if no_atual == destino:
            return caminho_atual

        saidas = mapa.get(no_atual, {})
        # Como a ordem exata de busca no BFS não importa para o menor caminho,
        # podemos iterar direto nos itens disponíveis.
        for direcao, estado in saidas.items():
            if estado == 2: # Navega apenas por caminhos SEGUROS
                dy, dx = MOVIMENTO[direcao]
                vizinho = (no_atual[0] + dy, no_atual[1] + dx)

                if vizinho not in visitados_bfs:
                    visitados_bfs.add(vizinho)
                    # Cria a nova rota anexando a COORDENADA do vizinho, não a direção
                    novo_caminho = caminho_atual + [vizinho] 
                    fila.append((vizinho, novo_caminho))

    print(f"Erro: Não há rota segura entre {inicio} e {destino}")
    return None



# ==========================================
# MAIN
# ==========================================
######################## INDO PARA O 0,0 NO INICIO DO JOGO ########################
while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha:
    seguir_linha()
drive_base.straight(50)
virarPara('E')
while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
    seguir_linha()

################## CASO TENHA UM VERMELHO ENTRE A ENTRADA E O 0,0 ############################
if color_sensorM.color()== Color.RED:
    drive_base.straight(-50)
    posicao_atual= (0,1)
    posicao_inicial= (0,1)
    virarPara('D')
    while color_sensorE.color()!=cor_linha:
        seguir_linha()
    drive_base.straight(50)
    virarPara('C')

################## CASO NÃO TENHA UM VERMELHO ENTRE A ENTRADA E O 0,0 ############################
else:
    drive_base.straight(50)
    virarPara('C')
    posicao_atual = (0, 0) # Ponto de partida
    posicao_inicial= (0, 0)

######################## COMEÇANDO A PROCURAR O FINAL DO TABULEIRO ########################
#Pontos de chegada
destino42 = (4, 2)       
destino41 = (4, 1)
pilha = []
pilha.append(posicao_atual)
while len(pilha) > 0:
    ####### CONDIÇÃO DE PARADA VERIFICA SE CHEGAMOS NO FINAL ################
    if posicao_atual == destino41 or posicao_atual==destino42:
        ############ VIRA PARA O LOCAL CORRETO EM DIRECAO A SAIDA A DEPENDER DO PONTO FINAL
        if posicao_atual==(4,2):
            virarPara('E')
        else:
            virarPara('D')
        drive_base.reset()
        while color_sensorD.color()!=cor_linha and color_sensorE.color()!=cor_linha and color_sensorM.color()!=Color.RED:
            seguir_linha()
        drive_base.stop()
        ############# CASO ENCONTRE UM VERMELHO MUDA O DESTINO PARA O OUTRO LADO
        if color_sensorM.color()==Color.RED:
            drive_base.straight(-drive_base.distance())   
            if posicao_atual==(4,2):
                mapa[posicao_atual]['E']=-1
                destino42 = (4,1)
            else:
                mapa[posicao_atual]['D']=-1
                destino41 = (4,2)  
        ############# DO CONTRARIO FAZ A MANOBRA NO FINAL PARA COMECA O SPEEDRUN E ENCERRA A PROCURA                  
        else:
            drive_base.straight(50)
            virarPara('C')
            drive_base.straight(200)
            virarPara('B')
            while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha:
                seguir_linha()
            drive_base.straight(50)
            break
    
    avancou = False

    ############# PROCURA POR CAMINHOS A SEREM SEGUIDOS ###################
    for direcao_vizinho in PRIORIDADE:
        ############# VERIFICA QUAL CAMINHO SEGUIR SEGUINDO A PRIORIDADE
        estado = mapa[posicao_atual].get(direcao_vizinho)

        if estado == 1:  #TESTANDO UMA IDEIA AQUI
            dy, dx = MOVIMENTO[direcao_vizinho]
            no_destino = (posicao_atual[0] + dy, posicao_atual[1] + dx)
            virarPara(direcao_vizinho)

            drive_base.reset()
            ###### ANDA ATÉ O CRUZAMENTO OU ATÉ VER UM VERMELHO
            if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
                while color_sensorD.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
                while color_sensorE.color()!=Color.WHITE and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            else:  
                while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            drive_base.stop()
            
            ########## SE ENCONTROU VERMELHO VOLTA PARA O CRUZAMENTO#######
            if color_sensorM.color()==Color.RED:
                drive_base.straight(-drive_base.distance())
                ####### MARCA A IDA E A VOLTA COMO -1
                if direcao =='C': 
                    direcao_oposta = 'B'
                elif direcao=='B':
                    direcao_oposta = 'C'
                elif direcao=='E':
                    direcao_oposta = 'D'
                elif direcao=='D':
                    direcao_oposta = 'E'
                mapa[posicao_atual][direcao] = -1
                mapa[no_destino][direcao_oposta] = -1

            ########## SE CHEGOU AO CRUZAMENTO ###########
            else:
                drive_base.straight(50)
                ######### MARCA A IDA E VOLTA COMO SEGURO
                if direcao =='C': 
                    direcao_oposta = 'B'
                elif direcao=='B':
                    direcao_oposta = 'C'
                elif direcao=='E':
                    direcao_oposta = 'D'
                elif direcao=='D':
                    direcao_oposta = 'E'
                mapa[no_destino][direcao_oposta] += 1
                mapa[posicao_atual][direcao] += 1
                posicao_atual = no_destino
                pilha.append(posicao_atual)
                avancou = True
                break
            
    ############# CASO ESTEJA EM UM BECO SEM SAIDA ###############
    ############# EU ACHO QUE MARCANDO O CAMINHO DE VOLTA COMO -1 PODEMOS VISITAR NOVAMENTE OS CAMINHOS SEGUROS SEM CAIR EM UM LOOP 
    if not avancou:
        no_descartado = pilha.pop()        
        if len(pilha) > 0:
            print(pilha)
            no_destino = pilha[-1]
            virar_para_no(posicao_atual, no_destino)
            if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
                while color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
                while color_sensorE.color()!=cor_linha and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            else:  
                while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
                    seguir_linha()
            drive_base.straight(50)
            posicao_atual=no_destino
            ####### MARCA A IDA E A VOLTA COMO -1 ##########
            if direcao =='C': 
                direcao_oposta = 'B'
            elif direcao=='B':
                direcao_oposta = 'C'
            elif direcao=='E':
                direcao_oposta = 'D'
            elif direcao=='D':
                direcao_oposta = 'E'
            #mapa[posicao_atual][direcao_oposta] = -1
            #mapa[no_destino][direcao] = -1

################## CAMINHO DE VOLTA ########################
########## VAI ATÉ O DESTINO USADO PARA ACESSAR A SAIDA #################
if pilha[-1]==(4,2):
    virarPara('D')
else:
    virarPara('E')
while color_sensorD.color()!=cor_linha and color_sensorE.color()!=cor_linha:
    seguir_linha2()
drive_base.straight(50)

########## ENCONTRAR O MELHOR CAMINHO DE VOLTA #################
caminho_volta = calcular_menor_caminho(mapa, pilha[-2], posicao_inicial)
print(caminho_volta)
print(posicao_atual)

########## SEGUE O CAMINHO ENCONTRADO ###################
for no_destino in caminho_volta:  
    virar_para_no(posicao_atual, no_destino)
    if (direcao=='D' and posicao_atual[0]==4) or (direcao=='E' and posicao_atual[0]==0):
        while color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
            seguir_linha2()
    elif (direcao=='D' and posicao_atual[0]==0) or (direcao=='E' and posicao_atual[0]==4):
        while color_sensorE.color()!=cor_linha and color_sensorM.color()!=Color.RED:
            seguir_linha2()
    else:  
        while color_sensorE.color()!=cor_linha and color_sensorD.color()!=cor_linha and color_sensorM.color()!=Color.RED:
            seguir_linha2()
    drive_base.straight(50)
    posicao_atual=no_destino

############ CHEGAMOS NO 0,0  NA VOLTA #########################
########### SE A POSICAO INICIAL FOR (0,0) ##################
if posicao_inicial == (0, 0):
    drive_base.straight(10)
    virarPara('D')
    while color_sensorD.color()!=cor_linha:
        target=60
        kp=-0.5
        erro = color_sensorE.reflection() - target
        correcao = erro * kp
        drive_base.drive(250, correcao)
    drive_base.straight(50)
############ SE A POSICAO INICIAL FOR (0, 1) ############
else: 
    virarPara('E')
    while color_sensorE.color()!=cor_linha:
        seguir_linha()
    drive_base.straight(50)
virarPara('B')
drive_base.straight(80)