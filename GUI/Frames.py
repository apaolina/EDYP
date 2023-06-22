import tkinter as tk
from DataClasses import *
from enum import Enum
import sys
sys.path.insert(0,'Database')
from DataBaseManager import DataManager
from typing import Callable
import re
from tkinter import messagebox

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Contiene todos las pestañas posibles. Hard coded, agregar aca y en linea 54 una nueva pestaña si se necesita.
class WindowState(Enum):
    LOGIN = 0,
    REGISTER = 1,
    MAIN_MENU = 2,
    NEW_SIMULATION = 3,
    RESULTS_SIMULATION = 4,
    AWAITING_SIMULATION = 5,
    ALL_SIMULATIONS = 6

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
        self.userHandler = UserHandler(self)

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

        self.frames: dict[WindowState, AppWindow] = {}

        self.currentFrame = WindowState.LOGIN
        
        self.__loadFrames()

    # Esto esta hardcoded, no creo que sea necesario cambiar esto excepto si se crean nuevos frames
    def __loadFrames(self) -> None:
        for we in (WindowState.LOGIN,WindowState.REGISTER, WindowState.MAIN_MENU, WindowState.NEW_SIMULATION, WindowState.RESULTS_SIMULATION, WindowState.AWAITING_SIMULATION, WindowState.ALL_SIMULATIONS):
            frame: AppWindow

            match we:
                case WindowState.LOGIN:
                    frame = LoginWindow(self.app.container, self.app)

                case WindowState.REGISTER:
                    frame = RegistroUsuarioWindow(self.app.container, self.app)

                case WindowState.MAIN_MENU:
                    frame = MenuPrincipalWindow(self.app.container, self.app)
                
                case WindowState.NEW_SIMULATION:
                    frame = CrearSimulacionFrame(self.app.container, self.app)

                case WindowState.RESULTS_SIMULATION:
                    frame = ResultadoSimulacionFrame(self.app.container, self.app)

                case WindowState.AWAITING_SIMULATION:
                    frame = EsperaSimulacionFrame(self.app.container, self.app)

                case WindowState.ALL_SIMULATIONS:
                    frame = TodasSimulacionesFrame(self.app.container, self.app)

            self.frames[we] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        self.cambiarWindow(WindowState.LOGIN)

    def cambiarWindow(self, nextWindow: WindowState) -> None:
        frame = self.frames[nextWindow]
        frame.tkraise()
        self.frames[nextWindow].reset()
        self.currentFrame = nextWindow

class UserHandler():

    def __init__(self, app: App) -> None:
        self.app = app
        self.dataManager = DataManager()

        self.userIngresado: (str|None)
        pass

    def requestLogin(self,usuarioInput: str, passwordInput:str , callback: Callable[[bool],None]) -> None:
        self.userIngresado = self.dataManager.requestLogin(usuarioInput, passwordInput, callback)
        pass

    def validarUsuario(self, input:str) -> bool:
        return self.dataManager.validarUsuarioTomado(input)
    
    def validarEmail(self, input:str) -> bool:
        return self.dataManager.validarEmailTomado(input)

    def requestRegistrar(self, paquete: tuple[str], callback: Callable[[bool],None]) -> None:
        # Estructura de tuple : Usuario, Contraseña, Email
        self.dataManager.requestRegistrar(paquete[0],paquete[1],paquete[2], callback)
        pass

# Esta es nuestra clase generica de window, cualquier cambio que queremos que ocurra en todos los frames se aplica aca.
class AppWindow(tk.Frame):
    
    h1 = ("Times New Roman", 50)
    h2 = ("Times New Roman", 20)
    h3 = ("Times New Roman", 14)
    h4 = ("Times New Roman", 9)

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        
        self.app = app
        self.dataManager = DataManager()
        super().__init__(master,kwargs)

        #Configuracion Filas y Columnas
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

# Esta clase representa el window de login de la aplicacion
class LoginWindow(AppWindow):

    def __init__(self, master: tk.Tk, app:App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)
        # Variables
        self._paqueteUsuario = PaqueteUsuario()

        self.__loadCallbacks()
        self.__loadWidgets()

    def reset(self) -> None:
        self._entry_usuario.delete(0, tk.END)
        self._entry_password.delete(0, tk.END)

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
    
    def __loginCallback(self, result: bool) -> None:
        if(result):
            self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)
        else:
            from tkinter import messagebox
            self._popUp = tk.messagebox.showerror("Error", "Usuario o Contraseña incorrectos")
            self.app.windowHandler.cambiarWindow(WindowState.LOGIN)
            print("Usuario o Contraseña incorrectos")

    # Metodos de Botones
    def __requestLogin(self) -> None:
        self.app.userHandler.requestLogin(self._entry_usuario.get(), self._entry_password.get(), self.__loginCallback)
            

    def __requestRegistrarUsuario(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.REGISTER)
    
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

    def __registrarCallback(self, result: bool) -> None:
        if(result):
            self.app.windowHandler.cambiarWindow(WindowState.LOGIN)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudo registrar correctamente.")

    def reset(self) -> None:
        self._entry_usuario.delete(0, tk.END)
        self._entry_password_1.delete(0, tk.END)
        self._entry_password_2.delete(0, tk.END)
        self._entry_email.delete(0, tk.END)
        self._label_usuario_verificado.config(text="")
        self._label_password1_verificado.config(text="")
        self._label_password2_verificado.config(text="")
        self._label_email_verificado.config(text="")

    def __requestRegistrar(self):
        resultados = 0

        for k,v in self.validaciones.items():
            if(v):
                resultados += 1
            
            print(f"{k}: {v}")

        if (resultados == len(self.validaciones)):
            self.app.userHandler.requestRegistrar(paquete=(self._entry_usuario.get(), self._entry_password_2.get(), self._entry_email.get()), callback=self.__registrarCallback)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "No se pudo registrar correctamente.")


    def __returnLogin(self):
        self.app.windowHandler.cambiarWindow(WindowState.LOGIN)

    # ✔ ✖ , Validadores

    def __validarInputUsuario(self, input: str) -> bool:
        
        if(len(input) == 0 or not self.app.userHandler.validarUsuario(input)):
            self._label_usuario_verificado.config(text="✖", fg="#880808") #Despues usar palette o algo
            self.validaciones["Usuario"] = False
        else:
            self._label_usuario_verificado.config(text="✔", fg="#228B22")
            self.validaciones["Usuario"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputPassword1(self, input: str) -> bool:
        
        if(len(input) == 0):
            self._label_password1_verificado.config(text="✖", fg="#880808") #Despues usar palette o algo
            self.validaciones["Password1"] = False
        else:
            self._label_password1_verificado.config(text="✔", fg="#228B22")
            self.validaciones["Password1"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputPassword2(self, input: str) -> bool:
        
        if(input != self._entry_password_1.get()):
            self._label_password2_verificado.config(text="✖", fg="#880808") #Despues usar palette o algo
            self.validaciones["Password2"] = False
        else:
            self._label_password2_verificado.config(text="✔", fg="#228B22")
            self.validaciones["Password2"] = True
        
        if(not input.isalnum() and len(input) > 0):
            print(input)
            return False
        
        return True
    
    def __validarInputEmail(self, input: str) -> bool:
        
        if(not re.match(r"[^@]+@[^@]+\.[^@]+", input) or not self.app.userHandler.validarEmail(input)):
            self._label_email_verificado.config(text="✖", fg="#880808") #Despues usar palette o algo
            self.validaciones["Email"] = False
        else:
            self._label_email_verificado.config(text="✔", fg="#228B22")
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
    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master,app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

    def reset(self) -> None:
        self._profile_text_var.set("Bienvenido " + self.app.userHandler.userIngresado + "!")
        pass

    def __logOff(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.LOGIN)

    def __newSimFrame(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.NEW_SIMULATION)

    def __allSimFrame(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.ALL_SIMULATIONS)

    def __loadCallbacks(self) -> None:
        pass

    def __loadWidgets(self) -> None:
        
        self._menuFrame = tk.Frame(self, background="#FFFFFF")
        self._menuFrame.grid(row=2, rowspan=3, column=2)
        self._menuFrame.grid_rowconfigure(4)
        self._menuFrame.grid_columnconfigure(1)

        self._newSimulation_button = tk.Button(self._menuFrame, width=30, height=1, text="Nueva Simulacion", font= super().h3, command=self.__newSimFrame)
        self._newSimulation_button.grid(row=1, column=1, pady=5, padx=5)

        self._listaSimulation_button = tk.Button(self._menuFrame, width=30, height=1, text="Ver Simulaciones", font= super().h3, command=self.__allSimFrame)
        self._listaSimulation_button.grid(row=2, column=1, pady=5, padx=5)

        self._simulator_grafico = plt.subplots()[0]
        self._simulator_canvas = FigureCanvasTkAgg(self._simulator_grafico,  self._menuFrame)
        self._simulator_canvas.get_tk_widget().grid(row=3, column=1, padx=5, pady=5)
        
        self._profileFrame = tk.Frame(self, background="#FFFFFF", width= 50, height=10)
        self._profileFrame.grid(row=1, column=1, sticky=tk.NW, padx=5, pady=5, ipadx=5, ipady=5)
        self._profileFrame.grid_rowconfigure(1)
        self._profileFrame.grid_columnconfigure(2)

        self._profile_text_var = tk.StringVar()
        self._profile_text_var.set("Bienvenido Username!")
        
        self._profileLabel = tk.Label(self._profileFrame, textvariable= self._profile_text_var, font=super().h2, background="#FFFFFF")
        self._profileLabel.grid(row=1, column=1)

        self._profileConfig_button = tk.Button(self._profileFrame, text="⚙")
        self._profileConfig_button.grid(row=1, column=2)

        self._logOff_button = tk.Button(self, width=25, height=2, text= "Log off", font= super().h2, command= self.__logOff)
        self._logOff_button.grid(row=1,column=3, padx=10, pady=10)
    pass

# Esta clase representa el frame de crear una nueva simulacion para el usuario
class CrearSimulacionFrame(AppWindow):

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()


        self.mesaCounter = 0
        self.mesas = []
        self.mesas_displayed = []

    def reset(self) -> None:
        pass

    def __validarInputNumerico(self, input: str) -> bool:

        if(not input.isnumeric() and len(input) > 0):
            return False
        
        return True
        

    def __loadCallbacks(self) -> None:
        self._validarInputNumericoCallback = self.register(self.__validarInputNumerico)
        
    def __iniciarSimulacion(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.AWAITING_SIMULATION)
        pass

    def __volverMenuPrincipal(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    def __borrar_mesa(self, master: tk.Frame) -> None:
        index = self.mesas.index(master)
        self.mesas.pop(index)
        master.destroy()

        for i in range(len(self.mesas_displayed)):
            if(i > index):
                self._mesa_canvas.move(self.mesas_displayed[i],0, -42)

        self.mesas_displayed.pop(index)

        if(40*len(self.mesas) > self._mesa_canvas.winfo_height()):
            self._mesa_canvas.config(scrollregion=(0,0,0,42*(len(self.mesas))))
            

    def __agregar_mesa(self) -> None:

        asientos = self._mesa_entry.get()
        if(asientos == ""):
            return None

        mesa = tk.Frame(self)
        mesa.columnconfigure(3)
        mesa.rowconfigure(1)

        width = self._mesa_canvas.winfo_width()
        display = self._mesa_canvas.create_window(width/2,42*len(self.mesas), anchor=tk.N, window=mesa)

        mesa_label = tk.Label(mesa, width=10,text="Mesa " + str(self.mesaCounter + 1), font= super().h3)
        mesa_label.grid(row=1, column=1, padx=5, pady=5)

        cantidad_label = tk.Label(mesa, width=10, text= str(asientos) + " asientos", font= super().h3)
        cantidad_label.grid(row=1, column=2, padx=5, pady=5)

        self._mesa_entry.delete(0, tk.END)

        borrar_button = tk.Button(mesa, width=10,text="Borrar", font=super().h3, command= lambda: self.__borrar_mesa(borrar_button.master))
        borrar_button.grid(row=1, column=3, padx=5, pady=5)

        if(40*len(self.mesas) > self._mesa_canvas.winfo_height()):
            self._mesa_canvas.config(scrollregion=(0,0,0,42*(len(self.mesas)+1)))

        self.mesas.append(mesa)
        self.mesas_displayed.append(display)
        self.mesaCounter += 1
        
    def __loadWidgets(self) -> None:

        self._main_frame = tk.Frame(self)
        self._main_frame.grid_rowconfigure(11)
        self._main_frame.grid_columnconfigure(4)
        self._main_frame.grid(row=2,column=2)
        
        self._titulo_label = tk.Label(self._main_frame, text="Nueva Simulación", font=super().h1)
        self._titulo_label.grid(row=1,column=1,columnspan=3)

        self._tiempo_sim_label = tk.Label(self._main_frame, text="Tiempo de Simulación (en segundos): ", font=super().h3)
        self._tiempo_sim_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self._tiempo_sim_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._tiempo_sim_entry.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)

        self._tiempo_tick_label = tk.Label(self._main_frame, text="Tiempo entre Tick (en segundos): ", font=super().h3)
        self._tiempo_tick_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self._tiempo_tick_entry = tk.Entry(self._main_frame, width=40, font=super().h2)
        self._tiempo_tick_entry.grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)

        self._cant_meseros_label = tk.Label(self._main_frame, text="Cantidad de Meseros: ", font=super().h3)
        self._cant_meseros_label.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_meseros_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._cant_meseros_entry.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

        self._cant_cocineros_label = tk.Label(self._main_frame, text="Cantidad de Cocineros: ", font=super().h3)
        self._cant_cocineros_label.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_cocineros_entry = tk.Entry(self._main_frame, width=40, font=super().h2)
        self._cant_cocineros_entry.grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)

        self._cant_clientes_label = tk.Label(self._main_frame, text="Cantidad de Grupo de Clientes por Hora: ", font=super().h3)
        self._cant_clientes_label.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_clientes_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._cant_clientes_entry.grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)

        self._mesa_label = tk.Label(self._main_frame, text="Cantidad de Asientos en Mesa: ", font=super().h3)
        self._mesa_label.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

        self._mesa_frame = tk.Frame(self._main_frame)
        self._mesa_frame.grid(row=7,column=2, sticky= tk.W)
        self._mesa_frame.grid_columnconfigure(2)
        self._mesa_frame.grid_rowconfigure(1)

        self._mesa_entry = tk.Entry(self._mesa_frame, width=5, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._mesa_entry.grid(row=1, column=1, padx=5, pady=5)

        self._mesa_button = tk.Button(self._mesa_frame, width=15, text="Agregar Mesa", font=super().h3, command=self.__agregar_mesa)
        self._mesa_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        self._mesa_display_frame = tk.Frame(self._main_frame)
        self._mesa_display_frame.grid(row=1, column=4, rowspan=5)

        self._mesa_canvas = tk.Canvas(self._mesa_display_frame, height=128)

        self._mesa_canvas_vbar = tk.Scrollbar(self._mesa_display_frame, orient=tk.VERTICAL, command=self._mesa_canvas.yview)
        self._mesa_canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._mesa_canvas.config(yscrollcommand=self._mesa_canvas_vbar.set)
        self._mesa_canvas.pack(side=tk.LEFT, expand=True, fill= tk.BOTH)

        self._plato_label = tk.Label(self._main_frame, text="Ingresar Nombre de Plato y Tiempo Promedio de Coccion:", font=super().h3)
        self._plato_label.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

        self._plato_frame = tk.Frame(self._main_frame)
        self._plato_frame.grid(row=8,column=2, sticky= tk.W)
        self._plato_frame.grid_columnconfigure(3)
        self._plato_frame.grid_rowconfigure(1)

        self._plato_entry_nombre = tk.Entry(self._plato_frame, width=20, font=super().h2)
        self._plato_entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        self._plato_entry_tiempo = tk.Entry(self._plato_frame, width=5, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._plato_entry_tiempo.grid(row=1, column=2, padx=5, pady=5)

        self._plato_button = tk.Button(self._plato_frame, width=15, text="Agregar Plato", font=super().h3, command=self.__agregar_mesa)
        self._plato_button.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

        self._plato_display_frame = tk.Frame(self._main_frame)
        self._plato_display_frame.grid(row=5, column=4, rowspan=5)

        self._plato_canvas = tk.Canvas(self._plato_display_frame, height=128)

        self._plato_canvas_vbar = tk.Scrollbar(self._plato_display_frame, orient=tk.VERTICAL, command=self._plato_canvas.yview)
        self._plato_canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._plato_canvas.config(yscrollcommand=self._plato_canvas_vbar.set)
        self._plato_canvas.pack(side=tk.LEFT, expand=True, fill= tk.BOTH)

        self._simular_button = tk.Button(self, text="Simular", command = self.__iniciarSimulacion)
        self._simular_button.grid(row=3, column=2, sticky=tk.S, padx=5, pady=5)

        self._go_back_button = tk.Button(self, text="Volver al menu principal", command = self.__volverMenuPrincipal)
        self._go_back_button.grid(row=1, column=3, sticky= tk.NE, padx=5, pady=5)
        pass


# Esta clase representa el frame de espera de la simulacion
class EsperaSimulacionFrame(AppWindow):
    pass

# Esta clase representa el frame de resultados de la simulacion
class ResultadoSimulacionFrame(AppWindow):

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

    def reset(self) -> None:
        pass

    def __loadCallbacks(self) -> None:
        pass

    def go_back(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    def __loadWidgets(self) -> None:
        _go_back_button = tk.Button(self, text="Go Back", command = self.go_back)
        _go_back_button.pack()
        pass

class TodasSimulacionesFrame(AppWindow):

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

    def reset(self) -> None:
        pass

    def __loadCallbacks(self) -> None:
        pass

    def go_back(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    def __loadWidgets(self) -> None:
        _go_back_button = tk.Button(self, text="Go Back", command = self.go_back)
        _go_back_button.pack()
        pass
