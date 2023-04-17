#Se crea la clase Menu
# Clase que visualiza los platos disponibles para pedir a los clientes basado en los ingredientes disponibles
class Menu:
    def __init__(self): 
        self.nombre = ''
        self.precio = 0
        self.ingredientes = []
        self.tiempo_preparacion = 0
        self.cant_ingredientes = []
    
    def __str__(self):
        return 'Nombre del plato: ' + self.nombre + " Precio: " + str(self.precio) + " Ingredientes: " + str(self.ingredientes) + ' Cantidad de cada ingrediente: ' + str(self.cant_ingredientes) + " Tiempo de preparacion: " + str(self.tiempo_preparacion)
    def agregar_plato(self):
        self.nombre = str(input("Ingrese el nombre del plato: "))
        self.precio = int(input("Ingrese el precio del plato: "))
        cantidad_ingredientes = int(input('Ingrese la cantidad de ingredientes del plato: '))
        for i in range(cantidad_ingredientes):
            self.ingredientes.append(str(input("Ingrese los ingredientes del plato: ")))
            self.cant_ingredientes.append(int(input("Ingrese la cantidad del ingrediente: ")))
        self.tiempo_preparacion = int(input("Ingrese el tiempo de preparacion del plato: "))

plato1 = Menu()
plato1.agregar_plato()
print(plato1)
