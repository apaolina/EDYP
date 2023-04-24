from .Mesa import Mesa, EstadoMesa
# Esta clase controla todas las mesas que se crearon
class MesaManager():

    mesas: dict[int,Mesa] = {}

    def __init__(self) -> None:
        pass

    def crearMesa(self, capacidad:int) -> Mesa:
        nuevaMesa = Mesa(capacidad)
        MesaManager.mesas.update({nuevaMesa.getId():nuevaMesa})
        return nuevaMesa
    
    def eliminarMesa(self, id: int) -> None:
        MesaManager.mesas.pop(id)

    def requestMesa(self, cantidad: int, response) -> None:
        # Busca dentro de la lista de todas las mesas una que este desocupada y que tenga la capacidad para el grupo que pide
        encontroMesa = False
        for id in range(len(MesaManager.mesas)):
            if(id in MesaManager.mesas):
                if((MesaManager.mesas[id].getEstado() == EstadoMesa.DESOCUPADO) and\
                    (MesaManager.mesas[id].getCapacidad() >= cantidad)):
                    encontroMesa = True
                    MesaManager.mesas[id].ocupar()
                    break

        response(encontroMesa)

    def verEstadoMesas(self) -> dict[str, int]:
        a = 0
        b = 0
        c = 0
        for id in range(len(MesaManager.mesas) + 1):
            if(id in MesaManager.mesas):
                match MesaManager.mesas[id].getEstado():
                    case EstadoMesa.DESOCUPADO:
                        a += 1
                    case EstadoMesa.OCUPADO:
                        b += 1
                    case EstadoMesa.SUCIO:
                        c += 1
                    case other:
                        pass
        
        return {"Desocupado": a, "Ocupado": b, "Sucio": c}