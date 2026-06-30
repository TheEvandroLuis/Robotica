from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.pupdevices import ColorLightMatrix
from pybricks.parameters import Icon
from pybricks.geometry import Matrix

hub = PrimeHub(broadcast_channel=120, observe_channels=[125])
matrix_1 = ColorLightMatrix(Port.A)
matrix_2 = ColorLightMatrix(Port.C)
botao = ForceSensor(Port.E)
motor = Motor(Port.B, Direction.CLOCKWISE)
motor_2 = Motor(Port.F, Direction.COUNTERCLOCKWISE)
motor.control.limits(torque=500)
motor_2.control.limits(torque=500)
bandeira = [Color.GREEN, Color.YELLOW, Color.GREEN, Color.YELLOW, Color.BLUE, Color.YELLOW,Color.GREEN, Color.YELLOW, Color.GREEN]

def pegar_bloco_ligar():
    motor.dc(-110)
    motor_2.dc(-110)
    while True:
        dado_recebido = hub.ble.observe(125)
        if dado_recebido == 6:
            pegar_bloco_desligar()
            return 
        wait(50)

def pegar_bloco_desligar():
    motor.brake()
    motor_2.brake()
#70 75 80 85
def soltar_bloco1():
    led(Color.CYAN)
    motor.dc(80)
    motor_2.dc(80)
    wait(500)
    motor.brake()
    motor_2.brake()
    motor.dc(-60)
    motor_2.dc(-60)
    wait(500)
    motor.brake()
    motor_2.brake()
    wait(200)
    led(Color.ORANGE)
def soltar_bloco2():
    led(Color.CYAN)
    motor.dc(83)
    motor_2.dc(83)
    wait(500)
    motor.brake()
    motor_2.brake()
    motor.dc(-60)
    motor_2.dc(-60)
    wait(500)
    motor.brake()
    motor_2.brake()
    wait(200)
    led(Color.ORANGE)
def soltar_bloco3():
    led(Color.CYAN)
    motor.dc(83)
    motor_2.dc(83)
    wait(500)
    motor.brake()
    motor_2.brake()
    motor.dc(-60)
    motor_2.dc(-60)
    wait(500)
    motor.brake()
    motor_2.brake()
    wait(200)
    led(Color.ORANGE)
def soltar_bloco4():
    led(Color.CYAN)
    motor.dc(95)
    motor_2.dc(95)
    wait(500)
    motor.brake()
    motor_2.brake()
    motor.dc(-60)
    motor_2.dc(-60)
    wait(500)
    motor.brake()
    motor_2.brake()
    wait(200)
    led(Color.ORANGE)

def piscarLED(cor):
    matrix_1.on(cor)
    matrix_2.on(cor)
    wait(200)
    matrix_1.on(Color.BLACK)
    matrix_2.on(Color.BLACK)

def led(cor):
    matrix_1.on(cor)
    matrix_2.on(cor)

############ REGISTRA A QUANTIDADE DE COLUNAS A FRENTE ##################
hub.light.on(Color.BLUE) # LED azul: Hub pronto.
valor_a_transmitir = 6
hub.display.number(valor_a_transmitir)
while True:
    # Verifica quais botões estão pressionados
    botoes_pressionados = hub.buttons.pressed()
    if Button.LEFT in botoes_pressionados:
        valor_a_transmitir = 5
        hub.display.number(valor_a_transmitir) # Feedback visual na matriz
        wait(300) # Pequena pausa para evitar leituras múltiplas (debounce)

    # Botão da Direita: Define a variável para 6
    elif Button.RIGHT in botoes_pressionados:
        valor_a_transmitir = 6
        hub.display.number(valor_a_transmitir) # Feedback visual na matriz
        wait(300) # Pequena pausa para evitar leituras múltiplas (debounce)

    if botao.pressed(5):        
        # Envia o valor atual da variável pelo Bluetooth no canal configurado (3)
        hub.ble.broadcast(valor_a_transmitir)
        # Feedback de transmissão na matriz (seta para indicar envio)
        hub.display.icon(Icon.ARROW_RIGHT_UP)
        wait(300)
        # Aguarda a liberação do sensor para evitar spam de transmissão
        while botao.pressed():
            wait(10)
        break
    # Pequena pausa para otimizar o uso da CPU
    wait(10)
hub.light.on(Color.BLACK) # LED azul: Hub pronto.
hub.display.icon(Icon.HAPPY)

############ ESPERA APERTAR O BOTÃO ##################
while not botao.pressed(5):
    led(bandeira)

############ TRANSMITE SINAL PARA INICIAR MOVIMENTO #############
hub.ble.broadcast(True)

while True:
    comando = hub.ble.observe(125)
    if (comando==0): led(Color.BLUE)
    elif (comando==1): led(Color.WHITE)
    elif (comando==2): led(Color.YELLOW)
    elif (comando==3): piscarLED(Color.GREEN)
    elif (comando==4): led(Color.RED)
    elif (comando==5): pegar_bloco_ligar()
    elif (comando==6): pegar_bloco_desligar()
    elif (comando==101):
        soltar_bloco1()
    elif (comando==102):
        soltar_bloco2()
    elif (comando==103):
        soltar_bloco3()
    elif (comando==104):
        soltar_bloco4()

    elif (comando==8): led(bandeira)
    else: led(Color.BLACK)
    print(comando)
    wait(10)
