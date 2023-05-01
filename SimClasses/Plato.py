# Es un objeto creado en base a la receta que cumple la funcion de ser servido en un pedido
#
# Esto es distinto a la clase Receta ya que la receta marca las indicaciones para el cocinero para crear uno de estos platos, pero capaz
# queremos implementar un sistema para simular platos mal armados o de diferentes niveles de calidad basado en la calidad de los chefs

class Plato():
    def __init__(self) -> None:
        self.nombre = str(input('Ingrese el nombre del plato nuevo: '))
        self.precio = int(input('Ingrese el precio del plato nuevo: '))
        self.tiempo_preparacion = int(input('Ingrese el tiempo promedio de preparacion del plato nuevo: ')) # Este dato nos va a servir de lambda para la distribucion de poisson al momento de simular la preparacion de un plato
        
        self.ingredientes =[]
        self.cant_ingredientes = []
         
        cantidad_de_ingredientes = int(input('Ingrese la cantidad de ingredientes que se necesitan para el plato nuevo: '))
        for i in range(1, cantidad_de_ingredientes + 1):
            self.ingredientes.append(str(input('Ingrese el ingediente ' + str(i) + ' del plato nuevo: ')))
            self.cant_ingredientes.append(int(input('Ingrese la cantidad del ingrediente ' + str(i) + ': ')))

    def __str__(self):
        return

