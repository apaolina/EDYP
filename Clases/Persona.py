#Clase generica de las personas
class Persona():
    def __init__(self) -> None:
        pass

#Clase de Clientes, hereda de Persona, se encarga de sentarse en una mesa desocupada, realizar pedidos y pagar
class Cliente(Persona):
    def __init__(self) -> None:
        super().__init__()

#Clase generica de los empleados, hereda de Persona
class Empleado(Persona):
    def __init__(self) -> None:
        super().__init__()

#Clase de Meseros, hereda de Empleado, se encarga de tomar pedidos y servir platos
class Mesero(Empleado):
    def __init__(self) -> None:
        super().__init__()

#Clase de Cocineros, hereda de Empleado, se encarga de crear platos segun los pedidos siguiendo los pasos de las recetas
class Cocinero(Empleado):
    def __init__(self) -> None:
        super().__init__()