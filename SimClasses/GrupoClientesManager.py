from .Persona import Cliente, GrupoClientes, EstadoGC
from .Cola import Cola, ColaSentar
from .FabricaClientes import FabricaClientes

class GrupoClientesManager():
    colaSentar = ColaSentar()
    gruposSentados: dict[int:GrupoClientes] = {}
    listaDesocupar: int = []
    colaPedido = Cola()

    def __init__(self) -> None:
        self.fabricaClientes = FabricaClientes() # Este objeto producira la entrada de nuevos clientes
        pass
    
    def getCantidadGrupoClientes(self) -> int:
        return GrupoClientes.totalGrupos
    
    def getCantidadNClientes(self) -> int:
        return self.fabricaClientes.n_clientes

    def getCantidadColaSentar(self) -> int:
        return len(GrupoClientesManager.colaSentar)
    
    def requestMesaDenuevo(self) -> int:
        self.colaSentar.nodos[0].item.requestMesa()

    def requestPedido(self, response) -> None:
        if(len(self.colaPedido) == 0):
            response(None,None)
            return None
        
        grupo: GrupoClientes = self.colaPedido.desencolar()
        grupo.tomarPedido()
        response(grupo.listaPedido, grupo.id)
        grupo.listaPedido = []

    def realizarAccionGrupoClientes(self, tiempoPorTick: int) -> None:
        for grupo in self.gruposSentados:
            if(self.gruposSentados[grupo].desocupando is False):
                self.gruposSentados[grupo].realizarAccion(tiempoPorTick)
        

