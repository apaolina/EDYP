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
    