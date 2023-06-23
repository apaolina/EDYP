#Se crea la clase Menu
# Clase que visualiza los platos disponibles para pedir a los clientes basado en los ingredientes disponibles
import sys
sys.path.insert(0, 'SimClasses')

class Menu:
    def __init__(self): 
        self.Platos_menu = []
        self.dict_platos: dict[str, int] = {}

    def agregar_plato(self, nombre: str, tiempo_coccion:int) -> None:
        self.Platos_menu.append(nombre)
        self.dict_platos[nombre] = tiempo_coccion


    def __str__(self):
        return f"Platos disponibles: {self.Platos_menu}"



