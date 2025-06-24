from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=-Axis.X)

########### MOTORES ###########
motorE = Motor(Port.E, Direction.COUNTERCLOCKWISE)
motorD = Motor(Port.F, Direction.CLOCKWISE)
motorG = Motor(Port.B, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(motorE, motorD, 56, 137)
drive_base.use_gyro(True)
drive_base.settings(straight_speed=300)

########### SENSORES ###########
color_sensorD = ColorSensor(Port.D)
color_sensorE = ColorSensor(Port.C)
Color.BLACK = Color(270, 27, 27)
Color.MY_BLUE = Color(219, 85, 48)
Color.GRAY = Color(235, 23, 60)
Color.MY_YELLOW = Color(60, 42, 98)
Color.MY_RED = Color(353, 82, 87)
Color.MY_GREEN = Color(138, 49, 88)
color_sensorE.detectable_colors((Color.BLACK, Color.WHITE, Color.GRAY, Color.MY_RED, Color.MY_BLUE, Color.MY_YELLOW, Color.MY_GREEN))
color_sensorD.detectable_colors((Color.BLACK, Color.WHITE, Color.GRAY, Color.MY_RED, Color.MY_BLUE, Color.MY_YELLOW, Color.MY_GREEN))

########### VARIAVEIS ###########
n = 5
m = 5
tabuleiro = [[ Color.NONE for _ in range(n)] for _ in range(m)]
linha, coluna = 0, 0
direcao = 'E'

########### FUNCOES ###########
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
        wait(500)
        return dir

def frente(linha, coluna):
    if direcao == 'D':
        coluna+=1
    elif direcao == 'E':
        coluna-=1
    elif direcao == 'B':
        linha+=1
    elif direcao == 'C':
        linha-=1
    
    drive_base.straight(285)
    print(f"Estou em {linha}, {coluna}")
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

    drive_base.straight(20)

def desviaAmarelo(direcao, linha, coluna):
    di=direcao
        if di=="C":
            do="B"
        if di=="B":
            do="C"
        if di=="E":
            do="D"
        if di=="D":
            do="E"
    coluna=coluna-1
    drive_base.straight(-200)
    direcao = virarPara('C')
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensorE.color()
    direcao = virarPara(di)
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensorE.color()
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensorE.color()
    direcao = virarPara('B')
    linha, coluna = frente (linha, coluna)
    tabuleiro[linha][coluna]=color_sensorE.color()
    direcao = virarPara(di)
    return direcao, linha, coluna

########### MAIN ###########
########### IR ATÉ A BORDA (0,0) ###########
alinharPreto()
direcao = virarPara('D')
drive_base.straight(-90)
tabuleiro[linha][coluna]=color_sensorE.color()

for i in range(n):
    for j in range(1,m): 
        if color_sensorD.color()== Color.MY_YELLOW or color_sensorE.color()== Color.MY_YELLOW:
            direcao, linha, coluna = desviaAmarelo(direcao, linha, coluna)
        else:
            linha, coluna = frente (linha, coluna)
            tabuleiro[linha][coluna]=color_sensorE.color()

    ########### ALINHAR NA BORDA NO FINAL DA LINHA ###########   
    alinharPreto()

    ########### MUDAR PARA OUTRA LINHA ###########   
    drive_base.straight(-50)
    direcao = virarPara('B')
    linha, coluna = frente (linha, coluna)

    if coluna>=4:
        direcao = virarPara('D')
        alinharPreto()
        drive_base.straight(-50)
        direcao = virarPara('E')
        drive_base.straight(-100)
    else:
        direcao = virarPara('E')
        alinharPreto()
        drive_base.straight(-50)
        direcao = virarPara('D')
        drive_base.straight(-100)
        
print(tabuleiro)