from SimClasses import Mesa as m, Persona as p

# Esta clase controla todas las mesas que se crearon
class MesaController():

    mesas: dict[int,m.Mesa] = {}

    def __init__(self) -> None:
        pass

    def crearMesa(self, capacidad:int) -> m.Mesa:
        nuevaMesa = m.Mesa(capacidad)
        MesaController.mesas.update({nuevaMesa.getId:nuevaMesa})
        return nuevaMesa
    
    def eliminarMesa(self, id: int) -> None:
        MesaController.mesas.pop(id)

    def ocuparMesa(self, grupo: p.GrupoClientes, response:function(bool, (m.Mesa|None))) -> None:
        # Busca dentro de la lista de todas las mesas una que este desocupada y que tenga la capacidad para el grupo que pide
        encontroMesa = False
        mesa = None
        for id in len(MesaController.mesas):
            if(MesaController.mesas[id].getEstado() == m.EstadoMesa.DESOCUPADO and\
                MesaController.mesas[id].getCapacidad >= grupo.getCantidadClientes()):
                MesaController.mesas[id].ocupar(grupo)
                encontroMesa = True
                mesa = MesaController.mesas[id]
                break

        response(encontroMesa, mesa)
        




