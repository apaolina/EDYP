#Clase generica de las personas
class Persona():
    def __init__(self, nombre:str) -> None:
        self.nombre = nombre
        pass

#Clase de Clientes, hereda de Persona, se encarga de sentarse en una mesa desocupada, realizar pedidos y pagar
class Cliente(Persona):
    def __init__(self, nombre:str) -> None:
        super().__init__(nombre)

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