from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
########### MOTORES/SENSORES ###########
hub = PrimeHub()
motorA = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorB = Motor(Port.F, Direction.CLOCKWISE)
drive_base = DriveBase(motorA, motorB, 56, 140)
color_sensor = ColorSensor(Port.D)
Color.BLACK = Color(270, 27, 27)
Color.GRAY = Color(220, 30, 50)
color_sensor.detectable_colors((Color.BLACK, Color.WHITE, Color.GRAY))
n = 6
tabuleiro = [[ Color.NONE for _ in range(n)] for _ in range(n)]
linha, coluna = 0, 0
direcao = 'E'

########### FUNCOES ###########
def verificarFrente(): 
    cor_atual = color_sensor.color()
    while color_sensor.color() == cor_atual:
        drive_base.drive(100, 0)
    drive_base.stop()
    drive_base.straight(5)
    if color_sensor.color()==Color.WHITE:
        hub.light.on(Color.WHITE)
    elif color_sensor.color()==Color.BLACK:
        hub.light.on(Color.BLACK)
    elif color_sensor.color()==Color.GRAY:
        hub.light.on(Color.RED)
    wait(500)
    hub.light.off()
    return color_sensor.color()

def frente(linha, coluna):
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha+=1
    elif direcao == 'C':
        linha-=1
    drive_base.straight(150)
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
tabuleiro[linha][coluna] = color_sensor.color()
linha, coluna = 0, 0

for i in range(6): #6 linhas
    for j in range(1, 6): #5 colunas já que estamos sempre em uma
        sensor = verificarFrente()
        if sensor!= Color.GRAY:
            linha, coluna = frente (linha, coluna)
            tabuleiro[linha][coluna]=color_sensor.color()
    direcao = virarPara('B')
    sensor = verificarFrente()
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensor.color()
    if coluna==5: #VIRA PARA O INICIO OU FINAL DO TABULEIRO
        direcao = virarPara('E')
    else:
        direcao = virarPara('D')
print(tabuleiro)