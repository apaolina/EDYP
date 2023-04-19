from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import ColaSentar

class GrupoClientesController():
    colaSentar = ColaSentar()
    def __init__(self) -> None:
        pass

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesController.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()