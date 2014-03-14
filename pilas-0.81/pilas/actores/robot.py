# -*- encoding: utf-8 -*-
import pilas
import time
from pilas.actores import Actor
from pilas.fondos import  *
from pilas.actores import Pizarra
from funciones_robot import *
from pilas.utils import distancia_entre_radios_de_colision_de_dos_actores

import sys
from PyQt4 import QtGui, QtCore, uic

class Sense(QtGui.QMainWindow):
    def __init__(self, unRobot):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi("/usr/local/lib/python2.7/dist-packages/pilas-0.81-py2.7.egg/pilas/data/senses.ui")
        self.activo = True       
        self._mostrarInfo(unRobot) 
        self.ui.show()
           
    #Definición de un evento para la salida del programa
    def closeEvent(self, event):
        self.activo = False   
        event.accept()       

    def _mostrarInfo(self, unRobot):
        
        def mostrarBateria():
            self.ui.batery.display(  '%0.2f' %  unRobot.batery())
            return self.activo

        def mostrarPing():
            self.ui.nping.display(  '%0.2f' %  unRobot.ping())
            return self.activo

        def mostrarSensoresDeLinea():
            izq, der = unRobot.getLine()
            self.ui.iline.display(  '%0.2f' %   izq)
            self.ui.dline.display( '%0.2f' %   der)
            return self.activo

        pilas.escena_actual().tareas.condicional(3, mostrarBateria)
        pilas.escena_actual().tareas.condicional(1, mostrarPing)
        pilas.escena_actual().tareas.condicional(1, mostrarSensoresDeLinea)
            

#### Robot

class Robot(Actor):

    def __init__(self,board, robotid=0, x=0, y=0):
        self.pizarra = pilas.actores.Pizarra()

        imagen = pilas.imagenes.cargar('RobotN6.png')
        Actor.__init__(self, imagen, x=x, y=y)
        self.rotacion = 270
        self.velocidad = 3
        self.pasos = 1
        self.anterior_x = x
        self.anterior_y = y
        self.bajalapiz()
	self.aprender(pilas.habilidades.Arrastrable)
	self.radio_de_colision = 31
        self.color = pilas.colores.negro
	self.bajalapiz()
        self.tiempo = 0	
#       self.aprender(pilas.habilidades.SeguidoPorLaCamara)
        self.aprender(pilas.habilidades.SeMantieneEnPantalla)
        """ Inicializa el robot y lo asocia con la placa board. """
        self.robotid = robotid
        self.board = board
        self.name = ''
	self.board.agregarRobot(self)
        self.tarea = None
    
    # Redefinir el método eliminar de la clase Actor para que lo elimine también de la lista de robots de Board    
    def eliminar(self):
        self.board.eliminarDeLaLista(self)
	Actor.eliminar(self)

    ## Movimiento horizontal y vertical

    def setVelocidad(self, valor):
   	""" Asigna una velocidad de movimiento real al robot """
	if ((valor % 2 == 0) and (valor % 10 == 0)):
	    self.velocidad = valor / 10 / 2
	else:
	    cvalor = valor / 10
	    self.velocidad = (cvalor / 2 ) + 1  
	
    def velocidadValida(self, vel, exta, extb):
        return ((vel >= exta) & (vel <= extb))

    def forward(self, vel=50, seconds=-1):
        """ El robot avanza con velocidad vel durante seconds segundos. """
        if not (self.tarea is None):
            self.tarea.terminar()
        self.board.mover(self, vel,  seconds)
    
    def realizarMovimiento(self, vel, seconds):
        """ El robot avanza con velocidad vel durante seconds segundos. """
	
        def adelanteSinTiempo():
            self.hacer(pilas.comportamientos.Avanzar(self.velocidad, self.velocidad))
            return (self.movimiento)

        def atrasSinTiempo():
            self.hacer(pilas.comportamientos.Retroceder(self.velocidad, self.velocidad))
            return (self.movimiento)

	self.stop()
	self.setVelocidad(vel) 
            
	if (self.velocidadValida(vel, 10, 100)) :
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, adelanteSinTiempo)
            if (seconds != -1):
                wait(seconds)
                self.stop()                 
        elif (self.velocidadValida(vel, -100, -10)) : 
            self.movimiento = True
            self.tarea = pilas.escena_actual().tareas.condicional(0.1, atrasSinTiempo)
            self.velocidad = self.velocidad * -1
            if (seconds != -1):   
                wait(seconds)
                self.stop()
        else:
            print   """ Rangos de velocidades válidas:
                                -100 a -10
                                  10 a 100   """
    
	
    def backward(self, vel=50, seconds=-1):
	""" El robot retrocede con velocidad vel durante seconds segundos.  """
        if not (self.tarea is None):
            self.tarea.terminar()
	self.board.mover(self, -vel, seconds)

    ## Movimiento de giro
    def turnRight(self, vel=50, seconds=-1):
        self.stop()
        """ El robot gira a la derecha con velocidad vel durante seconds segundos. """
        self.board.girar(self, vel, seconds)

    def realizarGiro(self, vel, seconds):
             
        def izquierdaSinTiempo():
            self.hacer_luego(pilas.comportamientos.Girar(-abs(self.velocidad), self.velocidad))
            return (self.movimiento)
      
        def derechaSinTiempo():
            self.hacer_luego(pilas.comportamientos.Girar(abs(self.velocidad), self.velocidad))
            return (self.movimiento)

        self.stop()
        self.setVelocidad(vel)
	

	if (self.velocidadValida(vel, 10, 100)) :
            self.movimiento = True
            pilas.escena_actual().tareas.condicional(0.1, derechaSinTiempo)
            if (seconds != -1): 
                wait(seconds)
                self.stop()            
        elif (self.velocidadValida(vel, -100, -10)) :
            self.movimiento = True
            pilas.escena_actual().tareas.condicional(0.1, izquierdaSinTiempo)
            self.velocidad = self.velocidad * -1
            if (seconds != -1):
                 wait(seconds)
                 self.stop()                  
        else:                 
            print   """ Rangos de velocidades válidas:
                                -100 a -10
                                  10 a 100   """

   
    def turnLeft(self, vel=50, seconds=-1):
        """ El robot gira a la izquierda con velocidad vel durante seconds segundos. """
        self.stop()
        self.board.girar(self, -vel, seconds)
    
 
    def beep(self, freq=200, seconds=0):
        """ Hace que el robot emita un pitido con frecuencia freq durante seconds segundos.""" 

        amplitud = 58
        sample = 8000
        half_period = int(sample/freq / 2)
        beep = chr(amplitud)*half_period+chr(0)*half_period
        beep *= int(seconds * freq)
        audio = file('/dev/audio', 'wb')
        audio.write(beep)
        audio.close()
        
    def detenerse(self):
        self.movimiento = False

    def stop(self):
        self.board.detener(self)    
    
    def batery(self):
        """ Devuelve el voltaje de las baterías del robot. """
        return 0
    
## Sensores
## Cuadrantes:      xy 
          #   1  -> ++ 
          #   2  -> +- 
          #   3  -> --
          #   4  -> -+
    def actores_cuadrante_1(self):
        actores = []
        # print "dentro de cuadrante 1"
        for actor in pilas.escena_actual().actores:
            # print actor
	    if ((id(actor) != id(self)) and  (actor.x >= self.x and actor.y >= self.y) and actor_no_valido(actor)):
                actores.append(actor)
                # print actor
	return actores

    def actores_cuadrante_2(self):
        actores = []
        # print "dentro del cuadrante 2"
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self)  and  (actor.x >= self.x and actor.y <= self.y) and actor_no_valido(actor)):
                    actores.append(actor)
        return actores

    def actores_cuadrante_3(self):
        # print "dentro del cuadrante 3"
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self) and (actor.x <= self.x and actor.y <= self.y) and actor_no_valido(actor)):
                    actores.append(actor)
        return actores

    def actores_cuadrante_4(self):
        # print "dentro del cuadrante 4"
        actores = []
        for actor in pilas.escena_actual().actores:
            if (id(actor) != id(self) and (actor.x <= self.x and actor.y >= self.y) and actor_no_valido(actor)):
                    actores.append(actor)
        return actores
    
    def _buscarActoresEnCadaCuadrante(self, cuadrante):
        actores = []
       
        if cuadrante == 1 :
            # print " _buscarActoresEnCadaCuadrante 1"
            actores = self.actores_cuadrante_1()
        elif cuadrante == 2:
            actores = self.actores_cuadrante_2()  
            # print " _buscarActoresEnCadaCuadrante 2"
        elif cuadrante == 3:
            actores = self.actores_cuadrante_3()
            # print " _buscarActoresEnCadaCuadrante  3 "
        else:
	    actores = self.actores_cuadrante_4()
            # print " _buscarActoresEnCadaCuadrante   4 "
        return actores
    
     
    def _analizarDistanciaEntreActores(self):
        cua = evaluarCuadrante(self)
        # print "cuadrante del robot ", cua
        valor = 100
        actores = self._buscarActoresEnCadaCuadrante(cua)
        dis = -1
         
        ## Recorre la lista de actores de la escena y saca la distancia de todos los que son perpendiculares a robot 
        for actor in actores:
             cuac = evaluarCuadrante(actor)
             # print "cuadrante del actor", cuac
             actorA, actorB = puntosParaLaRecta(actor)
             robotA, robotB = puntosParaLaRecta(self)
             # print "puntos del acto: x, y ",  actorA, actorB 
             # print "puntos del actor robot x, y ",  robotA, robotB
             if (evaluarPerpendicularidadDeObjetos(self, actor, robotA, robotB, actorA, actorB)) :
                 ## Los actores tienen sus rectas perpendiculares 
                  # print "Las rectas son perpendiculares"
                  actorA, actorB = puntosParaLaRecta(actor)                
                  rectaX, rectaY = self.crerLasRectasEncontrarLosPuntosEnLosQueSeCortan(actorA, actorB, actor, robotA, robotB)
                  if (self.evaluarPosicionDelPuntoDeInterseccionYElSegmentoDelActor(rectaX, rectaY, actor,  cua )): 
                        # print "es un obstaculo"
                        dis = distancia_entre_radios_de_colision_de_dos_actores(self, actor)
                        if (dis <= valor):
                             valor = dis
        
        if  (dis == -1) :
           # No hay actores frente al robot 
            return  -1
        else:
            return valor 
    
    
       
    def getObstacle(self, distance=100):
        """ Devuelve True si hay un obstaculo a menos de distance
        centimetros del robot. """

        valor = self._analizarDistanciaEntreActores()
        # print valor
        if valor == -1:
            return False 
        else:
            return valor <=  distance
    
                                        
 
    def crerLasRectasEncontrarLosPuntosEnLosQueSeCortan(self, otroRobotX, otroRobotY, unActor, otroPuntoActorX, otroPuntoActorY ) :
        
        # if ((self.x - otroRobotX)  == 0 ): 
           # El robot está en una recta vertical
           

### otro caso es que si el de la recta vertical es el actor,  la verificación es otra



           # entonces no necesito sacar la intersección  
        # Recta robot
        pendienteRobot = (self.y - otroRobotY ) / (self.x - otroRobotX )
        independienteRobat = ( pendienteRobot * pendienteRobot ) - self.y
        # ecuación: y = pendienteRobot.x + independienteRobat

        # Recta Actor
        pendienteActor = (unActor.y - otroPuntoActorY ) / ( unActor.x - otroPuntoActorX )
        independienteActor = pendienteActor  *  pendienteActor  - unActor.y

        # Determinar el valor en que se cortan las rectas
        # Sacar el valor de X
        x = independienteRobat - independienteActor
        indep = independienteRobat - independienteActor
        valorX = x / indep

        # Sacar el valor de Y
        valorY = (pendienteRobot * valorX)  +  independienteRobat
        
        # Devolver los puntos en los que se corta las rectas

        return (valorX, valorY)


    def evaluarPosicionDelPuntoDeInterseccionYElSegmentoDelActor(self, puntoX, puntoY, unActor, cuadrante):
        # Ya se que son perpendiculares y también conozco el punto en que se interconectan
        print cuadrante  
        print "punto donde se sruzan los puntos", puntoX, puntoY

        if ( (cuadrante == 1 ) ):
            return ((puntoX >= unActor.x - unActor.radio_de_colision ) and ( puntoX <= unActor.x + unActor.radio_de_colision))
        else: 
            return ((puntoY >= unActor.y - unActor.radio_de_colision) and (puntoY <= unActor.y + unActor.radio_de_colision))
 

    def ping(self):
        """ Devuelve la distancia en centimetros al objeto frente al robot. """
	return self._analizarDistanciaEntreActores()
     
    def _determinar_pixel_por_cuadrante(self, cuadrante):
        if cuadrante == 1 :
            
            return (self.x - 2, self.y + 30, self.x + 2, self.y + 30, )
        else:
            if cuadrante == 2:
                return (self.x + 30, self.y + 2, self.x + 30, self.y - 2)
            else:
                if cuadrante == 3:
                    return (self.x + 2, self.y - 30, self.x - 2, self.y - 30)
                else:
                    return (self.x - 30, self.y - 2, self.x - 30, self.y + 2)


    def getLine(self):
        """ Devuelve los valores de los sensores de linea. """
        
        ancho, alto =  pilas.mundo.get_gestor().escena_actual().get_fondo().dimension_fondo()
        xa, ya, xb, yb =self._determinar_pixel_por_cuadrante(evaluarCuadrante(self))
   
        vi = 0     
        ximagen = ancho / 2 + xa
        yimagen = alto / 2 - ya
        valores = pilas.mundo.get_gestor().escena_actual().get_fondo().informacion_de_un_pixel(ximagen, yimagen)
        for i in valores:
             vi = vi + i

        vd = 0
        ximagen = ancho / 2 + xb
        yimagen = alto / 2 - yb
        valores = pilas.mundo.get_gestor().escena_actual().get_fondo().informacion_de_un_pixel(ximagen, yimagen)
        for i in valores:
            vd = vd + i
        
        return (vi / 3.0 , vd / 3.0)
    
    def senses(self):
                
	ventana = Sense(self)
      
       
    ## Identificadores
    
    def setId(self, newid):
        """  Setea el robotid  """
        self.robotid = newid

    def setName(self, name):
        """ Setea el nombre para el robot. """
        self.name = str(name)

    def getId(self):
        """  Devuelve el robotid. """
        return self.robotid

    def getName(self):
        """ Devuelve el nombre del robot. """
        return self.name

    ## Otras funciones
    
    def speak(self, msj):
        """ Imprime en la terminal el mensaje msj. """
        print msj


    
    ## Aspectos del Actor

    def actualizar(self):
        if self.anterior_x != self.x or self.anterior_y != self.y:
            self.dibujar_linea_desde_el_punto_anterior()
            self.anterior_x = self.x
            self.anterior_y = self.y

    def dibujar_linea_desde_el_punto_anterior(self):
        self.pizarra.linea(self.anterior_x, self.anterior_y, self.x, self.y, self.color, grosor=4)
    
    def bajalapiz(self):
        self.lapiz_bajo = True

    def subelapiz(self):
        self.lapiz_bajo = False

    def pon_color(self, color):
        self.color = color
        return self._color

    def set_color(self, color):
        self._color = color
    
    def get_color(self):
        return self._color
        
    color = property(get_color, set_color)

    def pintar(self, color=None):
        self.pizarra.pintar(color)
                

   
