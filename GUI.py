from Hasheo import *

#Va a haber que agregar muchos verificadores acá. Especialmente cuando interactuamos con el users.txt

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
        with open("users.txt", "a") as file:    
            contraseña_hashear = hashear_contraseña(contraseña)
            file.write(f"{usuario},{contraseña_hashear}\n")
            file.close()
            print("|Usuario creado con exito")
            consola()

def dos():
    print("|Creando nuevo usuario...")
    print("|Ingrese su nombre de usuario:")
    usuario = str(input('|>>  ').strip())
    with open("users.txt", "r") as file:
        usuario_almacenado = []
        for line in file.readlines():
            usuario_almacenado, contraseña_almacenada = line.strip().split(",")
        if usuario_almacenado == usuario:
            print("|El usuario ya existe, pruebe otro")
            file.close()
            dos()
        else:
            file.close()
            registrar_usuario(usuario)

def uno():
    print("|Ingrese su nombre de usuario: ")
    usuario_ingresado = str(input('|>>  ').strip())
    print("|Ingrese su contraseña: ")
    contraseña_ingresadaa = input(">>  ")
    if verificar_contraseña(contraseña_ingresadaa, usuario_ingresado) == True:
        print("|Bienvenido " + usuario_ingresado)
        print('----------------------------------------')
    else:
        print("|Contraseña incorrecta")
        uno() #Ojo con esto puedo estar en un loop infinito. Lo mismo con las otras opciones chequear.

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