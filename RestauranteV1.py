#Se crea la clase Mesa
class Mesa:
    def __init__(self, numero, capacidad, estado):
        self.numero = numero
        self.capacidad = capacidad
        self.estado = estado
        self.cliente = 0
    def ocupar(self):
        self.estado = 'Ocupada'
    def liberar(self):
        self.estado = 'Libre'
        self.cliente = 0
    def getNumero(self):
        return self.numero
    def getCapacidad(self):
        return self.capacidad
    def getEstado(self):
        return self.estado
    def __str__(self):
        return "Mesa: " + str(self.numero) + " Capacidad: " + str(self.capacidad) + " Estado: " + str(self.estado) + " Cliente: " + str(self.cliente)
    def asignar_cliente(self):
        self.cliente = int(input('Ingrese el numero de cliente: '))
        if self.cliente != 0:
            self.ocupar()

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
        
#Se crea la clase Cliente
class Clientes():
    def __init__(self, Numero_cliente, Comensales):
        self.Numero_cliente = Numero_cliente
        self.Comensales = Comensales
        self.Estado_Cliente = 'En espera de mesa'
    def Asignar_mesa_cliente(self):
        self.Estado_Cliente = 'Mesa asignada'
    def Desasginar_mesa_cliente(self):
        self.Estado_Cliente = 'Termino'