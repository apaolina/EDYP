from .Persona import EstadoMesero, Mesero, Cocinero

class EmpleadoManager():

    meseros: dict[Mesero, int] = {}
    cocineros: dict[Cocinero, int] = {}

    def __init__(self) -> None:
        pass

    def crearMesero(self, nombre:str) -> Mesero:
        nuevoMesero = Mesero(nombre)
        EmpleadoManager.meseros.update({nuevoMesero:nuevoMesero.getId()})
        return nuevoMesero
    
    def crearCocinero(self, nombre:str) -> Cocinero:
        nuevoCocinero = Cocinero(nombre)
        EmpleadoManager.cocineros.update({nuevoCocinero:nuevoCocinero.getId()})
        return nuevoCocinero
    
    def eliminarMesero(self, id: int) -> None:
        EmpleadoManager.meseros.pop(id)

    def eliminarCocinero(self, id: int) -> None:
        EmpleadoManager.cocineros.pop(id)

    def realizarAccionMeseros(self, tiempoPorTick: int) -> None:
        for mesero in self.meseros:
            mesero.realizarAccion(tiempoPorTick)
