from enum import Enum

# Esta clase contiene los distintos posibles estados de la mesa
class EstadoMesa(Enum):
    DESOCUPADO = 1
    OCUPADO = 2
    SUCIO = 3

# Clase que representa una mesa para que los clientes ocupen y puedan realizar pedidos
class Mesa:
    totalMesas = 0
    
    def __init__(self, capacidad):
        self.id = Mesa.totalMesas
        Mesa.totalMesas += 1
        self.capacidad = capacidad
        self.estado = EstadoMesa.DESOCUPADO

    def ocupar(self) -> None:
        self.estado = EstadoMesa.OCUPADO
        from RestauranteManager import instance
        instance.infoManager.declararEvento("Se ocupo una mesa")
    
    def desocupar(self) -> None:
        self.estado = EstadoMesa.DESOCUPADO
        self.grupoClientes = None
        
    def limpiar(self) -> None:
        self.estado = EstadoMesa.DESOCUPADO # No implementado

    def getId(self) -> int:
        return self.id
    
    def getCapacidad(self) -> int:
        return self.capacidad
    
    def getEstado(self) -> EstadoMesa:
        return self.estado
    
    def __str__(self):
        return "Mesa: " + str(self.id) + " Capacidad: " + str(self.capacidad) + " Estado: " + str(self.estado) + " Cliente: " + str(self.grupoClientes)

    #Esto lo cambiaria en el futuro para el sistema de Request Response que mencione en Trello (Mirar Planeo/herramientas.txt para acceder)
    def asignar_cliente(self):
        self.cliente = int(input('Ingrese el numero de cliente: '))
        if self.cliente != 0:
            self.ocupar()