#!/usr/bin/env python

# sudo apt-get install ros-noetic-rosserial-arduino

# rosrun rosserial_python serial_node.py /dev/ttyACM0

# sudo chmod 666 /dev/ttyACM0  

# https://www.youtube.com/watch?v=9qZUjEsVWts&ab_channel=AleksandarHaber (9:11)

# rostopic pub /motor_control std_msgs/String "data: '00'"



import sys
import rospy
import termios
import tty
import select

from std_msgs.msg import String


# MENSAJE INICIAL
msg = """
Mapa de teclas:
---------------------------
     q   w  e 
   a          d
         s   
---------------------------

u = sube pistón
j = baja pistón
k o h = STOP


CTRL-C para salir.
"""
# MAPEO DE TECLAS

moveBindings = {
    # X, Y, Theta

    'w': "11",        # Frente
    'a': "20",        # Izquierda
    'd': "02",        # Derecha
    's': "00",        # Detengo
    'e': "01",        # Giro pequeño derecha
    'q': "10",        # Giro pequeño izquierda
    'u': "u",        # Subo pistón
    'j': "d",        # Bajo pistón
    'k': "s",        # Detengo pistón
    'h': "s",        # Detengo pistón
    'p': "p",        # Perforar
    'l': "l"         # Dejar de perforar
}


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


# MAIN

if __name__ == "__main__":

    settings = termios.tcgetattr(sys.stdin)

    # PUBLISHER EN /motor_control UTILIZANDO LOS VALORES DE STRING

    pub = rospy.Publisher('/motor_control', String, queue_size=10)

    # INICIALIZA EL NODO: teleop_twist_keyboard
    rospy.init_node('teleoper', anonymous=False)

    try:
        # Imprime el mensaje
        print(msg)

        while(1):
            # Asigna a key los valores del vector de la tecla presionada
            key = getKey()

            # Obtiene los valores de x, y, z y th del vector key
            if key in moveBindings.keys():
                instruction = moveBindings[key]

            # Si no se presiona ninguno, x, y, z y theta serán defaulteados a 0.
            else:
                instruction = "00"
                if (key == '\x03'):
                    break

            # Se publica la instrucción
            pub.publish(instruction)

    finally:
        # Se publica la instrucción de parada antes de terminar
        pub.publish("00")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
