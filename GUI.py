from Hasheo import *

def consola():
    print('----------------------------------------')
    print("Bienvenido al simulador 'Restaurant City'")
    print("1 - Iniciar sesion")
    print("2 - Registrar nuevo usuario")
    print("3 - Salir")
    print("Ingrese el numero de la opcion que desea realizar:")
    opcion = input('>>>>>')
    if opcion == "1" or opcion == "2" or opcion == "3":
        pass
    else:
        print("Ingrese una opcion valida")
        consola()
    if opcion == "3":
        print('Programa cerrado')
        print('----------------------------------------')
        exit()

consola()