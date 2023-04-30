from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import Cola, ColaSentar
from .FabricaClientes import FabricaClientes

class GrupoClientesManager():
    colaSentar = ColaSentar()
    gruposEligiendoComida = []
    colaPedido = Cola()
    def __init__(self) -> None:
        self.fabricaClientes = FabricaClientes() # Este objeto producira la entrada de nuevos clientes
        pass
    
    def getCantidadGrupoClientes(self) -> int:
        return GrupoClientes.totalGrupos

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesManager.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()

    def requestPedido(self, response) -> None:
        if(len(self.colaPedido) == 0):
            response(None,None)
            return None
        
        grupo: GrupoClientes = self.colaPedido.desencolar()
        
        response(grupo.listaPedido, grupo.id)
        grupo.listaPedido = []
        

    def elegirComidaGrupoClientes(self, tiempoPorTick: int) -> None:
        for grupo in self.gruposEligiendoComida:
            grupo.elegirComida(tiempoPorTick)
