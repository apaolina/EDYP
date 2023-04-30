from .Cola import Cola
# Clase que se encarga de todo lo relacionado a la cocina
class CocinaManager():


    def __init__(self) -> None:

        self.colaPlatosProducir = Cola()
        self.colaPedidosPreparar = Cola()
        self.colaPedidosEntregar = Cola()
        self.pedidoEnPreparacion = [(),[]]
        self.inventario = {
        "Hamburguesa": 0, 
        "Pancho": 0
        } # Cambiar para el 2ndo parcial, hacerlo en base al menu y lo que agrega el usuario

    def agregarPedido(self, pedido) -> None:
        
        self.colaPedidosPreparar.encolar(pedido)

        for plato in pedido[0]:
            self.colaPlatosProducir.encolar(plato)

    def requestCocinar(self, resultado) -> None:

        if(self.colaPlatosProducir.totalnodos == 0):
            resultado(None)
            return None
        
        resultado(self.colaPlatosProducir.desencolar())

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
    