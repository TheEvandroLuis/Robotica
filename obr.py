from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
#####Motores######
motorA= Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorB= Motor(Port.C, Direction.CLOCKWISE)
drive_base= DriveBase(motorA, motorB, 56, 81)
drive_base.use_gyro(True)
######Variaveis#####
Alvo=50
Erro=0
VelBase=75
Kp=1
Cor_da_vezDir= Color.WHITE
Cor_da_vezEsq= Color.WHITE
Cor_da_vezMeio= Color.WHITE

Color.BLACK=Color(220, 17, 42)
Color.GREEN=Color(146, 73, 83)
Color.WHITE=Color(60, 0, 99)

######Sensores######
color_sensorDir=ColorSensor(Port.D)
color_sensorEsq=ColorSensor(Port.F)
color_sensorMeio=ColorSensor(Port.A)
color_sensorDir.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN))
color_sensorEsq.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN))
color_sensorMeio.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN))

#######Funcoes######
def seguirLinha():
    Erro= color_sensorMeio.reflection() - Alvo
    Erro= Kp*Erro
    drive_base.drive(VelBase, Erro)

def virarEsq():
    drive_base.straight(80)
    drive_base.turn(-95)

def virarDir():
    drive_base.straight(80)
    drive_base.turn(95)

#######Main#######

while True:
    Cor_da_vezDir= color_sensorDir.color()
    Cor_da_vezEsq= color_sensorEsq.color()
    Cor_da_vezMeio= color_sensorMeio.color()
    if Cor_da_vezDir==Color.GREEN and Cor_da_vezEsq==Color.GREEN:
        drive_base.turn(180)
    elif Cor_da_vezEsq==Color.GREEN:
        drive_base.straight(10)
        if Cor_da_vezDir==Color.WHITE and Cor_da_vezEsq==Color.WHITE:
            seguirLinha()
        elif Cor_da_vezDir==Color.BLACK or Cor_da_vezEsq==Color.BLACK:
            drive_base.turn(-95)
    elif Cor_da_vezDir==Color.GREEN:
        drive_base.straight(10)
        if Cor_da_vezDir==Color.WHITE and Cor_da_vezEsq==Color.WHITE:
            seguirLinha()
        elif Cor_da_vezDir==Color.BLACK or Cor_da_vezEsq==Color.BLACK:
            drive_base.turn(95)
    else:
        seguirLinha()
    if Cor_da_vezDir==Color.BLACK and Cor_da_vezEsq==Color.WHITE:
        drive_base.straight(70)
        if Cor_da_vezMeio==Color.BLACK:
            seguirLinha()
        elif Cor_da_vezMeio==Color.WHITE:
            drive_base.turn(95)
            seguirLinha()
    elif Cor_da_vezEsq==Color.BLACK and Cor_da_vezDir==Color.WHITE:
        drive_base.straight(70)
        if Cor_da_vezMeio==Color.BLACK:
            seguirLinha()
        elif Cor_da_vezMeio==Color.WHITE:
            drive_base.turn(-95)
            print(f"E: {color_sensorEsq.color()} | M: {color_sensorMeio.color()} | D: {color_sensorDir.color()}")