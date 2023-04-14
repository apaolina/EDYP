#Se crea la clase Cliente
class Clientes():
    def __init__(self, Numero_cliente, Comensales):
        self.Numero_cliente = Numero_cliente
        self.Comensales = Comensales
        self.Estado_Cliente = 'En espera de mesa'
    def Asignar_mesa_cliente(self):
        self.Estado_Cliente = 'Mesa asignada'
    def Desasginar_mesa_cliente(self):
        self.Estado_Cliente = 'Termino'