import sys
sys.path.insert(0, 'SimClasses')
from Cola import Cola
from Menu import Menu
# Clase que se encarga de todo lo relacionado a la cocina
class CocinaManager():


    def __init__(self) -> None:

        self.colaPlatosProducir = Cola()
        self.colaPedidosPreparar = Cola()
        self.colaPedidosEntregar = Cola()
        self.pedidoEnPreparacion = [(),[]]
        self.menu = Menu()
        self.inventario = {

        } 

    def agregarPlato(self, nombre_plato: str, tiempo_promedio_coccion: int):
        self.menu.agregar_plato(nombre_plato, tiempo_promedio_coccion)
        self.inventario[nombre_plato] = 0


    def agregarPedido(self, pedido) -> None:
    
        self.colaPedidosPreparar.encolar(pedido)

        for plato in pedido[0]:
            self.colaPlatosProducir.encolar(plato)

    def requestCocinar(self, resultado) -> None:

        if(self.colaPlatosProducir.totalnodos == 0):
            resultado(None, None)
            return None
        
        plato = self.colaPlatosProducir.desencolar()

        resultado(plato, self.menu.dict_platos[plato])

    def requestPlatos(self, response) -> None:

        if(len(self.colaPedidosEntregar) == 0):
            response(None,None)
            return None
        
        resultado = self.colaPedidosEntregar.desencolar()

        response(resultado[0],resultado[1])


    def agregarInventario(self, plato :str) -> None:

        if(plato in self.inventario):
            d = {plato: self.inventario[plato] + 1}
            self.inventario.update(d)
            
    def crearPedido(self, tiempoPorTick:int) -> None:

        if(self.colaPedidosPreparar.totalnodos == 0 and self.pedidoEnPreparacion == [(),[]]):
            return None
        
        # Fijar proximo pedido a armarse
        if(self.pedidoEnPreparacion == [(),[]]):
            self.pedidoEnPreparacion[0] = self.colaPedidosPreparar.desencolar()
            for plato in self.pedidoEnPreparacion[0][0]:
                self.pedidoEnPreparacion[1].append(False)

        for platoId in range(len(self.pedidoEnPreparacion[0][0])):
            # Basicamente chequea si hay del plato en el inventario, si hay sacarlo del inventario y agregarlo al pedido
            if(self.inventario[self.pedidoEnPreparacion[0][0][platoId]] > 0 and self.pedidoEnPreparacion[1][platoId] == False):
                d = {self.pedidoEnPreparacion[0][0][platoId]:self.inventario[self.pedidoEnPreparacion[0][0][platoId]] - 1}
                self.inventario.update(d)
                self.pedidoEnPreparacion[1][platoId] = True

        # Checkea que todos los platos esten disponibles
        if(all(self.pedidoEnPreparacion[1])):
            self.colaPedidosEntregar.encolar(self.pedidoEnPreparacion[0])
            self.pedidoEnPreparacion = [(),[]]
            from RestauranteManager import instance
            instance.infoManager.declararEvento("Se preparo un pedido")
            
    