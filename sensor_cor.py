from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
hub = PrimeHub(top_side=Axis.Z, front_side=-Axis.X)

########### CORES ###########
Color.MY_WHITE= Color(200, 15, 97)
Color.MY_BLACK= Color(220, 20, 20)
Color.MY_YELLOW = Color(42, 65, 90)
Color.MY_RED = Color(350, 78, 50)
Color.MY_GREEN = Color(170, 69, 40)
MINHAS_CORES = (Color.MY_WHITE, Color.MY_BLACK, Color.MY_YELLOW, Color.MY_RED, Color.MY_GREEN)
########### SENSORES ###########
color_sensorD = ColorSensor(Port.C)
color_sensorE = ColorSensor(Port.E)
color_sensorL = ColorSensor(Port.A)
color_sensorE.detectable_colors(MINHAS_CORES)
color_sensorD.detectable_colors(MINHAS_CORES)
color_sensorL.detectable_colors(MINHAS_CORES)


########### FUNCOES ###########
################### CALCULAR MÉDIAS #################
def calcular_media_hsv(lista_leituras):
    if not lista_leituras:
        return Color(0, 0, 0)

    total_h = 0
    total_s = 0
    total_v = 0
    
    for cor in lista_leituras:
        total_h += cor.h
        total_s += cor.s
        total_v += cor.v
        
    n = len(lista_leituras)
    
    media_h = total_h // n
    media_s = total_s // n
    media_v = total_v // n
    
    return Color(media_h, media_s, media_v)

########### RETORNA A COR EMBAIXO DO ROBÔ ###########
def ler_cor():
    cor_e = color_sensorE.color()
    cor_d = color_sensorD.color()
    cor_l = color_sensorL.color()
    if cor_e == cor_d and cor_e==cor_l and cor_d==cor_l:
        return cor_e
    else: 
        #drive_base.straight(5)
        cor_e = color_sensorE.color()
        cor_d = color_sensorD.color()
        cor_l = color_sensorL.color()

        for cor_prioritaria in CORES_DE_PRIORIDADE:
            if cor_l == cor_prioritaria:
                return cor_l
            if cor_e == cor_prioritaria:
                return cor_e
            if cor_d == cor_prioritaria:
                return cor_d

leituras_D = []
leituras_M = []
leituras_E = []

for _ in range (20):
    leituras_D.append(color_sensorD.hsv())
    leituras_M.append(color_sensorL.hsv())
    leituras_E.append(color_sensorE.hsv())
    wait(100)

D= calcular_media_hsv(leituras_D)
M= calcular_media_hsv(leituras_M)
E= calcular_media_hsv(leituras_E)

final = calcular_media_hsv([D,M,E])

print(final)