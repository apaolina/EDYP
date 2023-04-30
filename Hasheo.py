import hashlib
import os


inicio = "adminasdsdfaergnlnqj!@#r412354ejfoiasdnvjklzdkvna//as".encode("utf-8") #Hago esto porque no me salio generar un inicio aleatorio y almacenarlo para despues usarlo. sal = os.urandom(16)

def hashear_contraseña(contraseña1):
    contraseña_hasheada1 = hashlib.pbkdf2_hmac("sha256", contraseña1.encode("utf-8"), inicio, 100000).hex()
    return contraseña_hasheada1


def verificar_contraseña(contraseña_ingresada1, usuario_ingresado1):
    verificador = False
    with open("users.txt", "r") as file1:
        usuarios_almacenados1 = []
        contraseñas_almacenadas1 = []
        for line1 in file1.readlines():
            usuario_almacenado1, contraseña_almacenada1 = line1.strip().split(",")
            usuarios_almacenados1.append(usuario_almacenado1)
            contraseñas_almacenadas1.append(contraseña_almacenada1)
        file1.close()
    hs = hashear_contraseña(contraseña_ingresada1)
   
    for i in range(len(contraseñas_almacenadas1)):
        if hs == contraseñas_almacenadas1[i] and usuario_ingresado1 == usuarios_almacenados1[i]:      
            verificador = True
    return verificador
