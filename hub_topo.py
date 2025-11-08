from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import ColorLightMatrix
from pybricks.parameters import Icon
from pybricks.geometry import Matrix

def pegar_bloco():
    drive_base.drive(250, 0)
    wait(2000)
    drive_base.stop()

def soltar_bloco(bloco):
    if bloco==1:
        drive_base.drive(-200, 0)
        wait(600)
        drive_base.stop()
    elif bloco==2:
        drive_base.drive(-225, 0)
        wait(600)
        drive_base.stop()
    elif bloco==3:
        drive_base.drive(-250, 0)
        wait(600)
        drive_base.stop()
    else:
        drive_base.drive(-300, 0)
        wait(600)
        drive_base.stop()

    wait(1000)
    drive_base.drive(250, 0)
    wait(1000)
    drive_base.stop()

def piscarLED(cor):
    matrix_1.on(cor)
    matrix_2.on(cor)
    wait(400)
    matrix_1.on(Color.BLACK)
    matrix_2.on(Color.BLACK)
    wait(400)

hub = PrimeHub(broadcast_channel=120, observe_channels=[125])
matrix_1 = ColorLightMatrix(Port.A)
matrix_2 = ColorLightMatrix(Port.C)
botao = ForceSensor(Port.E)
motor = Motor(Port.B, Direction.CLOCKWISE)
motor_2 = Motor(Port.F, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(motor, motor_2, 56, 114)
bandeira = [Color.GREEN, Color.YELLOW, Color.GREEN, Color.YELLOW, Color.BLUE, Color.YELLOW,Color.GREEN, Color.YELLOW, Color.GREEN]

############ ESPERA APERTAR O BOTÃO ##################
while not botao.pressed(5):
    matrix_1.on(bandeira)
    matrix_2.on(bandeira)

############ TRANSMITE SINAL PARA INICIAR MOVIMENTO #############
hub.ble.broadcast(True)

while True:
    cor_recebida = hub.ble.observe(125)
    if cor_recebida == 1: piscarLED(Color.YELLOW)
    elif cor_recebida == 2: piscarLED(Color.RED)
    elif cor_recebida == 3: 
        for _ in range (5):
            piscarLED(Color.GREEN)
    elif cor_recebida == 4: 
        matrix_1.on(Color.WHITE)
        matrix_2.on(Color.WHITE)
    elif cor_recebida == 5: 
        matrix_1.on(Color.BLACK)
        matrix_2.on(Color.BLACK)
    elif cor_recebida == 6:
        matrix_1.on(bandeira)
        matrix_2.on(bandeira)