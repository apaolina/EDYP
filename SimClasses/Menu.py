#Se crea la clase Menu
# Clase que visualiza los platos disponibles para pedir a los clientes basado en los ingredientes disponibles

from Plato import Platos

class Menu:
    def __init__(self): 
        self.Platos_menu = []

    def agregar_plato(self):
        nuevo_plato = Platos()
        self.Platos_menu.append(nuevo_plato)
        print("El plato {} ha sido añadido al menú.".format(nuevo_plato.nombre))

    def eliminar_plato(self):
        plato_eliminar = str(input("Ingrese el nombre del plato que desea eliminar: "))
        for plato in self.Platos_menu:
            if plato.nombre == plato_eliminar:
                self.Platos_menu.remove(plato)
        print("El plato {} ha sido eliminado del menú.".format(plato_eliminar))       
        
    def mostrar_menu(self):
        for plato in self.Platos_menu:
            print("Nombre del plato: {}".format(plato.nombre))
            print("Precio: ${}".format(plato.precio))
            print("Tiempo de preparación: {}min".format(plato.tiempo_preparacion))
            print("Ingredientes: {}".format(plato.ingredientes))
            print("Cantidades de cada ingrediente: {}".format(plato.cant_ingredientes))

MenuRestaurante = Menu()


