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
        print('|')
        print('|Programa cerrado')
        print('----------------------------------------')
        exit()

    def registrar_usuario(self, usuario):
        print('|')
        print("|Ingrese su contraseña: ")
        contraseña = input("|>>  ")
        print("|Repita su contraseña: ")
        contraseña2 = input("|>>  ")
        if contraseña != contraseña2:
            print("|Las contraseñas no coinciden, intente nuevamente")
            time.sleep(2)
            self.registrar_usuario(usuario)
        else:  
            try:
                
                with open("users.txt", "a") as file:
                    if file.closed:
                        print('|')
                        print("|El banco de usuarios no puede ser accedido. Intente en otro momento.")
                        exit()
                    contraseña_hashear = hashear_contraseña(contraseña)
                    file.write(f"{usuario},{contraseña_hashear}\n")
                    file.close()
                    time.sleep(2)
                    print('|')
                    print("|Usuario creado con exito")
                    time.sleep(2)
                    self.consola()
                    
            except FileNotFoundError:
                with open("users.txt", "w") as file: 
                    contraseña_hashear = hashear_contraseña(contraseña)
                    file.write(f"{usuario},{contraseña_hashear}\n")
                    file.close()
                    print('|')
                    print("|Usuario creado con exito")
                    self.consola()

    def dos(self):
        print('|')
        print("|Creando nuevo usuario...")
        time.sleep(2)
        print("|Ingrese su nombre de usuario:")
        usuario = str(input('|>>  ').strip())
        if not os.path.exists("users.txt"):
            with open("users.txt", "w") as file:
                file.write("")
                file.close()
        with open("users.txt", "r") as file:
            usuarios_almacenados = []
            for line in file.readlines():
                usuario_almacenado, contraseña_almacenada = line.strip().split(",")
                usuarios_almacenados.append(usuario_almacenado)
            for i in range(len(usuarios_almacenados)):
                if usuarios_almacenados[i] == usuario:
                    print("|El usuario ya existe, pruebe otro")
                    file.close()
                    time.sleep(2)
                    self.consola()
            file.close()
            self.registrar_usuario(usuario)

    def registrar_resultados(self):
        with open('resultadosSim.txt', 'a') as file:
            file.write(self.nombre + "," + str(self.cantidad_cocineros) + "," + str(self.cantidad_mozos) + "," + str(self.cantidad_mesas) + "," + str(self.clientes) + "," + str(self.clientes_generados) + "," + str(self.tiempo) + "\n")
            file.close()
            print('|')
            print("|Resultados guardados con exito")
            time.sleep(2)
            exit()

    def resultado_simulacion(self, start, end):
        print('|')
        print("----------------------------------------")
        print("|Resultados de la simulación:")
        print(f"grupos: {instance.grupoManager.getCantidadGrupoClientes()}")
        print(f"en cola: {instance.grupoManager.colaSentar.totalnodos}")
        print(instance.mesaManager.verEstadoMesas())
        print(instance.cocinaManager.inventario)
        print(end-start)
        self.clientes = instance.grupoManager.getCantidadGrupoClientes()
        self.clientes_generados = instance.grupoManager.getCantidadNClientes()
        self.registrar_resultados()
        exit()

    def empezar_simulacion(self):
        print('|')
        print("|¿Cuánto es el tiempo a simular")
        tiempoSimulacion = input('|>>  ')
        if not tiempoSimulacion.isdigit():
            print('|')
            print("|El tiempo de simulación debe ser un número entero. Por favor, ingrese un número entero.")
            time.sleep(3)
            self.empezar_simulacion()
        tiempoSimulacion = int(tiempoSimulacion)
        self.tiempo = tiempoSimulacion
        start = time.time()
        instance.simular(tiempoSimulacion, tiempoPorTick = 1)
        end = time.time()
        self.resultado_simulacion(start, end)

    def crear_empleados(self):
        print('|')
        print("|Cuántos cocineros desea agregar a la simulación?")
        numero_cocineros = input('|>>  ')
        if not numero_cocineros.isdigit():
            print('|')
            print("|El numero de cocineros debe ser un numero entero. Ingrese nuevamente. ")
            time.sleep(2)
            self.crear_empleados()
        numero_cocineros = int(numero_cocineros)
        self.cantidad_cocineros = numero_cocineros
        nombres_Cocineros = []
        for i in range(1, numero_cocineros + 1):
            print("|Ingrese el nombre del cocinero " + str(i) + ":")
            nombre_cocinero = input('|>>  ')
            nombres_Cocineros.append(nombre_cocinero)
            instance.empleadoManager.crearCocinero(nombre_cocinero)
        print("|Ha creado " + str(numero_cocineros) + " cocineros con exito")
        print("|Nombres de los cocineros creados:")
        for nombre in nombres_Cocineros:
            print('|')
            time.sleep(1)
            print(f"|El cocinero {nombre} ha sido creado correctamente")
        
        print('|')    
        print("|Cuántos mozos desea agregar a la simulación?")
        numero_mozos = input('|>>  ')
        if not numero_mozos.isdigit():
            print('|')
            print("|El numero de mozos debe ser un numero entero. Ingrese  todo nuevamente. ")
            time.sleep(2)
            self.crear_empleados()
        numero_mozos = int(numero_mozos)
        nombres_Mozos = []
        self.cantidad_mozos = numero_mozos
        for i in range(1, numero_mozos + 1):
            print("|Ingrese el nombre del mozo " + str(i) + ":")
            nombre_mozo = input('|>>  ')
            nombres_Mozos.append(nombre_mozo)
            instance.empleadoManager.crearMesero(nombre_mozo)
        print("|Ha creado " + str(numero_mozos) + " mozos con exito")
        print("|Nombres de los mozos creados:")
        for nombre in nombres_Mozos:
            time.sleep(1)
            print('|')
            print(f"|El mozo {nombre} ha sido creado correctamente")
        self.empezar_simulacion()

    def crear_mesas(self, usuario_ingresado):
        print('|')
        print("|Bienvenido al simulador 'Restaurant City' " + usuario_ingresado)
        time.sleep(1)
        print('|')
        print("|¿Cuántas mesas desea agregar a la simulación?")
        mesas = input('|>>  ')
        if not mesas.isdigit():
            print('|')
            print("|El numero de mesas debe ser un numero entero. Ingrese nuevamente. ")
            time.sleep(2)
            self.crear_mesas(usuario_ingresado)
        
        mesas = int(mesas)
        self.cantidad_mesas = mesas
        print('|')
        print("|¿Desea que todas las mesas tengan la misma capacidad?")
        time.sleep(1)
        print("|1 - Si")
        time.sleep(1)
        print("|2 - No")
        respuesta = input('|>>  ')
        if respuesta != "1" and respuesta != "2":
            print('|')
            print("|La respuesta debe ser 1 o 2. Ingrese nuevamente. ")
            time.sleep(2)
            self.crear_mesas(usuario_ingresado)
        if respuesta == "1":
            print("|Ingrese la capacidad de las mesas:")
            capacidad_mesas = input('|>>  ')
            if not capacidad_mesas.isdigit():
                print('|')
                print("|La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
                time.sleep(2)
                self.crear_mesas(usuario_ingresado)
            
            capacidad_mesas = int(capacidad_mesas)
            for i in range(1, mesas+1):
                instance.mesaManager.crearMesa(capacidad_mesas)
            print('|')
            print("|Ha creado " + str(mesas) + " mesas de " + str(capacidad_mesas) + " personas cada una")
            time.sleep(1)
            self.crear_empleados()
        if respuesta == "2":
            for i in range(1, mesas+1):
                print("|Ingrese la capacidad de la mesa " + str(i) + ":")
                capacidad_mesas = input('|>>  ')
                if not capacidad_mesas.isdigit():
                    print('|')
                    print("|La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
                    time.sleep(2)
                    self.crear_mesas(usuario_ingresado)
        
                capacidad_mesas = int(capacidad_mesas)
                instance.mesaManager.crearMesa(capacidad_mesas)
            time.sleep(1)
            print('|')
            print("|Ha creado " + str(mesas) + " mesas de diferentes capacidades")
            self.crear_empleados()
            
    def nombre_simulacion(self, usuario_ingresado):
        print("|Ingrese el nombre de la simulación:")
        nombre_simulacion = input('|>>  ')
        self.nombre = nombre_simulacion
        print('|')
        print('|')
        time.sleep(1)
        print("|---------------------------------")
        print("|||||||||  " + nombre_simulacion + "  |||||||||")
        print("|---------------------------------")
        print('|')
        
        time.sleep(3)
        self.crear_mesas(usuario_ingresado)

    def uno(self):
        print('|')
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
                print('|')
                print("|El usuario no existe, pruebe otro")
                time.sleep(2)
                file.close()
                self.consola()
            file.close()
            print('|')
        print("|Ingrese su contraseña: ")
        contraseña_ingresada = input("|>>  ")
        verificador = verificar_contraseña(contraseña_ingresada, usuario_ingresado)
        if verificador == True:
            time.sleep(1)
            print('----------------------------------------')
            print("|Bienvenido " + usuario_ingresado)
            print('----------------------------------------')
            time.sleep(1)
            self.nombre_simulacion(usuario_ingresado)
        if verificador == False:
            print('|')
            print("|Contraseña incorrecta")
            time.sleep(2)
            self.consola()
            
    def consola(self):
        print('----------------------------------------')
        print("|Bienvenido al simulador 'Restaurant City'")
        time.sleep(1)
        print("|1 - Iniciar sesion")
        time.sleep(1)
        print("|2 - Registrar nuevo usuario")
        time.sleep(1)
        print("|3 - Salir")
        time.sleep(1)
        print("|4 - Resultados históricos (Coming soon))")
        time.sleep(1)
        print('|')
        print("|Ingrese el numero de la opcion que desea realizar:")
        opcion = input('|>>  ')
        if opcion == "1" or opcion == "2" or opcion == "3":
            pass
        else:
            print('|')
            print("|Ingrese una opcion valida")
            time.sleep(2)
            self.consola()
        if opcion == "3":
            self.tres()

        if opcion == "2":
            self.dos()
        if opcion == "1":
            self.uno()
            
    
restaurante = Simulador()
restaurante.consola()

