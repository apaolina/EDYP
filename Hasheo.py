import hashlib
import os

def hashear_contraseña(contraseña):
    inicio = os.urandom(16)
    contraseña_hasheada = hashlib.pbkdf2_hmac("sha256", contraseña.encode(), inicio, 100000)
    return inicio, contraseña_hasheada

def verificar_contraseña(contraseña_almacenada, contraseña_ingresada, usuario_ingresado):
    with open("inicio.txt", "r") as file:
        for line in file.readlines():
            inicio = line
    with open("users.txt", "r") as file:
        for line in file.readlines():
            usuario_almacenado, contraseña_almacenada = line.strip().split(",")
    if contraseña_almacenada == hashlib.pbkdf2_hmac("sha256", contraseña_ingresada.encode(), inicio, 100000) and usuario_almacenado == usuario_ingresado:
        return True
    