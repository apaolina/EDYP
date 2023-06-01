from SimClasses import instance
import time
from Hasheo import *


#Creamos la clase usuario ya que es obligatioro :(
    
class Usuario:
    def ___innit___(self):
        nombre_usuario = ""
        contraseña_usuario = ""
    
    def crear_usuario(self, nombre_usuario, contraseña_usuario):
        self.nombre_usuario = nombre_usuario
        self.contraseña_usuario = contraseña_usuario
        
    def verificar_existencia_usuario(self, nombre_usuario):
        usuario_existe = False
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
                if usuarios_almacenados[i] == nombre_usuario:
                    usuario_existe = True
                    file.close()
            file.close()
        return usuario_existe
    
    
    