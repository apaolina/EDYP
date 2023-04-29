from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import Cola, ColaSentar
from .FabricaClientes import FabricaClientes

class GrupoClientesManager():
    colaSentar = ColaSentar()
    colaPedido = Cola()
    def __init__(self, mediaLlegadaGrupos: int, stdDevLlegadaGrupos: int) -> None:
        self.fabricaClientes = FabricaClientes(mediaLlegadaGrupos, stdDevLlegadaGrupos) # Este objeto producira la entrada de nuevos clientes
        pass

    def getCantidadGrupoClientes(self) -> int:
        return GrupoClientes.totalGrupos

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesManager.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()

    def elegirComidaGrupoClientes(self, tiempoPorTick: int) -> None:
        for grupo in self.colaPedido.items:
            grupo.elegirComida(tiempoPorTick)
