# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 16:43:12 2024

@author: mxfer
"""
import pygame
import random

#inicializar pygame
pygame.init()

#definir constantes
ANCHO_VENTANA = 600 
ALTO_VENTANA = 700 
MARGEN = 10 
NUM_FILAS = 4 
NUM_COLUMNAS = 4 
TAMAÑO_CARTA = 100 

#colores RGB (R, G, B)
Negro = (0, 0, 0)
Blanco = (255, 255, 255)
Rosa = (255, 158, 249)
Verde = (168, 255, 158)

#Cargar imagenes
imagenes = [
             "sandia.png",
             "platano.png",
             "guayaba.png",
             "tomate.png",
             "manzana.png",
             "uva.png",
             "naranja.png",
             "pera.png"
    ]
imagenes_cartas = [pygame.image.load(img) for img in imagenes]
imagen_reverso = pygame.image.load("cerebro.png")

#rendimiento imagenes a tamaño de las cartas
imagenes_cartas = [pygame.transform.scale(img, (TAMAÑO_CARTA, TAMAÑO_CARTA)) for img in imagenes_cartas]
imagen_reverso = pygame.transform.scale(imagen_reverso, (TAMAÑO_CARTA, TAMAÑO_CARTA))

#clase Pila para manejar las acciones del juego
class Pila:
    def __init__(self):
        self.elementos = []
        
    def push(self, item):
        self.elementos.append(item)
    
    def pop(self):
        if not self.esta_vacia():
            return self.elementos.pop()
        return None
        
    def esta_vacia(self):
        return len(self.elementos) == 0 
    
    def vaciar(self):
        self.elementos = []
        
#clase Cartas que representa cada carta del juego
class Carta:
    def __init__(self, id_carta, imagen_frontal, pos):
        self.id_carta = id_carta #identificador unico de la carta
        self.imagen_frontal = imagen_frontal #imagen cuando la carta esta descubierta
        self.imagen_reverso = imagen_reverso #imagen cuando la carta esta oculta
        self.esta_volteada = False
        self.es_par_encontrado = False #indicador de si es parte de un par ya encontrado
        self.pos = pos #posicion en la pantalla
        
    def voltear(self):
        #metodo para voltear la carta
        if not self.es_par_encontrado: #solo permite volteaar si no es parte de un par ya encontrado
            self.esta_volteada = not self.esta_volteada
            
    def es_par(self, otra_carta):
        #metodo que verifica su otra carta es el par de esta
        return self.id_carta == otra_carta.id_carta
    
    def dibujar(self, ventana):
        #dibujar la carta en la pantalla con un marco negro
        if self.esta_volteada:
            ventana.blit(self.imagen_frontal, self.pos)
        else:
            ventana.blit(self.imagen_reverso, self.pos)
        #dibujar un marco negro alrededor de la carta
        pygame.draw.rect(ventana, Negro, (*self.pos, TAMAÑO_CARTA, TAMAÑO_CARTA), 2)
            
#clase principal del juego
class JuegoMemoria:
    def __init__(self):
        #inicializar la ventana
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Juego de memoria")
        
        self.cartas_seleccionadas = []
        self.pila_movimientos = Pila() #crear una pila para guardar movimientos
        self.cartas = []
        self.mensaje = "" #mensaje que se muestra en pantalla
        self.temporizador = 0 #es un temporizador para controlar el volteo de cartas
        self.ganador = False #variable para indicar si el jugador ha ganado
        
        #crear los botones de reiniciar y salir
        espacio_entre_botones = 20 
        boton_ancho = 120 
        boton_alto = 30 
        
        self.boton_reiniciar = pygame.Rect(ANCHO_VENTANA // 2 - boton_ancho - espacio_entre_botones, 
                                           ALTO_VENTANA - 60, boton_ancho, boton_alto)
        self.boton_salir = pygame.Rect(ANCHO_VENTANA // 2 + espacio_entre_botones, 
                                       ALTO_VENTANA - 60, boton_ancho, boton_alto)
        
        #crear el tablero de cartas
        self.crear_tablero()
        
    def crear_tablero(self):
        #metodo para crear el tablero de cartas del juego
        total_cartas = NUM_FILAS * NUM_COLUMNAS
        cartas_ids = list(range(len(imagenes_cartas))) * 2 #duplicar las cartas
        random.shuffle(cartas_ids)
        
        #distribuir cartas de forma uniforme en la ventana
        espacio_horizontal = (ANCHO_VENTANA - (NUM_COLUMNAS * TAMAÑO_CARTA) - ((NUM_COLUMNAS - 1)*MARGEN))//2 
        espacio_vertical = (ALTO_VENTANA - 100 - (NUM_FILAS * TAMAÑO_CARTA) - ((NUM_FILAS - 1) * MARGEN)) // 2
 
        for fila in range(NUM_FILAS):
            for columna in range(NUM_COLUMNAS):
                id_carta = cartas_ids.pop()
                imagen_frontal = imagenes_cartas[id_carta]
                pos_x = espacio_horizontal + columna * (TAMAÑO_CARTA + MARGEN)
                pos_y = espacio_vertical + fila * (TAMAÑO_CARTA + MARGEN)
                carta = Carta(id_carta, imagen_frontal, (pos_x, pos_y))
                self.cartas.append(carta)
                
    def manejar_eventos(self):
        #metodo para manejar los eventos del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos
                    
                #verificar si se ha clickeado el boton de reinciar
                if self.boton_reiniciar.collidepoint(mouse_x, mouse_y):
                    self.reiniciar_juego()
                        
                #verificar si se ha clickeado el boton de salir
                if self.boton_salir.collidepoint(mouse_x, mouse_y):
                    return False
                
                for carta in self.cartas:
                    if carta.pos[0] <= mouse_x <= carta.pos[0] + TAMAÑO_CARTA and carta.pos[1] <= mouse_y <= carta.pos[1] + TAMAÑO_CARTA:
                        if len(self.cartas_seleccionadas) < 2 and not carta.esta_volteada:
                            carta.voltear()
                            self.cartas_seleccionadas.append(carta)
        return True
        
    def actualizar(self):
        #metodo para actualizar el estado del juego
        if len(self.cartas_seleccionadas) == 2:
            carta1, carta2 = self.cartas_seleccionadas
            if carta1.es_par(carta2):
                self.mensaje = "Es par"
                carta1.es_par_encontrado = True
                carta2.es_par_encontrado = True
                self.cartas_seleccionadas = []
            else:
                self.temporizador += 1
                if self.temporizador > 60: #n = seg * 60 a 60 FPS
                    carta1.voltear()
                    carta2.voltear()
                    self.cartas_seleccionadas = []
                    self.temporizador = 0 
                    self.mensaje = ""   
        #verificar si el jugador ha ganado
        if all(carta.es_par_encontrado for carta in self.cartas):
            self.ganador = True
            self.mensaje = "Ganaste"
        
    def dibujar(self):
        #metodo para sibujar las cartas, los botones y el mensaje en pantalla
        self.ventana.fill(Blanco)
        for carta in self.cartas:
            carta.dibujar(self.ventana)
                
        #dibujar el boton de reinciar
        pygame.draw.rect(self.ventana, Rosa, self.boton_reiniciar)
        fuente = pygame.font.SysFont(None, 36)
        texto_reiniciar = fuente.render("Reiniciar", True, Blanco)
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=self.boton_reiniciar.center)
        self.ventana.blit(texto_reiniciar, texto_reiniciar_rect)
            
        #dibujar el boton de salir
        pygame.draw.rect(self.ventana, Verde, self.boton_salir)
        fuente = pygame.font.SysFont(None, 36)
        texto_salir = fuente.render("Salir", True, Blanco)
        texto_salir_rect = texto_salir.get_rect(center=self.boton_salir.center)
        self.ventana.blit(texto_salir, texto_salir_rect)
            
        #mostrar el mensaje de resultado
        texto_mensaje = fuente.render(self.mensaje, True, Negro)
        self.ventana.blit(texto_mensaje, (ANCHO_VENTANA//2 - 100, 20))
            
        pygame.display.flip()
            
    def reiniciar_juego(self):
        #metodo para reiniciar el juego y reorganizar las cartar
        self.cartas = []
        self.mensaje = ""
        self.ganador = False
        self.temporizador = 0 
        self.crear_tablero()
    
#funcion principal del juego
def main():
    juego = JuegoMemoria()
    reloj = pygame.time.Clock()
    corriendo = True
    while corriendo:
        corriendo = juego.manejar_eventos()
        juego.actualizar()
        juego.dibujar()
        reloj.tick(60) #60 FPS para una animacion mas fluida
    pygame.quit()
        
if __name__ == "__main__":
    main()
            
        
        
        
        
        


#cambio minimo para el pull de nadime
