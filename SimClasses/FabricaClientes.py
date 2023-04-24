from .Persona import Cliente, GrupoClientes
import random as r
from .Cola import ColaSentar
import names

# Esta .py se encargara de la produccion de grupos de clientes, simulando entrada de los mismos
class FabricaClientes():
    def __init__(self, media: int, stdDev: int) -> None:
        self.media = media
        self.stdDev = stdDev
        self.tiempoParaProxCliente: int = 0
        pass

    def __tiempoEntreClientes(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo grupo de clientes
        self.tiempoParaProxCliente = 5 # Aca utilizar media y stdDev para alterar la frecuencia de los clientes
    
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxCliente -= tiempoPorTick
        pass

    def fabricarClientes(self, tiempoPorTick:int) -> None: # Esta seria la funcion que se callea por tick

        if(self.tiempoParaProxCliente > 0):
            self.__descontarTiempo(tiempoPorTick)
            return None
        
        cantidadClientes = r.randint(1,4) # Entre 1 a X, donde X es la cantidad maxima de grupos de clientes que acepta el restaurante

        resultado = GrupoClientes()

        for cliente in range(cantidadClientes):
            nuevoCliente = Cliente(names.get_full_name())
            resultado.addCliente(nuevoCliente)

        resultado.requestMesa()
        self.__tiempoEntreClientes() # Estas lineas de codigo producen un nuevo grupo, lo encolan y generan un nuevo tiempo entre clientes

    
