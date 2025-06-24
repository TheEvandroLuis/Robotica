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
def imprimeTabuleiro():
    global tabuleiro

    print("-----------------------------------------------------------------------------------------------------------------")
    for linha in tabuleiro:
        for j in range (m-1, -1, -1):
            print(linha[j], end="\t|\t")
        print()
        print("-----------------------------------------------------------------------------------------------------------------")

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

def verificarFrente():
    drive_base.straight(200)
    return ler_cor()
   
def frente():
    global linha, coluna, direcao
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha-=1
    elif direcao == 'C':
        linha+=1

    drive_base.straight(100)
    print(f"Estou em {linha}, {coluna}")

def andarBorda():
    drive_base.reset(0,0)
    while ler_cor()!=Color.MY_BLACK and ler_cor()!=Color.MY_BLUE:
        drive_base.straight(20, then=Stop.NONE)
    return drive_base.distance()

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

def desviaAmarelo():
    global direcao, linha, coluna

    coluna_obstaculo = coluna_atual
    linha_obstaculo = linha_atual

    #tabuleiro[linha_obstaculo][coluna_obstaculo] = Color.MY_YELLOW

    # 2. Define as direções relativas para o desvio
    direcao_inicial = direcao_atual

    # 3. Executa a manobra de contorno
    # Passo A: Sai da linha original
    direcao_atual = virarPara(direcao_atual, 'C')
    drive_base.straight(300)

    # Passo B: Anda paralelamente à linha original
    direcao_atual = virarPara(direcao_atual, direcao_inicial)
    drive_base.straight(600)

    # Passo C: Retorna para a linha original
    direcao_atual = virarPara(direcao_atual, 'B')
    drive_base.straight(300)
    # Passo D: Re-alinha com a direção original do percurso
    direcao_atual = virarPara(direcao_atual, direcao_inicial)
    
    return direcao_atual, linha_atual, coluna_atual

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

def fechar_borda():
    global tabuleiro
    global n,m

    for i in range(n):
        if tabuleiro[i][0]==Color.NONE: tabuleiro[i][0]=Color.WHITE
        if tabuleiro[i][m-1]==Color.NONE: tabuleiro[i][m-1]=Color.WHITE

    for i in range(m):
        if tabuleiro[0][i]==Color.NONE: tabuleiro[0][i]=Color.WHITE
        if tabuleiro[n-1][i]==Color.NONE: tabuleiro[n-1][i]=Color.WHITE

########### SAINDO DO CINZA ###########
while ler_cor()==Color.MY_GRAY:
    drive_base.straight(20, then=Stop.NONE)
hub.speaker.beep(500, 100)

########### ANDANDO PELA BORDA ###########
for lado in range(4):
    distancia = andarBorda()
    quadrados = distancia // 300

    if lado==0:
        tabuleiro[0][quadrados] = Color.MY_GRAY
    else:
        if direcao == 'C': linha -= quadrados
        elif direcao == 'B': linha += quadrados
        elif direcao == 'D': coluna -= quadrados
        elif direcao == 'E': coluna +=quadrados    
    
    preencher_borda(linha, coluna, direcao, quadrados)
    hub.speaker.beep(400, 100)
    
    if ler_cor() == Color.MY_BLUE:
        hub.speaker.beep(300, 100)
        drive_base.straight(-100)
        
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

        fechar_borda()
        break

    else:
        alinharPreto()
        viraAngulo(90)   

imprimeTabuleiro()

print(f"ESTOU EM: {linha}, {coluna}")