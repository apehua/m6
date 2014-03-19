# -*- encoding: utf-8 -*-

import pilas

def dibujar(unRobot):
        unRobot.forward(100, 2)
        unRobot.turnRight(100, 1.5)


pilas.iniciar()            
b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b, 1)

for i in range(0, 4):
    dibujar(b)

pilas.ejecutar()
