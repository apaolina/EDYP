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
        self.velocidad = 2 # Sujeto a cambio, requiere varianza, en metros/segundo

    def __str__(self) -> str:
        return super().__str__()

#Clase para agrupar a los clientes, se encarga de sentarse en una mesa desocupada, realizar pedidos y pagar
class GrupoClientes():
    totalGrupos = 0
    def __init__(self, *clientes: Cliente) -> None:
        self.id = GrupoClientes.totalGrupos + 1
        self.clientes:list[Cliente] = []
        for cliente in clientes:
            self.clientes.append(cliente)
        GrupoClientes.totalGrupos += 1

    def __str__(self) -> str:
        string = ""
        
        for cliente in self.clientes:
            string += f"{cliente.nombre}, "

        return string[0:len(str) - 2]

    def addCliente(self, cliente:Cliente) -> None:
        self.clientes.append(cliente)
    
    def getClientes(self) -> list[Cliente]:
        return self.clientes
    
    def getCantidadClientes(self) -> int:
        return len(self.clientes)
    
    def requestMesa():
        pass
        
#Clase generica de los empleados, hereda de Persona
class Empleado(Persona):
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)

#Clase de Meseros, hereda de Empleado, se encarga de tomar pedidos y servir platos
class Mesero(Empleado):
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)

#Clase de Cocineros, hereda de Empleado, se encarga de crear platos segun los pedidos siguiendo los pasos de las recetas
class Cocinero(Empleado):
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)