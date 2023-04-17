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
   
        

