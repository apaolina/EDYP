from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import ColaSentar

class GrupoClientesInterface():
    colaSentar = ColaSentar()
    def __init__(self) -> None:
        pass

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesInterface.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()