from SimClasses import instance
import time
from Hasheo import *



    
class Usuario:
    def ___innit___(self):
        self.nombre_usuario = ""
        self.contraseña_usuario = ""
    
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
                if usuarios_almacenados[i] == self.nombre_usuario:
                    usuario_existe = True
                    file.close()
            file.close()
        return usuario_existe
    
    def verificar_constraseña_usuario(self, nombre_usuario, contraseña, repetir_contraseña):
        contraseñas_iguales = True
        if contraseña != repetir_contraseña:
            contraselas_iguales = False
        return contraseñas_iguales
    
    def try_guardar_usuario_en_archivo(self, nombre_usuario, contraseña):
        with open("users.txt", "a") as file:
                    if file.closed:
                        print('|')
                        print("|El banco de usuarios no puede ser accedido. Intente en otro momento.")
                        exit()
                    contraseña_hashear = hashear_contraseña(contraseña)
                    file.write(f"{nombre_usuario},{contraseña_hashear}\n")
                    file.close()
                    print('|')
                    print("|Usuario creado con exito")
    
    def except_guardar_usuario_en_archivo(self, nombre_usuario, contraseña):
        with open("users.txt", "w") as file: 
                    contraseña_hashear = hashear_contraseña(contraseña)
                    file.write(f"{nombre_usuario},{contraseña_hashear}\n")
                    file.close()
                    print('|')
                    print("|Usuario creado con exito")
        
                    
    
    