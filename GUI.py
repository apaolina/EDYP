from Hasheo import *

def tres():
            print('|Programa cerrado')
            print('----------------------------------------')
            exit()

def registrar_usuario(usuario):
    with open("users.txt", "a") as file:
        print("|Ingrese su contraseña: ")
        contraseña = input(">>  ")
        print("|Repita su contraseña: ")
        contraseña2 = input(">>  ")
        if contraseña != contraseña2:
            print("|Las contraseñas no coinciden, intente nuevamente")
            registrar_usuario(usuario)
        else:
            contraseña_hasheada = hashear_contraseña(contraseña)
            file.write(f"{usuario},{contraseña_hasheada}\n")
            file.close()
            print("|Usuario creado con exito")


def dos():
    print("|Creando nuevo usuario...")
    print("|Ingrese su nombre de usuario:")
    usuario = str(input('|>>  ').strip())
    with open("users.txt", "r") as file:
        for line in file.readlines():
            usuario_almacenado, contraseña_almacenada = line.strip().split(",")
            if usuario_almacenado == usuario:
                print("|El usuario ya existe, pruebe otro")
                dos()
            else:
                registrar_usuario(usuario)
               
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
        
    


consola()