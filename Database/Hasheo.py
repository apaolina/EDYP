import hashlib
import os

clave_inicio = "adminasdsdfaergnlnqj!@#r412354ejfoiasdnvjklzdkvna//as".encode("utf-8") #Hago esto porque no me salio generar un inicio aleatorio y almacenarlo para despues usarlo. sal = os.urandom(16)

def hashear_contraseña(contraseña_hashear_hasheo):
    contraseña_hasheada_hasheo = hashlib.pbkdf2_hmac("sha256", contraseña_hashear_hasheo.encode("utf-8"), clave_inicio, 100000).hex()
    return contraseña_hasheada_hasheo

