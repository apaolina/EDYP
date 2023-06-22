import sys
sys.path.insert(0, r'./SimClasses')
from Mesa import Mesa, EstadoMesa
# Esta clase controla todas las mesas que se crearon
class MesaManager():

    def __init__(self) -> None:
        self.mesas: dict[int,Mesa] = {}
        pass

    def crearMesa(self, capacidad:int) -> Mesa:
        nuevaMesa = Mesa(capacidad)
        self.mesas.update({nuevaMesa.getId():nuevaMesa})
        return nuevaMesa
    
    def eliminarMesa(self, id: int) -> None:
        self.mesas.pop(id)

    def requestMesa(self, cantidad: int, response) -> None:
        # Busca dentro de la lista de todas las mesas una que este desocupada y que tenga la capacidad para el grupo que pide
        encontroMesa = False
        mesaId = -1
        for id in range(len(self.mesas)):
            if(id in self.mesas):
                if((self.mesas[id].getEstado() == EstadoMesa.DESOCUPADO) and\
                    (self.mesas[id].getCapacidad() >= cantidad)):
                    encontroMesa = True
                    self.mesas[id].ocupar()
                    mesaId = id
                    break

        response(encontroMesa,mesaId)

    def desocuparMesa(self, id: int) -> None:
        self.mesas[id].estado = EstadoMesa.DESOCUPADO

    def verEstadoMesas(self) -> dict[str, int]:
        a = 0
        b = 0
        c = 0
        for id in range(len(self.mesas) + 1):
            if(id in self.mesas):
                match self.mesas[id].getEstado():
                    case EstadoMesa.DESOCUPADO:
                        a += 1
                    case EstadoMesa.OCUPADO:
                        b += 1
                    case EstadoMesa.SUCIO:
                        c += 1
                    case other:
                        pass
        
        return {"Desocupado": a, "Ocupado": b, "Sucio": c}
    
    def __str__(self) -> str:
        return f"Mesas: {self.mesas}"