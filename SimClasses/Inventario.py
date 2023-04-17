#Se crea la clase Inventario
class Inventario:
    def __init__(self):
        self.nombre = ''
        self.cantidad = 0
        self.precio = 0
        self.categoria = ''
        self.fecha_vencimiento = ''
        self.fecha_ingreso = ''
    def __str__(self):
        return "Nombre: " + self.nombre + " Cantidad: " + str(self.cantidad) + " Precio: " + str(self.precio) + " Categoria: " + self.categoria + " Fecha de vencimiento: " + self.fecha_vencimiento + " Fecha de ingreso: " + self.fecha_ingreso
    def agregar_producto(self):
        self.nombre = str(input("Ingrese el nombre del producto: "))
        self.cantidad = int(input("Ingrese la cantidad del producto: "))
        self.precio = int(input("Ingrese el precio del producto: "))
        self.categoria = str(input("Ingrese la categoria del producto: "))
        self.fecha_vencimiento = str(input("Ingrese la fecha de vencimiento del producto: "))
        self.fecha_ingreso = str(input("Ingrese la fecha de ingreso del producto: "))
    def modificar_producto(self):
        self.nombre = str(input("Ingrese el nombre del producto: "))
        self.cantidad = int(input("Ingrese la cantidad del producto: "))
        self.precio = int(input("Ingrese el precio del producto: "))
        self.categoria = str(input("Ingrese la categoria del producto: "))
        self.fecha_vencimiento = str(input("Ingrese la fecha de vencimiento del producto: "))
        self.fecha_ingreso = str(input("Ingrese la fecha de ingreso del producto: "))
    def eliminar_producto(self):
        self.nombre = ''
        self.cantidad = 0
        self.precio = 0
        self.categoria = ''
        self.fecha_vencimiento = ''
        self.fecha_ingreso = ''
    def consumir_producto(self):
        self.cantidad = self.cantidad - 1
    def restockear_producto(self):
        self.cantidad = self.cantidad + 1
    