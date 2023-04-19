from .Mesa import MesaController

# Clase que contiene todas las instancias de los controllers en simultaneo
class Instance():
    def __init__(self) -> None:
        self.mesaController = MesaController()
        pass

    def requestMesa(self, cantidad: int, respuesta) -> None:
        self.mesaController.requestMesa(cantidad, respuesta)

instance = Instance()