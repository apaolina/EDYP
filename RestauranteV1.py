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