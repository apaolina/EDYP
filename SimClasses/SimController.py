from .MesaInterface import MesaInterface
from .GrupoClientesInterface import GrupoClientesInterface

# Clase que contiene todas las instancias de los Interfaces en simultaneo
class Instance():
    def __init__(self) -> None:
        self.mesaInterface = MesaInterface()
        self.grupoInterface = GrupoClientesInterface()
        pass

instance = Instance()