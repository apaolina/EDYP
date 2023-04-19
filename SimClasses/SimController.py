from .MesaController import MesaController
from .GrupoClientesController import GrupoClientesController

# Clase que contiene todas las instancias de los controllers en simultaneo
class Instance():
    def __init__(self) -> None:
        self.mesaController = MesaController()
        self.grupoController = GrupoClientesController()
        pass

    def requestMesa(self, grupoClientes, respuesta) -> None:
        self.mesaController.requestMesa(grupoClientes.getCantidadClientes(), respuesta)

instance = Instance()