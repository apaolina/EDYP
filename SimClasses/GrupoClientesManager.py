from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import ColaSentar
from .FabricaClientes import FabricaClientes

class GrupoClientesManager():
    colaSentar = ColaSentar()
    def __init__(self, mediaLlegadaGrupos: int, stdDevLlegadaGrupos: int) -> None:
        self.fabricaClientes = FabricaClientes(mediaLlegadaGrupos, stdDevLlegadaGrupos) # Este objeto producira la entrada de nuevos clientes
        pass

    def getCantidadGrupoClientes(self) -> int:
        return GrupoClientes.totalGrupos

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesManager.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()