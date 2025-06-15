from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
#####Motores######
motorA= Motor(Port.B, Direction.COUNTERCLOCKWISE)
motorB= Motor(Port.C, Direction.CLOCKWISE)
drive_base= DriveBase(motorA, motorB, 56, 123)
drive_base.settings(straight_speed=100)
drive_base.use_gyro(True)
######Variaveis#####
Alvo=70
Erro=0
VelBase=80
kp=1.2
Cor_da_vezDir= Color.WHITE
Cor_da_vezEsq= Color.WHITE
Cor_da_vezMeio= Color.WHITE

######Sensores######
color_sensorDir=ColorSensor(Port.D)
color_sensorEsq=ColorSensor(Port.E)
color_sensorMeio=ColorSensor(Port.A)
distance_sensor = UltrasonicSensor(Port.F)
color_sensorDir.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN, Color.RED))
color_sensorEsq.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN, Color.RED,))
color_sensorMeio.detectable_colors((Color.BLACK, Color.WHITE, Color.GREEN))

#######Funcoes######
def seguirLinha():
    Erro= color_sensorEsq.reflection() - color_sensorDir.reflection()
    Erro= kp*Erro
    drive_base.drive(VelBase, Erro)

def virarEsq():
    drive_base.straight(50)
    drive_base.turn(-90)

def virarDir():
    drive_base.straight(50)
    drive_base.turn(90)
#######Main#######
while True:
    #if n==1:
     #   drive_base.straight(297)
      #  n=n+1
       ## if color_sensorEsq.color()==Color.WHITE and color_sensorDir.color()==Color.WHITE and color_sensorMeio.color()==Color.WHITE:
            
    print(f"DIR: {color_sensorDir.color()} | MEIO: {color_sensorMeio.reflection()} | ESQ: {color_sensorEsq.color()}")
    Cor_da_vezDir = color_sensorDir.color()
    Cor_da_vezEsq = color_sensorEsq.color()
    
    if Cor_da_vezDir==Color.BLACK or Cor_da_vezEsq==Color.BLACK:
        if Cor_da_vezDir == Color.BLACK and Cor_da_vezEsq == Color.BLACK:
            hub.speaker.beep(400, 100)
            drive_base.straight(50)
            
        if Cor_da_vezDir == Color.BLACK and Cor_da_vezEsq == Color.WHITE:
            drive_base.straight(50)
            drive_base.turn(-10)
            if color_sensorMeio.color()==Color.BLACK:
                hub.speaker.beep(400, 100)
                drive_base.turn(10)
                drive_base.straight(10)
            else:
                drive_base.turn(10)
                drive_base.straight(-70)
                virarDir()
        if Cor_da_vezDir == Color.WHITE and Cor_da_vezEsq == Color.BLACK:
            drive_base.straight(50)
            drive_base.turn(-10)
            if color_sensorMeio.color()==Color.BLACK:
                hub.speaker.beep(400, 100)
                drive_base.turn(10)
                drive_base.straight(10)
            else:
                drive_base.turn(10)
                drive_base.straight(-70)
                virarEsq()

    if Cor_da_vezDir==Color.GREEN or Cor_da_vezEsq==Color.GREEN:
        hub.speaker.beep(700, 100)
        drive_base.stop()
        drive_base.straight(5)
        Cor_da_vezDir = color_sensorDir.color()
        Cor_da_vezEsq = color_sensorEsq.color()
        if Cor_da_vezDir==Color.GREEN and Cor_da_vezEsq==Color.GREEN:
            drive_base.turn(180)
        elif Cor_da_vezEsq==Color.GREEN:
            virarEsq()
        elif Cor_da_vezDir==Color.GREEN:
            virarDir()

    if color_sensorDir.color()==Color.RED or color_sensorEsq.color()==Color.RED:
        hub.speaker.beep(400, 100)
        drive_base.stop()
        break

    ##if color_sensorDir.reflection()==99 and color_sensorEsq.reflection()==99 and color_sensorMeio.reflection()==99:
       # hub.speaker.beep(400, 100)
        #while color_sensorDir.color()!=Color.GREEN:
            #drive_base.straight(10)
        #virarEsq()
        #while color_sensorMeio.color()!=Color.BLACK:
          # drive_base.straight(10)
       # drive_base.straight(50)
        #seguirLinha()

    ##if color_sensorMeio.color()==Color.WHITE:
        #drive_base.turn(-10)
        ##if color_sensorMeio.color()==Color.WHITE:
            ##drive_base.straight(50)
        ##else:
           ## seguirLinha()
    if distance_sensor.distance()<=50:
        drive_base.straight(-70)
        virarEsq()
        drive_base.straight(100)
        virarDir()
        drive_base.straight(270)
        virarDir()
        drive_base.straight(100)
        virarEsq()
        while distance_sensor.distance()>=150:
            seguirLinha()
        drive_base.straight(-70)
        virarDir()
        seguirLinha

    else:
        seguirLinha()