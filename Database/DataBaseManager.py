import json
from typing import Callable

class DataManager():

    def __init__(self) -> None:
        self.login_data = "Database/login_data.json"
        pass

    def validarUsuarioTomado(self, input:str) -> bool:
        with open(self.login_data, "r") as file:
            file_data: list = json.load(file)
            if(any(user['usuario'] == input for user in file_data['Usuarios'])):
                return False
            else:
                return True
            
    def validarEmailTomado(self, input:str) -> bool:
        with open(self.login_data, "r") as file:
            file_data: list = json.load(file)
            if(any(user['email'] == input for user in file_data['Usuarios'])):
                return False
            else:
                return True

    def requestRegistrar(self, usuario: str, password: str, email: str, callback: Callable[[bool], None]) -> None:
        
        # Aca utilizar encriptacion para ingresar al .json el password
        
        try:
            paquete = {
                "usuario": usuario,
                "password": password,
                "email": email
            }

            with open(self.login_data,"r+") as file:
                file_data = json.load(file)
                file_data["Usuarios"].append(paquete)
                file.seek(0)
                json.dump(file_data,file,indent = 4)
            
            callback(True)
        except:
            callback(False)

    def requestLogin(self, usuario: str, password:str, callback: Callable[[bool], None]) -> None:
        with open(self.login_data,"r+") as file:
            file_data = json.load(file)
            if(any(user['usuario'] == usuario and user['password'] == password for user in file_data['Usuarios'])):
                callback(True)
            else:
                callback(False)