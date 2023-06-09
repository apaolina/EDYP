from .MesaManager import MesaManager
from .GrupoClientesManager import GrupoClientesManager
from .EmpleadoManager import EmpleadoManager
from .CocinaManager import CocinaManager
from events import Events

# Un tick seria un chequeo de que el tiempo paso
class Tick(Events):
    __events__ = ("on_tick")

    def __init__(self, tiempoPorTick: int) -> None:
        super().__init__()
        self.tiempoPorTick = tiempoPorTick # Esto es la cantidad de tiempo que se simulara entre ticks expresados en segundos
        pass

# Clase que contiene todas las instancias de los Managers en simultaneo
class Restaurante():
    def __init__(self) -> None: 
        self.mesaManager = MesaManager()
        self.grupoManager = GrupoClientesManager()
        self.empleadoManager = EmpleadoManager()
        self.cocinaManager = CocinaManager()
        self.tick: Tick
        pass
    
    # Funcion para definir variables entrarian aca

    def __subscribirAcciones(self) -> None: # Esta funcion va a hacer que todas las acciones escuchen al paso del tiempo del tick
        self.tick.on_tick += self.cocinaManager.crearPedido
        self.tick.on_tick += self.empleadoManager.realizarAccionCocineros
        self.tick.on_tick += self.empleadoManager.realizarAccionMeseros
        self.tick.on_tick += self.grupoManager.realizarAccionGrupoClientes
        self.tick.on_tick += self.grupoManager.fabricaClientes.fabricarClientes
        pass

    def simular(self, tiempoSimulacion: int, tiempoPorTick: int) -> None: # Esto despues va a escupir los resultados de la simulacion, tiempoSim debe ser en segundos
        self.tick = Tick(tiempoPorTick)
        self.__subscribirAcciones()
        while tiempoSimulacion > 0:
            self.tick.on_tick(self.tick.tiempoPorTick)
            # Aca hay que poner un metodo de recoleccion de informacion
            tiempoSimulacion -= tiempoPorTick

instance = Restaurante()