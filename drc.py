from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=-Axis.X)

########### MOTORES ###########
motorE = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
drive_base = DriveBase(motorE, motorD, 56, 120)
drive_base.use_gyro(True)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.D)
color_sensorE = ColorSensor(Port.C)
Color.BLACK = Color(270, 27, 27)
Color.GRAY = Color(220, 30, 50)
Color.MY_YELLOW = Color(67, 42, 98)
Color.MY_GREEN = Color(138, 49, 88)
color_sensorE.detectable_colors((Color.BLACK, Color.WHITE, Color.GRAY, Color.RED, Color.MY_YELLOW, Color.MY_GREEN))
color_sensorD.detectable_colors((Color.BLACK, Color.WHITE, Color.GRAY, Color.RED, Color.MY_YELLOW, Color.MY_GREEN))

########### VARIAVEIS ###########
n = 6
tabuleiro = [[ Color.NONE for _ in range(n)] for _ in range(n)]
linha, coluna = 0, 0
direcao = 'E'

########### FUNCOES ###########
def verificarFrente(): 
    cor_atual = color_sensorE.color()
    alvo = color_sensorE.reflection()
    while color_sensorE.color() == cor_atual or color_sensorD.color() == cor_atual:
        drive_base.drive(100, 0)
    drive_base.stop()
    drive_base.straight(20)

    
    if color_sensorE.color()==Color.WHITE:
        hub.light.on(Color.WHITE)
        #print(f"ESQ: {color_sensorE.reflection()} | DIR: {color_sensorD.reflection()}")

        while color_sensorE.color()!=Color.BLACK:
            motorE.run(-50)
        motorE.stop()

        while color_sensorD.color()!=Color.BLACK:
            motorD.run(-50)
        motorD.stop()
        
        drive_base.straight(20)
        #print(f"ESQ: {color_sensorE.color()} | DIR: {color_sensorD.color()}")
    elif color_sensorE.color()==Color.BLACK:
        hub.light.on(Color.WHITE)

        while color_sensorE.color()!=Color.WHITE:
            motorE.run(-50)
        motorE.stop()

        while color_sensorD.color()!=Color.WHITE:
            motorD.run(-50)
        motorD.stop()
        
        drive_base.straight(20)

    elif color_sensorE.color()==Color.GRAY:
        hub.light.on(Color.RED)
    elif color_sensorE.color()==Color.RED:
        hub.light.on(Color.RED)
    elif color_sensorE.color()==Color.MY_GREEN:
        hub.light.on(Color.GREEN)
    elif color_sensorE.color()==Color.MY_YELLOW:
        hub.light.on(Color.YELLOW)
    wait(500)
    hub.light.off()
    return color_sensorE.color()

def frente(linha, coluna):
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha+=1
    elif direcao == 'C':
        linha-=1
    drive_base.straight(200)
    print(f"Estou em {linha}, {coluna}")
    return linha, coluna 

def virarPara(dir):
    if (dir== direcao):
        return dir
    else: 
        if dir =='B':
            if direcao == 'C':
                drive_base.turn(180)
            elif direcao == 'D':
                drive_base.turn(90)
            elif direcao == 'E':
                drive_base.turn(-90)
        elif dir =='D':
            if direcao == 'C':
                drive_base.turn(90)
            elif direcao == 'B':
                drive_base.turn(-90)
            elif direcao == 'E':
                drive_base.turn(180)
        elif dir =='E':
            if direcao == 'C':
                drive_base.turn(-90)
            elif direcao == 'B':
                drive_base.turn(90)
            elif direcao == 'D':
                drive_base.turn(180)
        elif dir =='C':
            if direcao == 'B':
                drive_base.turn(180)
            elif direcao == 'D':
                drive_base.turn(-90)
            elif direcao == 'E':
                drive_base.turn(90)
        return dir

########### MAIN ###########
########### INDO PARA O (0,0) ###########
proxQuadrado = verificarFrente()
while proxQuadrado != Color.GRAY: ##PENSAR O QUE FAZER CASO TENHA ALGUM QUADRADO Y/G NO CAMINHO
    linha, coluna = frente(linha, coluna)
    proxQuadrado = verificarFrente()

########### ESTOU EM (0,0) ###########
direcao = virarPara('D')
tabuleiro[linha][coluna] = color_sensorE.color()
linha, coluna = 0, 0

########### ANDANDO PELO LABIRINTO ###########
for i in range(6): #6 linhas
    for j in range(1, 6): #5 colunas já que estamos sempre em uma
        sensor = verificarFrente()
        if sensor!= Color.GRAY:
            linha, coluna = frente (linha, coluna)
            tabuleiro[linha][coluna]=color_sensorE.color()
    direcao = virarPara('B')
    sensor = verificarFrente()
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensorE.color()
    if coluna==5: #VIRA PARA O INICIO OU FINAL DO TABULEIRO
        direcao = virarPara('E')
    else:
        direcao = virarPara('D')
print(tabuleiro)