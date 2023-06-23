import sys
sys.path.insert(0, "Database")
from DataBaseManager import DataManager

class InfoManager():
    def __init__(self) -> None:
        # Estructura -> Nombre evento, tick ocurrido
        self.eventos: list[(str, int)] = []
        self.dataManager = DataManager()
        
    def declararEvento(self, evento:str) -> None:
        from RestauranteManager import instance
        self.eventos.append((evento, instance.tiempoSimulacion))

    def subirEventos(self, id:int) -> None:
        self.dataManager.subirEventos(id, self.eventos)
        pass

    def __str__(self) -> str:
        return len(self.eventos)