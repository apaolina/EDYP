import tkinter as tk
from DataClasses import PaqueteUsuario
from enum import Enum

# Contiene todos las pestañas posibles. Hard coded, agregar aca y en linea 54 una nueva pestaña si se necesita.
class FrameEnum(Enum):
    LOGIN = 0,
    REGISTER = 1,
    MAIN_MENU = 2

# La clase root del GUI, esto es lo que muestra toda informacion.
class App(tk.Tk):

    appPhoto: tk.PhotoImage = None

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Configurar root window
        self.title('Simulador de Restaurante: EDYP')

        if(App.appPhoto is None):
            App.appPhoto = tk.PhotoImage(file=self.__chooseAppIcon())

        self.iconphoto(False, App.appPhoto)

        # Handlers
        self.frameHandler = FrameHandler(self)
    
    # Funcion que elige al azar el icono de la aplicacion entre las variantes
    def __chooseAppIcon(self) -> str:
        from random import randint
        
        return "GUI\Images\PNG\opcion" + str(randint(1,3)) + ".png"
    
# Handlers -> Clases que manejan ciertos aspectos de la aplicacion, los cuales pueden ser referenciados directamente por los frames
class FrameHandler():
    def __init__(self, app: tk.Tk) -> None:
        self.app = app
        app.state("zoomed")
        app.minsize(width=500, height= 300)
    
        app.container = tk.Frame(app)
        app.container.pack(side="top", fill="both", expand = True)

        # Cambiar la cantidad de rows y columns del display (DEJAR EN 0 AMBAS)
        app.container.grid_rowconfigure(0, weight=1)
        app.container.grid_columnconfigure(0, weight=1)

        self.frames: dict[FrameEnum, AppWindow] = {}
        
        self.__loadFrames()
    
    # Esto esta hardcoded, no creo que sea necesario cambiar esto excepto si se crean nuevos frames
    def __loadFrames(self) -> None:
        for we in (FrameEnum.LOGIN,FrameEnum.REGISTER):
            frame: AppWindow

            match we:
                case FrameEnum.LOGIN:
                    frame = LoginFrame(self.app.container, self)

                case FrameEnum.REGISTER:
                    frame = RegistroUsuarioFrame(self.app.container, self)

            self.frames[we] = frame

            frame.grid(row=0,column=0,sticky="nsew")
        
        self.cambiarWindow(FrameEnum.LOGIN)

    def cambiarWindow(self, nextWindow: FrameEnum) -> None:
        frame = self.frames[nextWindow]
        frame.tkraise()
class DataHandler():
    pass
class DatabaseHandler():
    pass

# Esta es nuestra clase generica de frame, cualquier cambio que queremos que ocurra en todos los frames se aplica aca.
class AppWindow(tk.Frame):

    h1 = ("Times New Roman", 50)
    h2 = ("Times New Roman", 20)
    h3 = ("Times New Roman", 10)
    h4 = ("Times New Roman", 9)

    def __init__(self, master: tk.Tk, frameHandler: FrameHandler, *args, **kwargs) -> None:
        self.frameHandler = frameHandler
        super().__init__(master,kwargs)

# Esta clase representa el frame de login de la aplicacion
class LoginFrame(AppWindow):

    def __init__(self, master: tk.Tk, frameHandler: FrameHandler, *args, **kwargs) -> None:
        super().__init__(master, frameHandler, *args, **kwargs)
        # Variables
        self._paqueteUsuario = PaqueteUsuario()

        self.__loadCallbacks()
        self.__loadWidgets()

        #Configuracion Filas y Columnas
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)


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
        self.frameHandler.cambiarWindow(FrameEnum.MAIN_MENU)

    def __requestRegistrarUsuario(self) -> None:
        self.frameHandler.cambiarWindow(FrameEnum.REGISTER)
    
    def __loadCallbacks(self) -> None:
        # Lista de Callbacks registradas
        self._input_usuario = self.register(self.__validarInputUsuario)
        self._input_password = self.register(self.__validarInputPassword)
    
    def __loadWidgets(self) -> None:

        # Lista de Widgets presentes
        self._mainFrame = tk.Frame(self)
        self._mainFrame.grid(row=2,column=2)
        
        self._titulo = tk.Label(self._mainFrame, text= "Login", font=super().h1)
        self._titulo.pack(pady= 10)

        self._label_usuario = tk.Label(self._mainFrame, text= "Ingresar Usuario", font= super().h2)
        self._label_usuario.pack()

        self._entry_usuario = tk.Entry(self._mainFrame, width= 40, font= super().h2)
        self._entry_usuario.config(validate="key", validatecommand=(self._input_usuario, "%P"))
        self._entry_usuario.pack(padx= 5, pady=5)

        self._label_password = tk.Label(self._mainFrame, text= "Ingresar Contraseña", font= super().h2)
        self._label_password.pack()

        self._entry_password = tk.Entry(self._mainFrame, width=40,show="*", font= super().h2)
        self._entry_password.config(validate="key", validatecommand=(self._input_password, "%P"))
        self._entry_password.pack(padx= 5, pady= 5)

        self._request_login_button = tk.Button(self._mainFrame, width=10, height=2, text= "Log In", font= super().h3, command=self.__requestLogin)
        self._request_login_button.pack(pady=5)

        self._request_registrar_button = tk.Button(self, width=50, height=1, text= "No tienes Usuario? Registrarse aqui", font= super().h4, command= self.__requestRegistrarUsuario)
        self._request_registrar_button.grid(row=3,column=2, pady=5)

# Esta clase representa el frame de registracion para usuario nuevo de la aplicacion
class RegistroUsuarioFrame(AppWindow):

    def __init__(self, master: tk.Tk, frameHandler: FrameHandler, *args, **kwargs) -> None:
        super().__init__(master, frameHandler, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()


    def __goBack(self):
        self.frameHandler.cambiarWindow(FrameEnum.LOGIN)

    def __loadCallbacks(self):
        pass

    def __loadWidgets(self):
        
        self._back_button = tk.Button(self, width=50, height=1, text= "Retornar a Log in", font= super().h4, command= self.__goBack)
        self._back_button.pack()

# Esta clase representa el frame del main menu para el usuario de la aplicacion
class MenuPrincipalFrame(AppWindow):
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
