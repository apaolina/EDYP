import hashlib
import os

inicio = "adminasdsdfaergnlnqj!@#r412354ejfoiasdnvjklzdkvna//as".encode() #Hago esto porque no me salio generar un inicio aleatorio y almacenarlo para despues usarlo. sal = os.urandom(16)

def hashear_contraseña(contraseña):
    contraseña_hasheada = hashlib.pbkdf2_hmac("sha256", contraseña.encode(), inicio, 100000)
    return contraseña_hasheada

def verificar_contraseña(contraseña_ingresada, usuario_ingresado):
    with open("users.txt", "r") as file:
        for line in file.readlines():
            usuario_almacenado, contraseña_almacenada = line.strip().split(",")
    if contraseña_almacenada == hashlib.pbkdf2_hmac("sha256", contraseña_ingresada.encode(), inicio, 100000) and usuario_almacenado == usuario_ingresado:
        return True
    