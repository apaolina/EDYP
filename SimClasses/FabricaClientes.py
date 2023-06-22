import sys
sys.path.insert(0, 'SimClasses')
from Persona import Cliente, GrupoClientes
from Tiempo import tiempo_aleatorio
import random as r
import names

# Esta .py se encargara de la produccion de grupos de clientes, simulando entrada de los mismos
class FabricaClientes():
    
    def __init__(self) -> None:
        self.tiempoParaProxCliente: int = 0
        self.n_clientes: int = 0
        pass

    def __tiempoEntreClientes(self) -> None: # Esto devolvera la cantidad de tiempo para que llegue un nuevo grupo de clientes
        self.tiempoParaProxCliente = tiempo_aleatorio(60) # Definir el valor de lambda que queremos para los clientes (Lo fije 60 en un principio)
    
    def __descontarTiempo(self, tiempoPorTick:int) -> None: # Esta funcion ajusta la cantidad de tiempo entre c/tick
        self.tiempoParaProxCliente -= tiempoPorTick
        pass

    def fabricarClientes(self, tiempoPorTick:int) -> None: # Esta seria la funcion que se callea por tick

        if(self.tiempoParaProxCliente > 1):
            self.__descontarTiempo(tiempoPorTick)
            return None
        
        cantidadClientes = r.randint(1,4) # Entre 1 a X, donde X es la cantidad maxima de grupos de clientes que acepta el restaurante

        self.n_clientes = self.n_clientes + cantidadClientes
        
        resultado = GrupoClientes()

        for cliente in range(cantidadClientes):
            nuevoCliente = Cliente(names.get_full_name())
            resultado.addCliente(nuevoCliente)

        resultado.requestMesa()
        self.__tiempoEntreClientes() # Estas lineas de codigo producen un nuevo grupo, lo encolan y generan un nuevo tiempo entre clientes

    def __str__(self) -> str:
        return f"Tiempo entre clientes: {self.tiempoParaProxCliente}, Cantidad de clientes: {self.n_clientes}"

