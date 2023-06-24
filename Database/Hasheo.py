import hashlib
import os

clave_inicio = "adminasdsdfaergnlnqj!@#r412354ejfoiasdnvjklzdkvna//as".encode("utf-8") #Hago esto porque no me salio generar un inicio aleatorio y almacenarlo para despues usarlo. sal = os.urandom(16)

def hashear_contraseña(contraseña_hashear_hasheo):
    contraseña_hasheada_hasheo = hashlib.pbkdf2_hmac("sha256", contraseña_hashear_hasheo.encode("utf-8"), clave_inicio, 100000).hex()
    return contraseña_hasheada_hasheo

def verificar_contraseña(contraseña_ingresada_hasheo, usuario_ingresado_hasheo):
    verificador = False
    with open("users.txt", "r") as file1:
        usuarios_almacenados_hasheo = []
        contraseñas_almacenadas_hasheo = []
        for line1 in file1.readlines():
            usuario_almacenado_hasheo, contraseña_almacenada_hasheo = line1.strip().split(",")
            usuarios_almacenados_hasheo.append(usuario_almacenado_hasheo)
            contraseñas_almacenadas_hasheo.append(contraseña_almacenada_hasheo)
        file1.close()
    hs = hashear_contraseña(contraseña_ingresada_hasheo)
   
    for i in range(len(contraseñas_almacenadas_hasheo)):
        if hs == contraseñas_almacenadas_hasheo[i] and usuario_ingresado_hasheo == usuarios_almacenados_hasheo[i]:      
            verificador = True
    return verificador