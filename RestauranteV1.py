#Se crea la clase Mesa
class Mesa:
    def __init__(self, numero, capacidad, estado):
        self.numero = numero
        self.capacidad = capacidad
        self.estado = estado
    def reservar(self):
        self.estado = 'Reservada'
    def ocupar(self):
        self.estado = 'Ocupada'
    def liberar(self):
        self.estado = 'Libre'
    def getNumero(self):
        return self.numero
    def getCapacidad(self):
        return self.capacidad
    def getEstado(self):
        return self.estado
    def __str__(self):
        return "Mesa: " + str(self.numero) + " Capacidad: " + str(self.capacidad) + " Estado: " + self.estado

#Se crea la clase Personal
class Personal:
    def __init__(self, nombre, cargo, estado, asignado_mesas):
        self.nombre = nombre
        self.cargo = cargo
        self.estado = estado
        self.asignado_mesas = asignado_mesas
    def __str__(self):
        return self.nombre + " " + self.cargo + " " + self.estado
    def asignar_mesa(self, mesa):
        self.asignado_mesas.append(mesa)
    def desasignar_mesa(self, mesa):
        self.asignado_mesas.remove(mesa)
    def get_asignado_mesas(self):
        return self.asignado_mesas
    def promover(self, cargo):
        self.cargo = cargo
    def despedir(self):
        self.estado = "Despedido"
    def contratar(self):
        self.estado = "Activo"
        
#Se crea la clase Menu
class Menu:
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