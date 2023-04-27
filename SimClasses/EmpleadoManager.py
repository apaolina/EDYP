from .Persona import MeseroEstado, Mesero, Cocinero

class EmpleadoManager():

    meseros: dict[int,Mesero] = {}
    cocineros: dict[int,Cocinero] = {}

    def __init__(self) -> None:
        pass

    def crearMesero(self, nombre:str) -> Mesero:
        nuevoMesero = Mesero(nombre)
        EmpleadoManager.meseros.update({nuevoMesero.getId():nuevoMesero})
        return nuevoMesero
    
    def crearCocinero(self, nombre:str) -> Cocinero:
        nuevoCocinero = Cocinero(nombre)
        EmpleadoManager.cocineros.update({nuevoCocinero.getId():nuevoCocinero})
        return nuevoCocinero
    
    def eliminarMesero(self, id: int) -> None:
        EmpleadoManager.meseros.pop(id)

    def eliminarCocinero(self, id: int) -> None:
        EmpleadoManager.cocineros.pop(id)
    