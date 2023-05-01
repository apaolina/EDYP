#Se crea la clase Menu
# Clase que visualiza los platos disponibles para pedir a los clientes basado en los ingredientes disponibles

#class Menu:
#    def __init__(self): 
#        self.listaPlatos = ["Hamburguesa","Pancho"]
    


#    def __str__(self):
#        return 'Nombre del plato: ' + self.nombre + " Precio: " + str(self.precio) + " Ingredientes: " + str(self.ingredientes) + ' Cantidad de cada ingrediente: ' + str(self.cant_ingredientes) + " Tiempo de preparacion: " + str(self.tiempo_preparacion)

#    def agregar_plato(self):
#        self.nombre = str(input("Ingrese el nombre del plato: "))
#        self.precio = int(input("Ingrese el precio del plato: "))
#        cantidad_ingredientes = int(input('Ingrese la cantidad de ingredientes del plato: '))
#        for i in range(cantidad_ingredientes):
#            self.ingredientes.append(str(input("Ingrese los ingredientes del plato: ")))
#            self.cant_ingredientes.append(int(input("Ingrese la cantidad del ingrediente: ")))
#        self.tiempo_preparacion = int(input("Ingrese el tiempo de preparacion del plato: "))


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


