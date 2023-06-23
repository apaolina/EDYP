import sys
sys.path.insert(0, 'SimClasses')
from MesaManager import MesaManager
from GrupoClientesManager import GrupoClientesManager
from EmpleadoManager import EmpleadoManager
from CocinaManager import CocinaManager
from InfoManager import InfoManager
from events import Events
import names
from typing import Callable

# Un tick seria un chequeo de que el tiempo paso
class Tick(Events):
    __events__ = ("on_tick")

    def __init__(self, tiempoPorTick: int) -> None:
        super().__init__()
        self.tiempoPorTick = tiempoPorTick # Esto es la cantidad de tiempo que se simulara entre ticks expresados en segundos
        pass

    def __str__(self) -> str:
        return f"Tiempo por tick: {self.tiempoPorTick}"
    
# Clase que contiene todas las instancias de los Managers en simultaneo
class Restaurante():
    def __init__(self) -> None: 
        self.mesaManager = MesaManager()
        self.grupoManager = GrupoClientesManager()
        self.empleadoManager = EmpleadoManager()
        self.cocinaManager = CocinaManager()
        self.infoManager = InfoManager()
        self.tick: Tick
        pass
    
    def __str__(self) -> str:
        return f"Restaurante: {self.mesaManager}, {self.grupoManager}, {self.empleadoManager}, {self.cocinaManager}, {self.tick}"
    
    # Funcion para definir variables entrarian aca

    def __subscribirAcciones(self) -> None: # Esta funcion va a hacer que todas las acciones escuchen al paso del tiempo del tick
        self.tick.on_tick += self.cocinaManager.crearPedido
        self.tick.on_tick += self.empleadoManager.realizarAccionCocineros
        self.tick.on_tick += self.empleadoManager.realizarAccionMeseros
        self.tick.on_tick += self.grupoManager.realizarAccionGrupoClientes
        self.tick.on_tick += self.grupoManager.fabricaClientes.fabricarClientes
        pass

    def simular(self, cantidad_meseros:str, cantidad_cocineros:str, cantidad_clientes: str,\
                dict_mesas: dict[str,list[str,str]], dict_platos: dict[str,list[str,str]], \
                    tiempoSimulacionInput: str, tiempoPorTick: str, callback: Callable[[None],None], id: int) -> None: 
        
        self.tiempoSimulacion = int(tiempoSimulacionInput)

        for mesero in range(int(cantidad_meseros)):
            self.empleadoManager.crearMesero(names.get_full_name())
        
        for cocinero in range(int(cantidad_cocineros)):
            self.empleadoManager.crearCocinero(names.get_full_name())

        self.grupoManager.setLambdaFabrica(int(cantidad_clientes))

        for mesa in dict_mesas.values():
            self.mesaManager.crearMesa(int(mesa[1]))

        for plato in dict_platos.values():
            self.cocinaManager.agregarPlato(plato[0], int(plato[1]))
        
        self.tick = Tick(int(tiempoPorTick))
        self.__subscribirAcciones()
        while self.tiempoSimulacion > 0:
            self.tick.on_tick(self.tick.tiempoPorTick)
            
            self.tiempoSimulacion -= int(tiempoPorTick)
            
        self.infoManager.subirEventos(id)
        callback()
        
    


instance = Restaurante()