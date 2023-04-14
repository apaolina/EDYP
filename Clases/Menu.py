#Se crea la clase Menu
class Platos:
    def __init__(self): 
        self.nombre = ''
        self.precio = 0
        self.ingredientes = []
        self.tiempo_preparacion = 0
    
    def __str__(self):
        return 'Nombre del plato: ' + self.nombre + " Precio: " + str(self.precio) + " Ingredientes: " + str(self.ingredientes) + " Tiempo de preparacion: " + str(self.tiempo_preparacion)
    def agregar_plato(self):
        self.nombre = str(input("Ingrese el nombre del plato: "))
        self.precio = int(input("Ingrese el precio del plato: "))
        cantidad_ingredientes = int(input('Ingrese la cantidad de ingredientes del plato: '))
        for i in range(cantidad_ingredientes):
            self.ingredientes.append(str(input("Ingrese los ingredientes del plato: ")))
        self.tiempo_preparacion = int(input("Ingrese el tiempo de preparacion del plato: "))

plato1 = Platos()
plato1.agregar_plato()
print(plato1)

