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

mesa1 = Mesa(1, 4, 'Libre')
mesa1.asignar_cliente()
print(mesa1.cliente)
print(mesa1)
mesa1.liberar()
print(mesa1)