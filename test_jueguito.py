# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:18:32 2025

@author: mxfer
"""

import unittest
from pygame import image
from jueguito import Carta

# Definir una clase de prueba
class TestCarta(unittest.TestCase):

    def test_voltear(self):
        # Crear una carta con una imagen de prueba
        carta = Carta(1, image.load('sandia.png'), (0, 0))
        
        # Comprobar que inicialmente no está volteada
        self.assertFalse(carta.esta_volteada)
        
        # Voltear la carta
        carta.voltear()
        
        # Comprobar que ahora está volteada
        self.assertTrue(carta.esta_volteada)

    def test_es_par(self):
        # Crear dos cartas con el mismo id
        carta1 = Carta(1, image.load('sandia.png'), (0, 0))
        carta2 = Carta(1, image.load('sandia.png'), (100, 100))
        
        # Comprobar si son iguales (par)
        self.assertTrue(carta1.es_par(carta2))
        
        # Crear una carta diferente
        carta3 = Carta(2, image.load('platano.png'), (200, 200))
        
        # Comprobar si no son iguales
        self.assertFalse(carta1.es_par(carta3))

if __name__ == '__main__':
    unittest.main()
#cambio para el pull de Fer
