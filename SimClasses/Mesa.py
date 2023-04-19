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
        self.id = Mesa.totalMesas + 1
        Mesa.totalMesas += 1
        self.capacidad = capacidad
        self.estado = EstadoMesa.DESOCUPADO

    def ocupar(self) -> None:
        self.estado = EstadoMesa.OCUPADO
    
    def desocupar(self) -> None:
        self.estado = EstadoMesa.SUCIO
        self.grupoClientes = None
        
    def limpiar(self) -> None:
        self.estado = EstadoMesa.DESOCUPADO

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

# Esta clase controla todas las mesas que se crearon
class MesaController():

    mesas: dict[int,Mesa] = {}

    def __init__(self) -> None:
        pass

    def crearMesa(self, capacidad:int) -> Mesa:
        nuevaMesa = Mesa(capacidad)
        MesaController.mesas.update({nuevaMesa.getId():nuevaMesa})
        return nuevaMesa
    
    def eliminarMesa(self, id: int) -> None:
        MesaController.mesas.pop(id)

    def requestMesa(self, cantidad: int, response) -> None:
        # Busca dentro de la lista de todas las mesas una que este desocupada y que tenga la capacidad para el grupo que pide
        encontroMesa = False
        for id in range(len(MesaController.mesas) + 1):
            if(id in MesaController.mesas):
                if((MesaController.mesas[id].getEstado() == EstadoMesa.DESOCUPADO) and\
                    (MesaController.mesas[id].getCapacidad() >= cantidad)):
                    encontroMesa = True
                    MesaController.mesas[id].ocupar()
                    break

        response(encontroMesa)

    def verEstadoMesas(self) -> dict[str, int]:
        a = 0
        b = 0
        c = 0
        for id in range(len(MesaController.mesas) + 1):
            if(id in MesaController.mesas):
                match MesaController.mesas[id].getEstado():
                    case EstadoMesa.DESOCUPADO:
                        a += 1
                    case EstadoMesa.OCUPADO:
                        b += 1
                    case EstadoMesa.SUCIO:
                        c += 1
                    case other:
                        pass
        
        return {"Desocupado": a, "Ocupado": b, "Sucio": c}