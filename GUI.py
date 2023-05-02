from SimClasses import instance
import time
from Hasheo import *
import os
#Va a haber que agregar muchos verificadores acá. Especialmente cuando interactuamos con el users.txt
#Tambien verificar que las respuestas sean numericas o strings, dependiendo de lo que se pida.
#DUDA para cada simulación es necesario crear mozos y cocineros nuevos o ya hay guardados, hay que eliminar a los viejos?
#Se me ocurre que habría que ponerle un nombre a cada simulación y guardar los resultados como los parametros de la simulación, los empleados que se crearon, etc. en un archivo de texto

def tres():
            print('|Programa cerrado')
            print('----------------------------------------')
            exit()

def registrar_usuario(usuario):
    print("|Ingrese su contraseña: ")
    contraseña = input(">>  ")
    print("|Repita su contraseña: ")
    contraseña2 = input(">>  ")
    if contraseña != contraseña2:
        print("|Las contraseñas no coinciden, intente nuevamente")
        registrar_usuario(usuario)
    else:
        try:
            with open("users.txt", "a") as file:
                if file.closed:
                    print("El banco de usuarios no puede ser accedido. Intente en otro momento.")
                    return False
        
                contraseña_hashear = hashear_contraseña(contraseña)
                file.write(f"{usuario},{contraseña_hashear}\n")
                file.close()
                print("|Usuario creado con exito")
                consola()
                
        except FileNotFoundError:
            with open("users.txt", "w") as file: 
                contraseña_hashear = hashear_contraseña(contraseña)
                file.write(f"{usuario},{contraseña_hashear}\n")
                file.close()
                print("|Usuario creado con exito")
                consola()
                
                 

def dos():
    print("|Creando nuevo usuario...")
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
                consola()
        file.close()
        registrar_usuario(usuario)

def resultado_simulacion(start, end):
    print("----------------------------------------")
    print("|Resultados de la simulación:")
    print(f"grupos: {instance.grupoManager.getCantidadGrupoClientes()}")
    print(f"en cola: {instance.grupoManager.colaSentar.totalnodos}")
    print(instance.mesaManager.verEstadoMesas())
    print(instance.cocinaManager.inventario)
    print(end-start)
    exit()

def empezar_simulacion():
    print("|¿Cuánto es el tiempo a simular")
    tiempoSimulacion = (input('|>>  '))
    
    if not tiempoSimulacion.isdigit():
        print("El tiempo de simulación debe ser un número entero. Por favor, ingrese un número entero.")
        empezar_simulacion()
        return
    tiempoSimulacion = int(input('|>>  '))
    start = time.time()
    instance.simular(tiempoSimulacion, tiempoPorTick = 1)
    end = time.time()
    resultado_simulacion(start, end)

def crear_empleados():
    print("|Cuántos cocineros desea agregar a la simulación?")
    numero_cocineros = (input('|>>  '))
    if not numero_cocineros.isdigit():
        print("El numero de cocineros debe ser un numero entero. Ingrese nuevamente. ")
        crear_empleados()
        return
    numero_cocineros = int(numero_cocineros)
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
    numero_mozos = (input('|>>  '))
    if not numero_mozos.isdigit():
        print("El numero de mozos debe ser un numero entero. Ingrese  todo nuevamente. ")
        crear_empleados()
        return
    numero_mozos = int(numero_mozos)
        #Por una cuestion tiempos no lo hago bien, pero habria que separar para que si no pone un numeero pida de nuevo 
        # el numero de mozos, no toda la funcion
        
    for i in range(1, numero_mozos + 1):
        print("|Ingrese el nombre del mozo " + str(i) + ":")
        nombre_mozo = input('|>>  ')
        instance.empleadoManager.crearMesero(nombre_mozo)
    print("|Ha creado " + str(numero_mozos) + " con exito")
    print("|Nombres de los mozos creados:")
    for i in range(1, numero_mozos + 1):
        print("|No se como hacer que se muestren los nombres de los mozos creados")
    empezar_simulacion()

def crear_mesas(usuario_ingresado):
    print("|Bienvenido al simulador 'Restaurant City' " + usuario_ingresado)
    print("|¿Cuántas mesas desea agregar a la simulación?")
    mesas = (input('|>>  '))
    if not mesas.isdigit():
        print("El numero de mesas debe ser un numero entero. Ingrese nuevamente. ")
        crear_mesas(usuario_ingresado)
        return
    mesas = int(mesas)
    
    print("|¿Desea que todas las mesas tengan la misma capacidad?")
    print("|1 - Si")
    print("|2 - No")
    respuesta = input('|>>  ')
    if respuesta != "1" and respuesta != "2":
        print("La respuesta debe ser 1 o 2. Ingrese nuevamente. ")
        crear_mesas(usuario_ingresado)
        return
    if respuesta == "1":
        print("|Ingrese la capacidad de las mesas:")
        capacidad_mesas = (input('|>>  '))
        if not capacidad_mesas.isdigit():
            print("La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
            crear_mesas(usuario_ingresado)
            return
        capacidad_mesas = int(capacidad_mesas)
         #Por una cuestion tiempos no lo hago bien, pero habria que separar para que si no pone un numeero pida de nuevo 
        # la capacidad, no toda la funcion
        
        for i in range(1, mesas+1):
            instance.mesaManager.crearMesa(capacidad_mesas)
        print("|Ha creado " + str(mesas) + " mesas de " + str(capacidad_mesas) + " personas cada una")
        crear_empleados()
    if respuesta == "2":
        for i in range(1, mesas+1):
            print("|Ingrese la capacidad de la mesa " + str(i) + ":")
            capacidad_mesas = (input('|>>  '))
            if not capacidad_mesas.isdigit():
                print("La capacidad de las mesas debe ser un numero entero. Ingrese nuevamente. ")
                crear_mesas(usuario_ingresado)
                return
            capacidad_mesas = int(capacidad_mesas)
            instance.mesaManager.crearMesa(capacidad_mesas)
        print("|Ha creado " + str(mesas) + " mesas de diferentes capacidades")
        crear_empleados()

def uno():
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
            consola()
        file.close()
    print("|Ingrese su contraseña: ")
    contraseña_ingresada = input("|>>  ")
    verificador = verificar_contraseña(contraseña_ingresada, usuario_ingresado)
    if verificador == True:
        print("|Bienvenido " + usuario_ingresado)
        print('----------------------------------------')
        crear_mesas(usuario_ingresado)
    if verificador == False:
        print("|Contraseña incorrecta")
        consola() 

def consola():
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
        consola()
    if opcion == "3":
        tres()

    if opcion == "2":
        dos()
    if opcion == "1":
        uno()
        
    


consola()