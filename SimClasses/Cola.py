from typing import TypeVar, Generic

T = TypeVar('T')

class NodoCola(Generic[T]):
    def __init__(self,item:T, id: int) -> None:
        self.item: T = item
        self.id: int = id

    def __str__(self) -> str:
        return f"item: {self.item}, id: {self.id}"

    def MoverAdelante(self) -> None:
        self.id -= 1

    def MoverAtras(self) -> None:
        self.id += 1


class Cola(Generic[T]):
    def __init__(self) -> None:
        self.nodos: list[NodoCola] = []
        self.totalnodos: int = 0
        pass

    def __len__(self) -> int:
        return self.totalnodos

    def encolar(self, item:T):
        self.nodos.append(NodoCola(item,self.totalnodos))
        self.totalnodos += 1
        pass

    def desencolar(self) -> T:
        nodoDescolado = self.nodos.pop(0)
        for nodo in self.nodos:
            nodo.MoverAdelante()
        self.totalnodos -= 1
        return nodoDescolado.item

    def vaciar(self) -> list[T]:
        return not self.items
    
    def dentro(self, item:T) -> bool:
        for nodo in self.nodos:
            if(item == nodo.item):
                return True
        
        return False
    
class ColaSentar(Cola):

    def __acomodarCola(self, id: int) -> None:
        for nodo in self.nodos[id+1:]:
            nodo.MoverAdelante()


    def desencolar(self, item: T) -> T:
        for nodo in self.nodos:
            if(nodo.item == item):
                resultado = self.nodos.pop(nodo.id)
                self.__acomodarCola(nodo.id)
                self.totalnodos -= 1
                return resultado.item
            
            



    