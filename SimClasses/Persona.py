from enum import Enum
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
        self.velocidad = 2 # Sujeto a cambio, requiere varianza, en metros/segundo

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
        for cliente in clientes:
            if(cliente.enGrupo):
                raise Exception(f"Cliente {cliente.nombre} ya se encuentra en un grupo")
            self.clientes.append(cliente)
            cliente.agrupar()
        GrupoClientes.totalGrupos += 1
        self.estado = EstadoGC.ESPERANDO_MESA

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
    
    def __responseMesa(self, result: bool) -> None:
        from .RestauranteManager import instance
        if(result):
            self.estado = EstadoGC.ELIGIENDO_COMIDA
            if(instance.grupoManager.colaSentar.dentro(self)):
                instance.grupoManager.colaSentar.desencolar(self)
            # Aca implementar funcion que inicia el proceso de seleccion de comida
        elif(not instance.grupoManager.colaSentar.dentro(self)):
            instance.grupoManager.colaSentar.encolar(self)
    
    def requestMesa(self) -> None:
        from .RestauranteManager import instance
        if(self.estado != EstadoGC.ESPERANDO_MESA):
            raise Exception("Grupo ya esta sentado")
        instance.mesaManager.requestMesa(self.getCantidadClientes(), self.__responseMesa)

#Clase generica de los empleados, hereda de Persona
class Empleado(Persona):
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)

class MeseroEstado(Enum):
    ESPERANDO_ACCION = 1
    TOMANDO_PEDIDO = 2
    LLEVANDO_PLATOS = 3
    LAVANDO_MESA = 4

#Clase de Meseros, hereda de Empleado, se encarga de tomar pedidos y servir platos
class Mesero(Empleado):
    totalMeseros = 0
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.estado: MeseroEstado = MeseroEstado.ESPERANDO_ACCION
        self.id = Mesero.totalMeseros
        Mesero.totalMeseros += 1

#Clase de Cocineros, hereda de Empleado, se encarga de crear platos segun los pedidos siguiendo los pasos de las recetas
class Cocinero(Empleado):
    totalCocineros = 0
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)
        self.id = Mesero.totalCocineros
        Cocinero.totalCocineros += 1