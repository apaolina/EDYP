import json
from typing import Callable
from Hasheo import * #Tuve que hacer un copy del archivo y meterlo en la carpeta Database porque no me lo reconocia.

class DataManager():

    def __init__(self) -> None:
        self.database = "Database/database.json"
        pass

    def validarUsuarioTomado(self, input:str) -> bool:
        with open(self.database, "r") as file:
            file_data: list = json.load(file)
            if(any(user['usuario'] == input for user in file_data['Usuarios'])):
                return False
            else:
                return True
            
    def validarEmailTomado(self, input:str) -> bool:
        with open(self.database, "r") as file:
            file_data: list = json.load(file)
            if(any(user['email'] == input for user in file_data['Usuarios'])):
                return False
            else:
                return True

    def requestRegistrar(self, usuario: str, password: str, email: str, callback: Callable[[bool], None]) -> None:
        
        # Aca utilizar encriptacion para ingresar al .json el password
        password = hashear_contraseña(password)
        
        try:
            paquete = {
                "usuario": usuario,
                "password": password,
                "email": email
            }

            with open(self.database,"r+") as file:
                file_data = json.load(file)
                file_data["Usuarios"].append(paquete)
                file.seek(0)
                json.dump(file_data,file,indent = 4)
            
            callback(True)
        except:
            callback(False)
            

    def requestLogin(self, usuario: str, password:str, callback: Callable[[bool], None]) -> (str | None):
        with open(self.database,"r+") as file:
            file_data = json.load(file)
            if(any(user['usuario'] == usuario and user['password'] == hashear_contraseña(password) for user in file_data['Usuarios'])):
                callback(True)
                return usuario
            else:
                callback(False)
                return False
            
    def cargarSimulacion(self, usuario:str, nombre: str, cantidad_meseros: str, cantidad_cocineros: str, clientes_por_hora: str,\
                         lista_mesas:dict[str,list[str,str]], lista_platos:dict[str,list[str,str]], tiempo_simulado: str,\
                            tiempo_por_tick:str, callback:Callable[[bool],None]):

        try:
            id = 0
            dict_mesas: dict[str, str] = {}
            dict_platos: dict[str,str] = {}

            for v in lista_mesas.values():
                dict_mesas[v[0]] = v[1]

            for v in lista_platos.values():
                dict_platos[v[0]] = v[1]

            paquete = {
                "id": 0,
                "usuario": usuario,
                "nombre": nombre,
                "cantidad_meseros": cantidad_meseros,
                "cantidad_cocineros": cantidad_cocineros,
                "clientes_por_hora": clientes_por_hora,
                "lista_mesas": dict_mesas,
                "lista_platos": dict_platos,
                "tiempo_simulado": tiempo_simulado,
                "tiempo_por_tick": tiempo_por_tick,
                "eventos": ""
            }

            with open(self.database,"r+") as file:
                file_data = json.load(file)
                id = len(file_data["Simulaciones"]) + 1
                paquete["id"] = str(id)
                file_data["Simulaciones"].append(paquete)
                file.seek(0)
                json.dump(file_data,file,indent = 4)
            
            callback(True, id)
        except:
            callback(False, None)
