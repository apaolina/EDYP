from SimClasses import  instance
import time
import sys
from Hasheo import *
from Usuario import *
from Hasheo import verificar_contraseña
from InfoManager import InfoManager
from events import Events
import names
from typing import Callable

class Simulador:
    
    def __init__(self):
        self.nombre = ""
        self.cantidad_cocineros = 0
        self.cantidad_mozos = 0
        self.cantidad_mesas = 0
        self.clientes = 0
        self.clientes_generados = 0
        self.tiempo = 0
        self.usuario = Usuario()
        self.mesas: dict[str, list[str]] = {}
        self.lista_mesas = []
        self._mesas_dict: dict[str,list[str,list]] = {}
        self.instance = instance
        

    def opcion_tres(self):
        print('|')
        print('|Programa cerrado')
        print('----------------------------------------')
        exit()

    def registrar_usuario(self, usuario):
        print('|')
        print("|Ingrese su contraseña: ")
        contraseña = input("|>>  ")
        print("|Repita su contraseña: ")
        repetir_contraseña = input("|>>  ")
        if self.usuario.verificar_constraseña_usuario(usuario, contraseña, repetir_contraseña) == False:
            print("|Las contraseñas no coinciden, intente nuevamente")
            self.registrar_usuario(usuario)
        else:  
            try:
                self.usuario.try_guardar_usuario_en_archivo(usuario, contraseña)
                self.consola()
                    
            except FileNotFoundError:
                self.usuario.except_guardar_usuario_en_archivo(usuario, contraseña)
                self.consola()

    def opcion_dos(self):
        print('|')
        print("|Creando nuevo usuario...")
        print("|Ingrese su nombre de usuario:")
        usuario = str(input('|>>  ').strip())
        self.usuario.crear_usuario(usuario, "")
        if self.usuario.verificar_existencia_usuario(usuario) == True:
            print('|')
            print("|El usuario ya existe, intente con otro nombre de usuario")
            print('|')
            self.consola()
        self.registrar_usuario(usuario)
        
    def registrar_resultados(self):
        with open('resultadosSim.txt', 'a') as file:
            file.write(self.nombre + "," + str(self.cantidad_cocineros) + "," + str(self.cantidad_mozos) + "," + str(self.cantidad_mesas) + "," + str(self.clientes) + "," + str(self.clientes_generados) + "," + str(self.tiempo) + "\n")
            file.close()
            print('|')
            print("|Hasta luego")
            exit()

    def resultado_simulacion(self, start, end):
        print('|')
        print("----------------------------------------")
        print("|Resultados de la simulación:")
        print(f"|grupos: {self.instance.grupoManager.getCantidadGrupoClientes()}")
        print(f"|en cola: {self.instance.grupoManager.colaSentar.totalnodos}")
        print("|" + str(self.instance.mesaManager.verEstadoMesas()))
        print("|" +str(self.instance.cocinaManager.inventario))
        print("|" + str(end-start))
        self.clientes = self.instance.grupoManager.getCantidadGrupoClientes()
        self.clientes_generados = self.instance.grupoManager.getCantidadNClientes()
        print('|')
        print("|Los resultados se han almacenado con éxito en resultadosSim.txt")
        self.registrar_resultados()
        exit()
    
    def no_hago_nada(self):
        print("|Sim finalizada")

    def empezar_simulacion(self):
        print('|')
        print("|¿Cuánto es el tiempo a simular")
        tiempoSimulacion = input('|>>  ')
        if not tiempoSimulacion.isdigit():
            print('|')
            print("|El tiempo de simulación debe ser un número entero. Por favor, ingrese un número entero.")
            self.empezar_simulacion()
        tiempoSimulacion = int(tiempoSimulacion)
        self.tiempo = tiempoSimulacion
        start = time.time()
        self.instance.simular(self.cantidad_mozos, self.cantidad_cocineros, cantidad_clientes= 10, dict_mesas= self.mesas, dict_platos= {0:['Hamburguesa', 35], 1: ['Pancho', 35]}, tiempoSimulacionInput= self.tiempo, tiempoPorTick = 1, callback= self.no_hago_nada, id = 9999)
        end = time.time()
        self.resultado_simulacion(start, end)

    def crear_empleados(self):
        print('|')
        print("|Cuántos cocineros desea agregar a la simulación?")
        numero_cocineros = input('|>>  ')
        if not numero_cocineros.isdigit():
            print('|')
            print("|El numero de cocineros debe ser un numero entero. Ingrese nuevamente. ")
            self.crear_empleados()
        numero_cocineros = int(numero_cocineros)
        self.cantidad_cocineros = numero_cocineros
        nombres_Cocineros = []
        for i in range(1, numero_cocineros + 1):
            print("|Ingrese el nombre del cocinero " + str(i) + ":")
            nombre_cocinero = input('|>>  ')
            nombres_Cocineros.append(nombre_cocinero)
            
        print("|Ha creado " + str(numero_cocineros) + " cocineros con exito")
        print("|Nombres de los cocineros creados:")
        for nombre in nombres_Cocineros:
            print('|')
            print(f"|El cocinero {nombre} ha sido creado correctamente")
        
        print('|')    
        print("|Cuántos mozos desea agregar a la simulación?")
        numero_mozos = input('|>>  ')
        if not numero_mozos.isdigit():
            print('|')
            print("|El numero de mozos debe ser un numero entero. Ingrese  todo nuevamente. ")
            self.crear_empleados()
        numero_mozos = int(numero_mozos)
        nombres_Mozos = []
        self.cantidad_mozos = numero_mozos
        for i in range(1, numero_mozos + 1):
            print("|Ingrese el nombre del mozo " + str(i) + ":")
            nombre_mozo = input('|>>  ')
            nombres_Mozos.append(nombre_mozo)

        print("|Ha creado " + str(numero_mozos) + " mozos con exito")
        print("|Nombres de los mozos creados:")
        for nombre in nombres_Mozos:
            print('|')
            print(f"|El mozo {nombre} ha sido creado correctamente")
        self.empezar_simulacion()

    def crear_mesas(self, usuario_ingresado):
        print('|')
        print("|Bienvenido al simulador 'Restaurant City' " + usuario_ingresado)
        print('|')
        print("|¿Cuántas mesas desea agregar a la simulación?")
        mesas = input('|>>  ')
        if not mesas.isdigit():
            print('|')
            print("|El numero de mesas debe ser un numero entero. Ingrese nuevamente. ")
            self.crear_mesas(usuario_ingresado)
        
        mesas = int(mesas)
        self.cantidad_mesas = mesas
        print('|')
        print("|¿Desea que todas las mesas tengan la misma capacidad?")
        print("|1 - Si")
        print("|2 - No")
        respuesta = input('|>>  ')
        if respuesta != "1" and respuesta != "2":
            print('|')
            print("|La respuesta debe ser 1 o 2. Ingrese nuevamente. ")
            self.crear_mesas(usuario_ingresado)
        if respuesta == "1":
            print("|Ingrese la capacidad de las mesas:")
            capacidad_mesas = input('|>>  ')
            if not capacidad_mesas.isdigit():
                print('|')
                print("|La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
                self.crear_mesas(usuario_ingresado)
            
            capacidad_mesas = int(capacidad_mesas)
            
            for mesa in range(mesas):
                self.mesas[mesa] = [mesa,capacidad_mesas]
            
            print('|')
            print("|Ha creado " + str(mesas) + " mesas de " + str(capacidad_mesas) + " personas cada una")
            
            self.crear_empleados()
        if respuesta == "2":
            for i in range(1, mesas+1):
                print("|Ingrese la capacidad de la mesa " + str(i) + ":")
                capacidad_mesas = input('|>>  ')
                if not capacidad_mesas.isdigit():
                    print('|')
                    print("|La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
                    self.crear_mesas(usuario_ingresado)
        
                capacidad_mesas = int(capacidad_mesas)
                
                self.mesas[i] = [i,capacidad_mesas]
                
            print('|')
            print("|Ha creado " + str(mesas) + " mesas de diferentes capacidades")
            self.crear_empleados()
            
    def nombre_simulacion(self, usuario_ingresado):
        print("|Ingrese el nombre de la simulación:")
        nombre_simulacion = input('|>>  ')
        self.nombre = nombre_simulacion
        print('|')
        print('|')
        print("|---------------------------------")
        print("|||||||||  " + nombre_simulacion + "  |||||||||")
        print("|---------------------------------")
        print('|')
        
        self.crear_mesas(usuario_ingresado)

    def opcion_uno(self):
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
                file.close()
                self.consola()
            file.close()
            print('|')
        print("|Ingrese su contraseña: ")
        contraseña_ingresada = input("|>>  ")
        self.usuario.crear_usuario(usuario_ingresado, contraseña_ingresada)
        verificador = verificar_contraseña(contraseña_ingresada, usuario_ingresado)
        if verificador == True:
            print('----------------------------------------')
            print("|Bienvenido " + usuario_ingresado)
            print('----------------------------------------')
            self.nombre_simulacion(usuario_ingresado)
        if verificador == False:
            print('|')
            print("|Contraseña incorrecta")
            self.consola()
            
    def consola(self):
        print('----------------------------------------')
        print("|Bienvenido al simulador 'Restaurant City'")
        print("|1 - Iniciar sesion")
        print("|2 - Registrar nuevo usuario")
        print("|3 - Salir")
        print("|4 - Resultados históricos (Coming soon))")
        print('|')
        print("|Ingrese el numero de la opcion que desea realizar:")
        opcion = input('|>>  ')
        if opcion == "1" or opcion == "2" or opcion == "3":
            pass
        else:
            print('|')
            print("|Ingrese una opcion valida")
            self.consola()
        if opcion == "3":
            self.opcion_tres()

        if opcion == "2":
            self.opcion_dos()
        if opcion == "1":
            self.opcion_uno()
    
    def __str__(self):
        return f"Simulador: {self.nombre}, {self.cantidad_cocineros}, {self.cantidad_mozos}, {self.cantidad_mesas}, {self.clientes}, {self.clientes_generados}, {self.tiempo}"        

restaurante = Simulador()
restaurante.consola()

