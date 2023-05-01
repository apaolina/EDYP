from SimClasses import instance
import time
from Hasheo import *

#Va a haber que agregar muchos verificadores acá. Especialmente cuando interactuamos con el users.txt
#Tambien verificar que las respuestas sean numericas o strings, dependiendo de lo que se pida.
#DUDA para cada simulación es necesario crear mozos y cocineros nuevos o ya hay guardados, hay que eliminar a los viejos?
#Se me ocurre que habría que ponerle un nombre a cada simulación y guardar los resultados como los parametros de la simulación, los empleados que se crearon, etc. en un archivo de texto

class Simulador:
    def __init__(self):
        self.nombre = ""
        self.cantidad_cocineros = 0
        self.cantidad_mozos = 0
        self.cantidad_mesas = 0
        self.clientes = 0
        self.clientes_generados = 0
        self.tiempo = 0

    def tres(self):
            print('|Programa cerrado')
            print('----------------------------------------')
            exit()

    def registrar_usuario(self, usuario):
        print("|Ingrese su contraseña: ")
        contraseña = input(">>  ")
        print("|Repita su contraseña: ")
        contraseña2 = input(">>  ")
        if contraseña != contraseña2:
            print("|Las contraseñas no coinciden, intente nuevamente")
            self.registrar_usuario(usuario)
        else:
            with open("users.txt", "a") as file:    
                contraseña_hashear = hashear_contraseña(contraseña)
                file.write(f"{usuario},{contraseña_hashear}\n")
                file.close()
                print("|Usuario creado con exito")
                self.consola()

    def dos(self):
        print("|Creando nuevo usuario...")
        print("|Ingrese su nombre de usuario:")
        usuario = str(input('|>>  ').strip())
        with open("users.txt", "r") as file:
            usuarios_almacenados = []
            for line in file.readlines():
                usuario_almacenado, contraseña_almacenada = line.strip().split(",")
                usuarios_almacenados.append(usuario_almacenado)
            for i in range(len(usuarios_almacenados)):
                if usuarios_almacenados[i] == usuario:
                    print("|El usuario ya existe, pruebe otro")
                    file.close()
                    self.consola()
            file.close()
            self.registrar_usuario(usuario)

    def resultado_simulacion(self, start, end):
        print("----------------------------------------")
        print("|Resultados de la simulación:")
        print(f"grupos: {instance.grupoManager.getCantidadGrupoClientes()}")
        print(f"en cola: {instance.grupoManager.colaSentar.totalnodos}")
        print(instance.mesaManager.verEstadoMesas())
        print(instance.cocinaManager.inventario)
        print(end-start)
        exit()

    def empezar_simulacion(self):
        print("|¿Cuánto es el tiempo a simular")
        tiempoSimulacion = int(input('|>>  '))
        self.tiempo = tiempoSimulacion
        start = time.time()
        instance.simular(tiempoSimulacion, tiempoPorTick = 1)
        end = time.time()
        self.resultado_simulacion(start, end)

    def crear_empleados(self):
        print("|Cuántos cocineros desea agregar a la simulación?")
        numero_cocineros = int(input('|>>  '))
        self.cantidad_cocineros = numero_cocineros
        for i in range(1, numero_cocineros + 1):
            print("|Ingrese el nombre del cocinero " + str(i) + ":")
            nombre_cocinero = input('|>>  ')
            instance.empleadoManager.crearCocinero(nombre_cocinero)
        print("|Ha creado " + str(numero_cocineros) + " cocineros con exito")
        print("|Nombres de los cocineros creados:")
        for i in range(1, numero_cocineros +1):
            #print(instance.empleadoManager.empleados[i].nombre) FALTA ESTOOO
            print("|No se como hacer que se muestren los nombres de los cocineros creados")
            
        print("|Cuántos mozos desea agregar a la simulación?")
        numero_mozos = int(input('|>>  '))
        self.cantidad_mozos = numero_mozos
        for i in range(1, numero_mozos + 1):
            print("|Ingrese el nombre del mozo " + str(i) + ":")
            nombre_mozo = input('|>>  ')
            instance.empleadoManager.crearMesero(nombre_mozo)
        print("|Ha creado" + str(numero_mozos) + " con exito")
        print("|Nombres de los mozos creados:")
        for i in range(1, numero_mozos + 1):
            print("|No se como hacer que se muestren los nombres de los mozos creados")
        self.empezar_simulacion()

    def crear_mesas(self, usuario_ingresado):
        print("|Bienvenido al simulador 'Restaurant City' " + usuario_ingresado)
        print("|¿Cuántas mesas desea agregar a la simulación?")
        mesas = int(input('|>>  '))
        self.cantidad_mesas = mesas
        print("|¿Desea que todas las mesas tengan la misma capacidad?")
        print("|1 - Si")
        print("|2 - No")
        respuesta = input('|>>  ')
        if respuesta == "1":
            print("|Ingrese la capacidad de las mesas:")
            capacidad_mesas = int(input('|>>  '))
            for i in range(1, mesas+1):
                instance.mesaManager.crearMesa(capacidad_mesas)
            print("|Ha creado " + str(mesas) + " mesas de " + str(capacidad_mesas) + " personas cada una")
            self.crear_empleados()
        if respuesta == "2":
            for i in range(1, mesas+1):
                print("|Ingrese la capacidad de la mesa " + str(i) + ":")
                capacidad_mesas = int(input('|>>  '))
                instance.mesaManager.crearMesa(capacidad_mesas)
            print("|Ha creado " + str(mesas) + " mesas de diferentes capacidades")
            self.crear_empleados()
            
    def nombre_simulacion(self, usuario_ingresado):
        print("|Ingrese el nombre de la simulación:")
        nombre_simulacion = input('|>>  ')
        self.nombre = nombre_simulacion
        print("|------------------------")
        print("| " + nombre_simulacion)
        print("|------------------------")
        self.crear_mesas(usuario_ingresado)

    def uno(self):
        print("|Ingrese su nombre de usuario: ")
        usuario_ingresado = str(input('|>>  ').strip())
        with open('users.txt', 'r') as file:
            existe = False
            usuarios_almacenados = []
            for line in file.readlines():
                usuario_almacenado, contraseña_almacenada = line.strip().split(",")
                usuarios_almacenados.append(usuario_almacenado)
            for i in range(len(usuarios_almacenados)):
                    if usuarios_almacenados[i] == usuario_ingresado:
                        existe = True
            if existe == False:
                print("|El usuario no existe, pruebe otro")
                file.close()
                self.consola()
            file.close()
        print("|Ingrese su contraseña: ")
        contraseña_ingresada = input("|>>  ")
        verificador = verificar_contraseña(contraseña_ingresada, usuario_ingresado)
        if verificador == True:
            print("|Bienvenido " + usuario_ingresado)
            print('----------------------------------------')
            self.nombre_simulacion(usuario_ingresado)
        if verificador == False:
            print("|Contraseña incorrecta")
            self.consola()
            
    def registrar_resultados(self):
        with open('resultadosSim.txt', 'a') as file:
            file.write(self.nombre + "," + str(instance.grupoManager.getCantidadGrupoClientes()) + "," + str(instance.grupoManager.colaSentar.totalnodos) + "," + str(instance.mesaManager.verEstadoMesas()) + "," + str(instance.cocinaManager.inventario) + "\n")
            file.close()

    def consola(self):
        print('----------------------------------------')
        print("|Bienvenido al simulador 'Restaurant City'")
        print("|1 - Iniciar sesion")
        print("|2 - Registrar nuevo usuario")
        print("|3 - Salir")
        print("|Ingrese el numero de la opcion que desea realizar:")
        opcion = input('|>>  ')
        if opcion == "1" or opcion == "2" or opcion == "3":
            pass
        else:
            print("|Ingrese una opcion valida")
            self.consola()
        if opcion == "3":
            self.tres()

        if opcion == "2":
            self.dos()
        if opcion == "1":
            self.uno()
            
    
restaurante = Simulador()
restaurante.consola()

