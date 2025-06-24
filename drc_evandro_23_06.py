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
ANGULOS_DIRECAO = {'C': 0, 'D': 90, 'B': 180, 'E': -90}
linha, coluna = 0, 0
direcao = 'E'

########### CORES ###########
MY_BLACK= Color(270, 27, 27)
MY_BLUE = Color(219, 85, 48)
MY_GRAY = Color(235, 23, 60)
MY_YELLOW = Color(60, 42, 98)
MY_RED = Color(353, 82, 87)
MY_GREEN = Color(138, 49, 88)
MINHAS_CORES = (MY_BLACK, MY_BLUE, MY_GRAY, MY_YELLOW, MY_RED, MY_GREEN)
CORES_DE_PRIORIDADE = (MY_YELLOW, MY_BLUE, MY_RED, MY_GREEN, MY_BLACK)

########### MOTORES ###########
motorE = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
motorG = Motor(Port.B, Direction.COUNTERCLOCKWISE) #GARRA
drive_base = DriveBase(motorE, motorD, 56, 137)
drive_base.use_gyro(True)
drive_base.settings(straight_speed=200)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.D)
color_sensorE = ColorSensor(Port.C)
color_sensorL = ColorSensor(Port.A)
color_sensorE.detectable_colors(MINHAS_CORES)
color_sensorD.detectable_colors(MINHAS_CORES)
color_sensorL.detectable_colors(Color.RED, Color.GREEN)

########### FUNCOES ###########
def ler_cor():
    cor_e = color_sensorE.color()
    cor_d = color_sensorD.color()

    if cor_e == cor_d:
        return cor_e

    for cor_prioritaria in CORES_DE_PRIORIDADE:
        # Se um dos sensores vir uma cor importante, essa é a que vale.
        if cor_e == cor_prioritaria:
            return cor_e
        if cor_d == cor_prioritaria:
            return cor_d

    return cor_e

def virarPara(direcao_atual, direcao_destino):
    if direcao_atual == direcao_destino:
        return direcao_destino

    angulo_atual = ANGULOS_DIRECAO[direcao_atual]
    angulo_destino = ANGULOS_DIRECAO[direcao_destino]
    
    # Calcula o ângulo de giro
    angulo_giro = angulo_destino - angulo_atual
    
    # Normaliza o ângulo para o caminho mais curto (entre -180 e 180)
    if angulo_giro > 180:
        angulo_giro -= 360
    elif angulo_giro < -180:
        angulo_giro += 360
        
    # Executa o giro
    drive_base.turn(angulo_giro)
    wait(100) # Pequena pausa para estabilizar
    
    return direcao_destino

def frente(linha, coluna):
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha+=1
    elif direcao == 'C':
        linha-=1
    
    drive_base.reset(0, 0)
    while drive_base.distance() <= 300:
        drive_base.drive(100, 0)
        if ler_cor() == MY_YELLOW or ler_cor() == MY_BLUE:
            drive_base.stop()
            break
    
    return linha, coluna 

def alinharPreto():
    while color_sensorD.color()!= Color.BLACK:
            drive_base.drive(100, 0)
    drive_base.stop()

    while color_sensorE.color()!=Color.WHITE and color_sensorE.color()!=Color.MY_BLUE:
        motorE.run(-50)
    motorE.stop()

    while color_sensorD.color()!=Color.WHITE and color_sensorD.color()!=Color.MY_BLUE:
        motorD.run(-50)
    motorD.stop()

def desviaAmarelo(direcao_atual, linha_atual, coluna_atual):
    coluna_obstaculo = coluna_atual
    linha_obstaculo = linha_atual

    if direcao_atual == 'D':
        coluna_obstaculo += 1
    elif direcao_atual == 'E':
        coluna_obstaculo -= 1
    elif direcao_atual == 'B':
        linha_obstaculo += 1
    elif direcao_atual == 'C':
        linha_obstaculo -= 1

    tabuleiro[linha_obstaculo][coluna_obstaculo] = MY_YELLOW

    # 2. Define as direções relativas para o desvio
    direcao_inicial = direcao_atual

    # 'virar_a_esquerda' e 'virar_a_direita' são relativos à direção de movimento
    if direcao_inicial == 'D': # Indo para Direita
        virar_a_esquerda, virar_a_direita = 'C', 'B'
    elif direcao_inicial == 'E': # Indo para Esquerda
        virar_a_esquerda, virar_a_direita = 'B', 'C'
    elif direcao_inicial == 'B': # Indo para Baixo
        virar_a_esquerda, virar_a_direita = 'D', 'E'
    else: # direcao_inicial == 'C' (Indo para Cima)
        virar_a_esquerda, virar_a_direita = 'E', 'D'

    # 3. Executa a manobra de contorno
    # Passo A: Sai da linha original
    direcao_atual = virarPara(direcao_atual, virar_a_esquerda)
    linha_atual, coluna_atual = frente(linha_atual, coluna_atual)
    tabuleiro[linha_atual][coluna_atual] = color_sensorE.color() # Mapeia a célula do desvio

    # Passo B: Anda paralelamente à linha original
    direcao_atual = virarPara(direcao_atual, virar_a_direita)
    linha_atual, coluna_atual = frente(linha_atual, coluna_atual) # Passa ao lado do obstáculo
    tabuleiro[linha_atual][coluna_atual] = color_sensorE.color() # Mapeia

    # Passo C: Retorna para a linha original
    direcao_atual = virarPara(direcao_atual, virar_a_direita)
    linha_atual, coluna_atual = frente(linha_atual, coluna_atual)
    tabuleiro[linha_atual][coluna_atual] = color_sensorE.color()

    # Passo D: Re-alinha com a direção original do percurso
    direcao_atual = virarPara(direcao_atual, virar_a_esquerda)
    
    return direcao_atual, linha_atual, coluna_atual

########### MAIN ###########
########### IR ATÉ A BORDA (0,0) ###########
alinharPreto()
direcao = virarPara(direcao, 'D')
indo_para_direita = True # Flag para controlar a direção da varredura
tabuleiro[linha][coluna]=ler_cor()

########### PERCORRENDO O LABIRINTO ###########
for i in range(n):
    for j in range(m-1): 
        linha, coluna = frente(linha, coluna)
        cor = ler_cor()
        tabuleiro[linha][coluna]=cor      
        if cor == MY_YELLOW:
            desviaAmarelo(direcao, linha, coluna)

    ########### ALINHAR NA BORDA NO FINAL DA LINHA ###########   
    alinharPreto()

    ########### MUDAR PARA OUTRA LINHA ###########   
    # Se ainda não estiver na última linha, desce para a próxima
    if i < n - 1:
        drive_base.straight(-50) # Pequeno recuo para poder virar
        direcao = virarPara(direcao, 'B') # Vira para baixo
        
        # Anda para a próxima linha
        linha, coluna = frente(linha, coluna)
        tabuleiro[linha][coluna] = color_sensorE.color()

        # Inverte a direção da varredura para a próxima linha (zigue-zague)
        if indo_para_direita:
            direcao = virarPara(direcao, 'E') # Vira para a Esquerda
        else:
            direcao = virarPara(direcao, 'D') # Vira para a Direita
        
        # Inverte a flag
        indo_para_direita = not indo_para_direita

print("Mapeamento concluído!")
print(tabuleiro)