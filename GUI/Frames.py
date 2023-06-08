import tkinter as tk
from DataClasses import PaqueteUsuario
from enum import Enum
import re

# Contiene todos las pestañas posibles. Hard coded, agregar aca y en linea 54 una nueva pestaña si se necesita.
class WindowEnum(Enum):
    LOGIN = 0,
    REGISTER = 1,
    MAIN_MENU = 2

# La clase root del GUI, esto es lo que muestra toda informacion.
class App(tk.Tk):

    appPhoto: (tk.PhotoImage | None) = None

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Configurar root window
        self.title('Simulador de Restaurante: EDYP')

        if(App.appPhoto is None):
            App.appPhoto = tk.PhotoImage(file=self.__chooseAppIcon())

        self.iconphoto(False, App.appPhoto)

        # Handlers
        self.windowHandler = WindowHandler(self)

        self.container: tk.Frame
    
    # Funcion que elige al azar el icono de la aplicacion entre las variantes
    def __chooseAppIcon(self) -> str:
        from random import randint
        
        return "GUI/Images/PNG/opcion" + str(randint(1,3)) + ".png"
    
# Handlers -> Clases que manejan ciertos aspectos de la aplicacion, los cuales pueden ser referenciados directamente por los frames
class WindowHandler():
    def __init__(self, app: App) -> None:
        self.app = app
        app.state("zoomed")
        app.minsize(width=500, height=400)
    
        app.container = tk.Frame(app)
        app.container.pack(side="top", fill="both", expand = True)

        # Cambiar la cantidad de rows y columns del display (DEJAR EN 0 AMBAS)
        app.container.grid_rowconfigure(0, weight=1)
        app.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[WindowEnum, AppWindow] = {}
        
        self.__loadFrames()
    
    # Esto esta hardcoded, no creo que sea necesario cambiar esto excepto si se crean nuevos frames
    def __loadFrames(self) -> None:
        for we in (WindowEnum.LOGIN,WindowEnum.REGISTER, WindowEnum.MAIN_MENU):
            frame: AppWindow

            match we:
                case WindowEnum.LOGIN:
                    frame = LoginWindow(self.app.container, self)

                case WindowEnum.REGISTER:
                    frame = RegistroUsuarioWindow(self.app.container, self)

                case WindowEnum.MAIN_MENU:
                    frame = MenuPrincipalWindow(self.app.container, self)

            self.frames[we] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.cambiarWindow(WindowEnum.LOGIN)

    def cambiarWindow(self, nextWindow: WindowEnum) -> None:
        frame = self.frames[nextWindow]
        frame.tkraise()

class DataHandler():
    pass
class DatabaseHandler():
    pass

# Esta es nuestra clase generica de window, cualquier cambio que queremos que ocurra en todos los frames se aplica aca.
class AppWindow(tk.Frame):

    h1 = ("Times New Roman", 50)
    h2 = ("Times New Roman", 20)
    h3 = ("Times New Roman", 14)
    h4 = ("Times New Roman", 9)

    def __init__(self, master: tk.Tk, windowHandler:WindowHandler, *args, **kwargs) -> None:
        self.windowHandler = windowHandler
        super().__init__(master,kwargs)

        #Configuracion Filas y Columnas
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

# Esta clase representa el window de login de la aplicacion
class LoginWindow(AppWindow):

    def __init__(self, master: tk.Tk, windowHandler:WindowHandler, *args, **kwargs) -> None:
        super().__init__(master,windowHandler, *args, **kwargs)
        # Variables
        self._paqueteUsuario = PaqueteUsuario()

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
        self.windowHandler.cambiarWindow(WindowEnum.MAIN_MENU)

    def __requestRegistrarUsuario(self) -> None:
        self.windowHandler.cambiarWindow(WindowEnum.REGISTER)
    
    def __loadCallbacks(self) -> None:
        # Lista de Callbacks registradas
        self._inputUsuarioCallback = self.register(self.__validarInputUsuario)
        self._inputPasswordCallback = self.register(self.__validarInputPassword)
    
    def __loadWidgets(self) -> None:

        # Lista de Widgets presentes
        self._mainFrame = tk.Frame(self)
        self._mainFrame.grid(row=2, column=2)
        
        self._titulo = tk.Label(self._mainFrame, text= "Login", font=super().h1)
        self._titulo.pack(pady=10)

        self._label_usuario = tk.Label(self._mainFrame, text= "Ingresar Usuario", font= super().h2)
        self._label_usuario.pack()

        self._entry_usuario = tk.Entry(self._mainFrame, width= 40, font= super().h2, validate="key", validatecommand=(self._inputUsuarioCallback, "%P"))
        self._entry_usuario.pack(padx=5, pady=5)

        self._label_password = tk.Label(self._mainFrame, text= "Ingresar Contraseña", font= super().h2)
        self._label_password.pack()

        self._entry_password = tk.Entry(self._mainFrame, width=40,show="*", font= super().h2, validate="key", validatecommand=(self._inputPasswordCallback, "%P"))
        self._entry_password.pack(padx=5, pady=5)

        self._request_login_button = tk.Button(self._mainFrame, width=10, height=2, text= "Log In", font= super().h3, command=self.__requestLogin)
        self._request_login_button.pack(pady=5)

        self._request_registrar_button = tk.Button(self, width=50, height=1, text= "No tienes Usuario? Registrarse aqui", font= super().h4, command= self.__requestRegistrarUsuario)
        self._request_registrar_button.grid(row=3, column=2, pady=5)

# Esta clase representa el frame de registracion para usuario nuevo de la aplicacion
class RegistroUsuarioWindow(AppWindow):

    def __init__(self, master: tk.Tk, windowHandler:WindowHandler, *args, **kwargs) -> None:
        super().__init__(master,windowHandler, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

        self.validaciones: dict[str,bool] = {
            "Usuario": False,
            "Password1": False,
            "Password2": False,
            "Email": False
        }

    def __requestRegistrar(self):
        resultados = 0

        for k,v in self.validaciones.items():
            if(v):
                resultados += 1
            
            print(f"{k}: {v}")

        if (resultados == len(self.validaciones)):
            print("Usuario ha sido creado correctamente!")
        else:
            print("Hay un error en la registracion.")


    def __returnLogin(self):
        self.windowHandler.cambiarWindow(WindowEnum.LOGIN)

    # ✔ ✖ , Validadores

    def __validarInputUsuario(self, input: str) -> bool:
        
        if(len(input) == 0):
            self._label_usuario_verificado.config(text="✖", fg="#880808", bg="#FFF") #Despues usar palette o algo
            self.validaciones["Usuario"] = False
        else:
            self._label_usuario_verificado.config(text="✔", fg="#DAF7A6", bg="#FFF")
            self.validaciones["Usuario"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputPassword1(self, input: str) -> bool:
        
        if(len(input) == 0):
            self._label_password1_verificado.config(text="✖", fg="#880808", bg="#FFF") #Despues usar palette o algo
            self.validaciones["Password1"] = False
        else:
            self._label_password1_verificado.config(text="✔", fg="#DAF7A6", bg="#FFF")
            self.validaciones["Password1"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputPassword2(self, input: str) -> bool:
        
        if(input != self._entry_password_1.get()):
            self._label_password2_verificado.config(text="✖", fg="#880808", bg="#FFF") #Despues usar palette o algo
            self.validaciones["Password2"] = False
        else:
            self._label_password2_verificado.config(text="✔", fg="#DAF7A6", bg="#FFF")
            self.validaciones["Password2"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputEmail(self, input: str) -> bool:
        
        if(not re.match(r"[^@]+@[^@]+\.[^@]+", input)):
            self._label_email_verificado.config(text="✖", fg="#880808", bg="#FFF") #Despues usar palette o algo
            self.validaciones["Email"] = False
        else:
            self._label_email_verificado.config(text="✔", fg="#DAF7A6", bg="#FFF")
            self.validaciones["Email"] = True
        
        return True
        
    def __loadCallbacks(self) -> None:
        self._validarInputUsuarioCallback = self.register(self.__validarInputUsuario)
        self._validarInputPassword1Callback = self.register(self.__validarInputPassword1)
        self._validarInputPassword2Callback = self.register(self.__validarInputPassword2)
        self._validarInputEmailCallback = self.register(self.__validarInputEmail)
        pass

    def __loadWidgets(self) -> None:

        # Frame de los botones
        self._buttonFrame = tk.Frame(self)
        self._buttonFrame.grid(row=3, column=2, pady=5)
        self._buttonFrame.grid_rowconfigure(1)
        self._buttonFrame.grid_columnconfigure(3, pad=5)

        self._registrar_button = tk.Button(self._buttonFrame, width=15, height=1, text= "Registrarse", font= super().h4, command= self.__requestRegistrar)
        self._registrar_button.grid(row=1, column=2)

        self._back_button = tk.Button(self._buttonFrame, width=15, height=1, text= "Volver", font= super().h4, command= self.__returnLogin)
        self._back_button.grid(row=1, column=3)

        # Frame con labels y entry requeridos para cuenta

        self._registrarInfoFrame = tk.Frame(self)
        self._registrarInfoFrame.grid(row=2, column=2)
        self._registrarInfoFrame.grid_rowconfigure(5)
        self._registrarInfoFrame.grid_columnconfigure(3, minsize=50)

        self._titulo = tk.Label(self._registrarInfoFrame, text= "Registrar Nueva Cuenta", font=super().h1)
        self._titulo.grid(row=1, column=1, columnspan=3, pady=10)

        self._label_usuario = tk.Label(self._registrarInfoFrame, text= "Ingresar Usuario: ", font= super().h3)
        self._label_usuario.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self._entry_usuario = tk.Entry(self._registrarInfoFrame, width= 40, font= super().h2, validate="key", validatecommand= (self._validarInputUsuarioCallback, "%P"))
        self._entry_usuario.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)

        self._label_usuario_verificado = tk.Label(self._registrarInfoFrame, text= "", font= super().h3)
        self._label_usuario_verificado.grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)

        self._label_password_1 = tk.Label(self._registrarInfoFrame, text= "Ingresar Contraseña:", font= super().h3)
        self._label_password_1.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self._entry_password_1 = tk.Entry(self._registrarInfoFrame, width=40,show="*", font= super().h2, validate="key", validatecommand= (self._validarInputPassword1Callback, "%P"))
        self._entry_password_1.grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)

        self._label_password1_verificado = tk.Label(self._registrarInfoFrame, text= "", font= super().h3)
        self._label_password1_verificado.grid(row=3, column=3, padx=5, pady=5, sticky=tk.E)

        self._label_password_2 = tk.Label(self._registrarInfoFrame, text= "Repetir Contraseña:", font= super().h3)
        self._label_password_2.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self._entry_password_2 = tk.Entry(self._registrarInfoFrame, width=40,show="*", font= super().h2, validate="key", validatecommand= (self._validarInputPassword2Callback, "%P"))
        self._entry_password_2.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

        self._label_password2_verificado = tk.Label(self._registrarInfoFrame, text= "", font= super().h3)
        self._label_password2_verificado.grid(row=4, column=3, padx=5, pady=5, sticky=tk.E)

        self._label_email = tk.Label(self._registrarInfoFrame, text= "Ingresar Email:", font= super().h3)
        self._label_email.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        self._entry_email = tk.Entry(self._registrarInfoFrame, width= 40, font= super().h2, validate="key", validatecommand= (self._validarInputEmailCallback, "%P"))
        self._entry_email.grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)

        self._label_email_verificado = tk.Label(self._registrarInfoFrame, text= "", font= super().h3)
        self._label_email_verificado.grid(row=5, column=3, padx=5, pady=5, sticky=tk.E)
        


# Esta clase representa el frame del main menu para el usuario de la aplicacion
class MenuPrincipalWindow(AppWindow):
    def __init__(self, master: tk.Tk, windowHandler:WindowHandler, *args, **kwargs) -> None:
        super().__init__(master,windowHandler, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()


    def __goBack(self):
        self.windowHandler.cambiarWindow(WindowEnum.LOGIN)

    def __loadCallbacks(self):
        pass

    def __loadWidgets(self):
        
        self._back_button = tk.Button(self, width=50, height=1, text= "Retornar a Log in", font= super().h4, command= self.__goBack)
        self._back_button.pack()
    pass

# Esta clase representa el frame de crear una nueva simulacion para el usuario
class CrearSimulacionFrame(AppWindow):
    pass

# Esta clase representa el frame de espera de la simulacion
class EsperaSimulacionFrame(AppWindow):
    pass

# Esta clase representa el frame de resultados de la simulacion
class ResultadoSimulacionFrame(AppWindow):
    pass
