import tkinter as tk
from DataClasses import PaqueteUsuario
from typing import Callable
from enum import Enum

class WindowEnum(Enum):
    LOGIN = 0,
    REGISTER = 1,
    MAIN_MENU = 2

# Este es nuestra clase generica de applicacion, cualquier cambio que queremos que ocurra en toda la applicacion se aplica aca.
class AppWindow(tk.Tk):

    appPhoto: tk.PhotoImage = None

    h1 = ("Times New Roman", 50)
    h2 = ("Times New Roman", 20)
    h3 = ("Times New Roman", 10)
    h4 = ("Times New Roman", 9)

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Configurar root window
        self.title('Simulador de Restaurante: EDYP')

        if(AppWindow.appPhoto is None):
            AppWindow.appPhoto = tk.PhotoImage(file=self.__chooseAppIcon())

        self.iconphoto(False, AppWindow.appPhoto)
        self.state("zoomed")
        self.minsize(width=500, height= 300)

        # Lista de Widgets presentes
        self.frame = tk.Frame()
        self.frame.pack()

    # Funcion que elige al azar el icono de la aplicacion entre las variantes
    def __chooseAppIcon(self) -> str:
        from random import randint
        
        return "GUI\Images\PNG\opcion" + str(randint(1,3)) + ".png"


# Esta clase representa el login de la aplicacion principal
class Login(AppWindow):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None, callback: (Callable[[WindowEnum],None] | None) = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Variables
        self._paqueteUsuario = PaqueteUsuario()
        if(callback is not None):
            self._changeWindows = callback

        self.__loadCallbacks()
        self.__loadWidgets()


    #Metodos Publicos
    def getPaqueteUsuario(self) -> PaqueteUsuario:
        return self._paqueteUsuario


    # Validadores de Input
    def __validarInputUsuario(self, input:str) -> bool:
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        self._paqueteUsuario.usuario = input
        return True
    
    def __validarInputPassword(self, input:str) -> bool:
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        self._paqueteUsuario.password = input
        return True
    
    # Metodos de Botones
    def __requestLogin(self) -> None:
        self._changeWindows(WindowEnum.MAIN_MENU)

    def __requestRegistrarUsuario(self) -> None:
        self._changeWindows(WindowEnum.REGISTER)
    
    def __loadCallbacks(self) -> None:
        # Lista de Callbacks registradas
        self._input_usuario = self.register(self.__validarInputUsuario)
        self._input_password = self.register(self.__validarInputPassword)
    
    def __loadWidgets(self) -> None:

        # Lista de Widgets presentes
        self._titulo = tk.Label(self, text= "Login", font=super().h1)
        self._titulo.pack(pady= 10)

        self._label_usuario = tk.Label(self, text= "Ingresar Usuario", font= super().h2)
        self._label_usuario.pack()

        self._entry_usuario = tk.Entry(self, width= 40, font= super().h2)
        self._entry_usuario.config(validate="key", validatecommand=(self._input_usuario, "%P"))
        self._entry_usuario.pack(padx= 5, pady=5)

        self._label_password = tk.Label(self, text= "Ingresar Contraseña", font= super().h2)
        self._label_password.pack()

        self._entry_password = tk.Entry(self, width=40,show="*", font= super().h2)
        self._entry_password.config(validate="key", validatecommand=(self._input_password, "%P"))
        self._entry_password.pack(padx= 5, pady= 5)

        self._request_login_button = tk.Button(self, width=10, height=2, text= "Log In", font= super().h3, command=self.__requestLogin)
        self._request_login_button.pack(pady=5)

        self._request_registrar_button = tk.Button(self, width=50, height=1, text= "No tienes Usuario? Registrarse aqui", font= super().h4, command= self.__requestRegistrarUsuario)
        self._request_registrar_button.pack(pady=5, side= "bottom")


class RegistroUsuario(AppWindow):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)