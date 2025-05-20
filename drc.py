from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

########### FUNCOES ###########
def verificarFrente(): 
    drive_base.drive(50, 0)
    while not color_sensor.color() == (not tabuleiro[linha][coluna] ):
        wait(0)
    drive_base.stop()
    leitura = color_sensor.color()
    drive_base.straight(-150)
    return leitura

def frente(linha, coluna):
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha+=1
    elif direcao == 'C':
        linha-=1
    drive_base.straight(300)

def virarPara(dir):
    if (dir== direcao):
        return
    else: 
        if dir =='B'
            if direcao == 'C':
                drive_base.turn(180)
            elif direcao == 'D':
                drive_base.turn(-90)
            elif direcao == 'E'
                drive_base.turn(90)
        elif dir =='D'
             if direcao == 'C':
                drive_base.turn(-90)
            elif direcao == 'B':
                drive_base.turn(90)
            elif direcao == 'E'
                drive_base.turn(180)
        elif dir =='E'
             if direcao == 'C':
                drive_base.turn(90)
            elif direcao == 'B':
                drive_base.turn(-90)
            elif direcao == 'E'
                drive_base.turn(180)
        elif dir =='C'
             if direcao == 'B':
                drive_base.turn(180)
            elif direcao == 'D':
                drive_base.turn(90)
            elif direcao == 'E'
                drive_base.turn(-90)
        direcao=dir

########### MOTORES/SENSORES ###########
hub = PrimeHub()
motorA = Motor(Port.A, Direction.CLOCKWISE)
motorB = Motor(Port.B, Direction.CLOCKWISE)
global drive_base = DriveBase(motor, motor_2, 56, 114)
global color_sensor = ColorSensor(Port.C)
global tabuleiro = [ [Color.NONE for _ in range(6)] for _ in range(6)]
global linha = 0
global coluna = 0
global direcao = 'E'

########### MAIN ###########
########### INDO PARA O (0,0) ###########
while verificarFrente() != Color.GRAY: ##PENSAR O QUE FAZER CASO TENHA ALGUM QUADRADO Y/G NO CAMINHO
    frente()

########### ESTOU EM (0,0) ###########
virarPara('D')
tabuleiro[linha][coluna] = color_sensor.color() #

for i in range(6): #6 linhas
    for j in range(1, 6): #5 colunas já que estamos sempre em uma
        sensor = verificarFrente()
        if sensor!= Color.GRAY:
            tabuleiro[linha][coluna]=sensor
            frente
    virarPara('B')
    sensor = verificarFrente()
    frente()
    if coluna==5: #VIRA PARA O INICIO OU FINAL DO TABULEIRO
        direcao='E'
    else:
        direcao='D'
    print(tabuleiro)
    break