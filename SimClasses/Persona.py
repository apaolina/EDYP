import sys
sys.path.insert(0, 'SimClasses')
from enum import Enum
import random as r
from Tiempo import tiempo_aleatorio_normal

#Clase generica de las personas
class Persona():

    def __init__(self, nombre:str) -> None:
        self.nombre = nombre
        pass

    def __str__(self) -> str:
        return self.nombre

#Clase de Clientes, hereda de Persona
class Cliente(Persona):

    totalClientes = 0

    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.id = Cliente.totalClientes + 1
        Cliente.totalClientes += 1
        self.enGrupo = False

    def __str__(self) -> str:
        return super().__str__()
    
    def agrupar(self) -> None:
        self.enGrupo = True


class EstadoGC(Enum):
    ESPERANDO_MESA = 1
    ELIGIENDO_COMIDA = 2
    ESPERANDO_PEDIR = 3
    ESPERANDO_COMIDA = 4
    COMIENDO = 5

#Clase para agrupar a los clientes, se encarga de sentarse en una mesa desocupada, realizar pedidos y pagar
class GrupoClientes():

    totalGrupos = 0

    def __init__(self, *clientes: Cliente) -> None:
        self.id = GrupoClientes.totalGrupos + 1
        self.clientes:list[Cliente] = []
        self.mesa: int
        self.desocupando = False

        for cliente in clientes:

            if(cliente.enGrupo):
                raise Exception(f"Cliente {cliente.nombre} ya se encuentra en un grupo")
            
            self.clientes.append(cliente)
            cliente.agrupar()

        GrupoClientes.totalGrupos += 1
        self.estado = EstadoGC.ESPERANDO_MESA
        self.contadorParaAccion: int
        self.listaPedido: list(str) = []

    def __str__(self) -> str:
        string = ""
        
        for cliente in self.clientes:
            string += f"{cliente.nombre}, "

        return string[:-2]
    
    def __len__(self) -> int:
        return len(self.clientes)

    def addCliente(self, cliente:Cliente) -> None:
        self.clientes.append(cliente)
    
    def getClientes(self) -> list[Cliente]:
        return self.clientes
    
    def getCantidadClientes(self) -> int:
        return len(self.clientes)
    
    def getEstado(self) -> EstadoGC:
        return self.estado

    def realizarAccion(self, tiempoPorTick: int) -> None:
        
        match self.estado:

            case EstadoGC.ELIGIENDO_COMIDA:
                if(self.contadorParaAccion > 1):
                    self.contadorParaAccion -= tiempoPorTick
                    return None

                for cliente in self.clientes:
                    from RestauranteManager import instance
                    plato = instance.cocinaManager.menu.Platos_menu[r.randint(0,len(instance.cocinaManager.menu.Platos_menu) - 1)]
                    self.listaPedido.append(plato)

                self.estado = EstadoGC.ESPERANDO_PEDIR

                from RestauranteManager import instance
                instance.grupoManager.colaPedido.encolar(self)

            case EstadoGC.COMIENDO:

                if(self.contadorParaAccion > 1):
                    self.contadorParaAccion -= tiempoPorTick
                    return None
                
                from RestauranteManager import instance
                self.desocupando = True
                instance.mesaManager.desocuparMesa(self.mesa)

    def __responseMesa(self, resultado: bool, id: int) -> None:
        from RestauranteManager import instance

        if(resultado):
            if(instance.grupoManager.colaSentar.dentro(self)):
                instance.grupoManager.colaSentar.desencolar(self)
                instance.infoManager.declararEvento("Se sento un grupo de clientes")

            self.contadorParaAccion = tiempo_aleatorio_normal(40,7) # Esto esta fuera del scope, implementar en el futuro
            self.estado = EstadoGC.ELIGIENDO_COMIDA
            self.mesa = id

            instance.grupoManager.gruposSentados.update({self.id:self})

        elif(not instance.grupoManager.colaSentar.dentro(self)):
            instance.grupoManager.colaSentar.encolar(self)
    
    def requestMesa(self) -> None:
        from RestauranteManager import instance

        if(self.estado != EstadoGC.ESPERANDO_MESA):
            raise Exception(f"El grupo {self.id} ya esta sentado")
        
        instance.mesaManager.requestMesa(self.getCantidadClientes(), self.__responseMesa)

    def tomarPedido(self) -> None:
        if(self.estado != EstadoGC.ESPERANDO_PEDIR):
            raise Exception(f"El grupo {self.id} no esta esperando pedir")
        
        self.estado = EstadoGC.ESPERANDO_COMIDA

    def entregarPedido(self) -> None:
        if(self.estado != EstadoGC.ESPERANDO_COMIDA):
            raise Exception(f"El grupo {self.id} no esta esperando comida")
        
        self.estado = EstadoGC.COMIENDO
        self.contadorParaAccion = tiempo_aleatorio_normal(10,5) # Otra instancia donde necesitamos aleatorizar el tiempo

#Clase generica de los empleados, hereda de Persona
class Empleado(Persona):

    totalEmpleados = 0

    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.id = self.totalEmpleados
        self.totalEmpleados += 1

    def getId(self) -> int:
        return self.id

class EstadoMesero(Enum):
    ESPERANDO_ACCION = 1
    TOMANDO_PEDIDO = 2
    LLEVANDO_PLATOS = 3
    LAVANDO_MESA = 4

#Clase de Meseros, hereda de Empleado, se encarga de tomar pedidos y servir platos
class Mesero(Empleado):

    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.estado: EstadoMesero = EstadoMesero.ESPERANDO_ACCION
        self.pedidoEnMano: tuple[list[str],int]
        self.contadorParaAccion: int

    def __responsePedido(self, resultado: (None|list), id: (None|int)) -> None:
        if(resultado is None or id is None):
            return None
        
        self.estado = EstadoMesero.TOMANDO_PEDIDO
        self.pedidoEnMano = (resultado,id)
        self.contadorParaAccion = tiempo_aleatorio_normal(5,3)  # Otra instancia donde necesitamos aleatorizar el tiempo

    def __responsePlatos(self, resultado: (None|list), id: (None|int)) -> None:
        if(resultado is None or id is None):
            return None
        
        self.estado = EstadoMesero.LLEVANDO_PLATOS
        self.pedidoEnMano = (resultado,id)
        self.contadorParaAccion = tiempo_aleatorio_normal(5,3) # Otra instancia donde necesitamos aleatorizar el tiempo
    
    def __requestPlatos(self) -> None:
        from RestauranteManager import instance
        if(self.estado != EstadoMesero.ESPERANDO_ACCION):
            raise Exception(f"Mesero {self.id} ya esta ocupado")
        
        instance.cocinaManager.requestPlatos(self.__responsePlatos)

    def __requestPedido(self) -> None:
        from RestauranteManager import instance
        if(self.estado != EstadoMesero.ESPERANDO_ACCION):
            raise Exception(f"Mesero {self.id} ya esta ocupado")
        
        instance.grupoManager.requestPedido(self.__responsePedido)

    def realizarAccion(self,tiempoPorTick: int) -> None:
        
        match self.estado:

            case EstadoMesero.ESPERANDO_ACCION: 
                self.__requestPedido()
                if(self.estado == EstadoMesero.ESPERANDO_ACCION):
                    self.__requestPlatos()
                pass

            case EstadoMesero.TOMANDO_PEDIDO:
                if(self.contadorParaAccion > 1):
                    self.contadorParaAccion -= tiempoPorTick

                from RestauranteManager import instance
                instance.cocinaManager.agregarPedido(self.pedidoEnMano)
                instance.infoManager.declararEvento("Se tomo un pedido")

                self.estado = EstadoMesero.ESPERANDO_ACCION
                self.pedidoEnMano = None
                pass

            case EstadoMesero.LLEVANDO_PLATOS:
                if(self.contadorParaAccion > 1):
                    self.contadorParaAccion -= tiempoPorTick


                from RestauranteManager import instance
                instance.grupoManager.gruposSentados[self.pedidoEnMano[1]].entregarPedido()
                instance.infoManager.declararEvento("Se entrego un pedido")
                
                self.estado = EstadoMesero.ESPERANDO_ACCION
                self.pedidoEnMano = None
                pass

            case other:
                pass

    def __str__(self) -> str:
        return f"Mesero {self.id}"
    
    
class EstadoCocinero(Enum):
    ESPERANDO_ACCION = 1
    COCINANDO = 2
    
#Clase de Cocineros, hereda de Empleado, se encarga de crear platos segun los pedidos siguiendo los pasos de las recetas
class Cocinero(Empleado):

    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.estado = EstadoCocinero.ESPERANDO_ACCION
        self.platoEnCoccion = ""
        self.contadorParaAccion = 0

    def responseCocinar(self, plato: (None|str), tiempoCoccion: (None|int)) -> None:
        
        if(plato is None):
            return None
        
        self.platoEnCoccion = plato
        self.estado = EstadoCocinero.COCINANDO
        self.contadorParaAccion = tiempo_aleatorio_normal(tiempoCoccion,2)
        
        
    def __requestCocinar(self) -> None:
        
        if(self.estado != EstadoCocinero.ESPERANDO_ACCION):
            raise Exception(f"Cocinero {self.id} ya esta cocinando")
        
        from RestauranteManager import instance
        instance.cocinaManager.requestCocinar(self.responseCocinar)
        
    def realizarAccion(self, tiempoPorTick: int) -> None:

        match self.estado:

            case EstadoCocinero.ESPERANDO_ACCION:
                self.__requestCocinar()
                pass
            
            case EstadoCocinero.COCINANDO:
                if(self.contadorParaAccion > 1):
                    self.contadorParaAccion -= tiempoPorTick

                from RestauranteManager import instance
                instance.cocinaManager.agregarInventario(self.platoEnCoccion)
                instance.infoManager.declararEvento("Se cocino un " + self.platoEnCoccion)
                
                
                self.platoEnCoccion = ""
                self.estado = EstadoCocinero.ESPERANDO_ACCION
                pass
            
            case other:
                pass
    
    def __str__(self) -> str:
        return f"Cocinero {self.id}"
    