import tkinter as tk
from DataClasses import *
from enum import Enum
import sys

sys.path.insert(0,'Database')
from DataBaseManager import DataManager
from typing import Callable
import re
from tkinter import messagebox
sys.path.insert(0,'SimClasses')

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Contiene todos las pestañas posibles. Hard coded, agregar aca y en linea 54 una nueva pestaña si se necesita.
class WindowState(Enum):
    LOGIN = 0,
    REGISTER = 1,
    MAIN_MENU = 2,
    NEW_SIMULATION = 3,
    AWAITING_SIMULATION = 4,
    RESULTS_SIMULATION = 5,
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

        self.tempStorage = ""

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
        for we in (WindowState.LOGIN,WindowState.REGISTER, WindowState.MAIN_MENU, WindowState.NEW_SIMULATION, WindowState.AWAITING_SIMULATION, WindowState.RESULTS_SIMULATION, WindowState.ALL_SIMULATIONS):
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
        self.progreso_sim: int = 0
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
        self.after(50,lambda: self._profile_text_var.set(f"Bienvenido {self.app.userHandler.userIngresado}!"))
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
        
#Se callean mesaManager, empleadoManager y restauranteManager
        
        self.__loadCallbacks()
        self.__loadWidgets()


        self._mesaCounter = 0
        self._mesas: list[tk.Frame] = []
        self._mesas_displayed: list[int] = []
        self._mesas_dict: dict[str,list[str,list]] = {}

        self._platoCounter = 0
        self._platos: list[tk.Frame] = []
        self._platos_displayed: list[int] = []
        self._platos_dict: dict[str,list[str,str]] = {}

    def reset(self) -> None:
        self._nombre_sim_entry.delete(0,tk.END)
        self._tiempo_sim_entry.delete(0,tk.END)
        self._tiempo_tick_entry.delete(0,tk.END)
        self._mesa_entry.delete(0,tk.END)
        self._plato_entry_nombre.delete(0,tk.END)
        self._plato_entry_tiempo.delete(0,tk.END)
        self._cant_meseros_entry.delete(0,tk.END)
        self._cant_clientes_entry.delete(0,tk.END)
        self._cant_cocineros_entry.delete(0,tk.END)
        
        self._mesaCounter = 0
        self._platoCounter = 0
        
        for mesa in self._mesas:
            mesa.destroy()

        self._mesas.clear()
        self._mesas_displayed.clear()
        self._mesas_dict.clear()

        for plato in self._platos:
            plato.destroy()
        
        self._platos.clear()
        self._platos_displayed.clear()
        self._platos_dict.clear()

        pass

    def __loadCallbacks(self) -> None:
        self._validarInputNumericoCallback = self.register(self.__validarInputNumerico)

    # Validadores
    def __validarInputNumerico(self, input: str) -> bool:

        if(not input.isnumeric() and len(input) > 0):
            return False
        
        return True
    
    def __mostrarResultados(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.RESULTS_SIMULATION)

    def __procesarSimulacion(self, result:bool, id: int) -> None:
        if(result):
            self.app.windowHandler.cambiarWindow(WindowState.AWAITING_SIMULATION)

            from RestauranteManager import instance
            instance.simular(self._cant_meseros_entry.get(), self._cant_cocineros_entry.get(),\
                                            self._cant_clientes_entry.get(), self._mesas_dict, self._platos_dict, self._tiempo_sim_entry.get(),\
                                                self._tiempo_tick_entry.get(), self.__mostrarResultados, id)
        else:
            messagebox.showerror("Error", "Hubo un error al procesar la simulacion.")

    # Metodos Privados para cambiar de Window 
    def __iniciarSimulacion(self) -> None:

        if len(self._mesas) == 0 or len(self._platos) == 0:
            messagebox.showerror("Error", "Debe haber minimo 1 plato y 1 mesa para realizar la simulacion")
            return

        self.app.tempStorage = self._nombre_sim_entry.get()

        self.dataManager.cargarSimulacion(self.app.userHandler.userIngresado, self._nombre_sim_entry.get(), self._cant_meseros_entry.get(), self._cant_cocineros_entry.get(),\
                                            self._cant_clientes_entry.get(), self._mesas_dict, self._platos_dict, self._tiempo_sim_entry.get(),\
                                                self._tiempo_tick_entry.get(), self.__procesarSimulacion)
        

    def __volverMenuPrincipal(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    # Metodos privados que manejan informacion expuesta en los Canvas scrolleables
    def __borrar_mesa(self, master: tk.Frame) -> None:
        index = self._mesas.index(master)
        self._mesas.pop(index)
        master.destroy()

        for i in range(len(self._mesas_displayed)):
            if(i > index):
                self._mesa_canvas.move(self._mesas_displayed[i],0, -30)

        self._mesas_dict.pop(self._mesas_displayed.pop(index))

        if(40*len(self._mesas) > self._mesa_canvas.winfo_height()):
            self._mesa_canvas.config(scrollregion=(0,0,0,30*(len(self._mesas))))

    def __borrar_plato(self, master: tk.Frame) -> None:
        index = self._platos.index(master)
        self._platos.pop(index)
        master.destroy()

        for i in range(len(self._platos_displayed)):
            if(i > index):
                self._plato_canvas.move(self._platos_displayed[i],0, -35)

        self._platos_dict.pop(self._platos_displayed.pop(index))

        if(40*len(self._platos) > self._plato_canvas.winfo_height()):
            self._plato_canvas.config(scrollregion=(0,0,0,35*(len(self._platos))))
            
    def __agregar_plato(self) -> None:

        nombre_plato = self._plato_entry_nombre.get()
        tiempo_plato = self._plato_entry_tiempo.get()
        if(nombre_plato == "" or tiempo_plato == ""):
            return None

        plato = tk.Frame(self)
        plato.columnconfigure(4)
        plato.rowconfigure(1)

        width = self._plato_canvas.winfo_width()
        display = self._plato_canvas.create_window(width/2,35*len(self._platos), anchor=tk.N, window=plato)

        plato_label = tk.Label(plato, width=10,text=f"Plato {str(self._platoCounter + 1)}", font= super().h4)
        plato_label.grid(row=1, column=1, padx=5, pady=5)

        nombre_label = tk.Label(plato, width=10, text= nombre_plato, font= super().h4)
        nombre_label.grid(row=1, column=2, padx=5, pady=5)

        tiempo_label = tk.Label(plato, width=10, text= f"{tiempo_plato} segundos", font= super().h4)
        tiempo_label.grid(row=1, column=3, padx=5, pady=5)

        self._plato_entry_nombre.delete(0, tk.END)
        self._plato_entry_tiempo.delete(0, tk.END)

        borrar_button = tk.Button(plato, width=10,text="Borrar", font=super().h4, command= lambda: self.__borrar_plato(borrar_button.master))
        borrar_button.grid(row=1, column=4, padx=5, pady=5)

        if(40*len(self._platos) > self._plato_canvas.winfo_height()):
            self._plato_canvas.config(scrollregion=(0,0,0,35*(len(self._platos)+1)))

        self._platos.append(plato)
        self._platos_displayed.append(display)
        self._platoCounter += 1
        self._platos_dict[display] = [nombre_plato, tiempo_plato]
    
    def __agregar_mesa(self) -> None:

        asientos = self._mesa_entry.get()
        if(asientos == ""):
            return None

        mesa = tk.Frame(self)
        mesa.columnconfigure(3)
        mesa.rowconfigure(1)

        width = self._mesa_canvas.winfo_width()
        display = self._mesa_canvas.create_window(width/2,30*len(self._mesas), anchor=tk.N, window=mesa)

        mesa_label = tk.Label(mesa, width=10,text=f"Mesa {str(self._mesaCounter + 1)}", font= super().h4)
        mesa_label.grid(row=1, column=1, padx=5, pady=5)

        cantidad_label = tk.Label(mesa, width=10, text= f"{str(asientos)} asientos", font= super().h4)
        cantidad_label.grid(row=1, column=2, padx=5, pady=5)

        self._mesa_entry.delete(0, tk.END)

        borrar_button = tk.Button(mesa, width=10,text="Borrar", font=super().h4, command= lambda: self.__borrar_mesa(borrar_button.master))
        borrar_button.grid(row=1, column=3, padx=5, pady=5)

        if(40*len(self._mesas) > self._mesa_canvas.winfo_height()):
            self._mesa_canvas.config(scrollregion=(0,0,0,30*(len(self._mesas)+1)))

        self._mesas.append(mesa)
        self._mesas_displayed.append(display)
        self._mesaCounter += 1
        self._mesas_dict[display] = [f"Mesa {str(self._mesaCounter)}", str(asientos)]
        
    def __loadWidgets(self) -> None:

        self._main_frame = tk.Frame(self)
        self._main_frame.grid_rowconfigure(11)
        self._main_frame.grid_columnconfigure(4)
        self._main_frame.grid(row=2,column=2)
        
        self._titulo_label = tk.Label(self._main_frame, text="Nueva Simulación", font=super().h1)
        self._titulo_label.grid(row=1,column=1,columnspan=3)

        self._nombre_sim_label = tk.Label(self._main_frame, text="Nombre de la Simulación: ", font=super().h3)
        self._nombre_sim_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self._nombre_sim_entry = tk.Entry(self._main_frame, width=40, font=super().h2)
        self._nombre_sim_entry.grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)

        self._tiempo_sim_label = tk.Label(self._main_frame, text="Tiempo de Simulación (en segundos): ", font=super().h3)
        self._tiempo_sim_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self._tiempo_sim_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._tiempo_sim_entry.grid(row=3, column=2, padx=5, pady=5, sticky=tk.E)

        self._tiempo_tick_label = tk.Label(self._main_frame, text="Tiempo entre Tick (en segundos): ", font=super().h3)
        self._tiempo_tick_label.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self._tiempo_tick_entry = tk.Entry(self._main_frame, width=40, font=super().h2)
        self._tiempo_tick_entry.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

        self._cant_meseros_label = tk.Label(self._main_frame, text="Cantidad de Meseros: ", font=super().h3)
        self._cant_meseros_label.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_meseros_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._cant_meseros_entry.grid(row=5, column=2, padx=5, pady=5, sticky=tk.E)
  
        self._cant_cocineros_label = tk.Label(self._main_frame, text="Cantidad de Cocineros: ", font=super().h3)
        self._cant_cocineros_label.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_cocineros_entry = tk.Entry(self._main_frame, width=40, font=super().h2)
        self._cant_cocineros_entry.grid(row=6, column=2, padx=5, pady=5, sticky=tk.E)

        self._cant_clientes_label = tk.Label(self._main_frame, text="Cantidad de Grupo de Clientes por Hora: ", font=super().h3)
        self._cant_clientes_label.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

        self._cant_clientes_entry = tk.Entry(self._main_frame, width=40, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._cant_clientes_entry.grid(row=7, column=2, padx=5, pady=5, sticky=tk.E)

        self._mesa_label = tk.Label(self._main_frame, text="Cantidad de Asientos en Mesa: ", font=super().h3)
        self._mesa_label.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

        self._mesa_frame = tk.Frame(self._main_frame)
        self._mesa_frame.grid(row=8,column=2, sticky= tk.W)
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
        self._plato_label.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

        self._plato_frame = tk.Frame(self._main_frame)
        self._plato_frame.grid(row=9,column=2, sticky= tk.W)
        self._plato_frame.grid_columnconfigure(3)
        self._plato_frame.grid_rowconfigure(1)

        self._plato_entry_nombre = tk.Entry(self._plato_frame, width=20, font=super().h2)
        self._plato_entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        self._plato_entry_tiempo = tk.Entry(self._plato_frame, width=5, font=super().h2, validate= "key", validatecommand=(self._validarInputNumericoCallback, "%P"))
        self._plato_entry_tiempo.grid(row=1, column=2, padx=5, pady=5)

        # Aca cambiar comando para que agregue al canvas correcto.
        self._plato_button = tk.Button(self._plato_frame, width=15, text="Agregar Plato", font=super().h3, command=self.__agregar_plato)
        self._plato_button.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

        self._plato_display_frame = tk.Frame(self._main_frame)
        self._plato_display_frame.grid(row=5, column=4, rowspan=5)

        self._plato_canvas = tk.Canvas(self._plato_display_frame, height=128)

        self._plato_canvas_vbar = tk.Scrollbar(self._plato_display_frame, orient=tk.VERTICAL, command=self._plato_canvas.yview)
        self._plato_canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._plato_canvas.config(yscrollcommand=self._plato_canvas_vbar.set)
        self._plato_canvas.pack(side=tk.LEFT, expand=True, fill= tk.BOTH)

        self._simular_button = tk.Button(self, text="Simular", command = self.__iniciarSimulacion)
        self._simular_button = tk.Button(self, text="Simular", command = self.__iniciarSimulacion)
        self._simular_button.grid(row=3, column=2, sticky=tk.S, padx=5, pady=5)

        self._go_back_button = tk.Button(self, text="Volver al menu principal", command = self.__volverMenuPrincipal)
        self._go_back_button = tk.Button(self, text="Volver al menu principal", command = self.__volverMenuPrincipal)
        self._go_back_button.grid(row=1, column=3, sticky= tk.NE, padx=5, pady=5)
        pass


# Esta clase representa el frame de espera de la simulacion
class EsperaSimulacionFrame(AppWindow):
    
    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

    def reset(self):
        pass

    def __loadCallbacks(self) -> None:
        pass

    def update_percentage(self, percentage: int) -> None:
        self.text.set(f"{percentage}%")
        pass

    def __loadWidgets(self) -> None:
        self.text = tk.StringVar()
        self.text.set("0%")
        self._percentage_label = tk.Label(self, textvariable=self.text, font= super().h1)
        self._percentage_label.grid(row=2,column=2)
        pass
    

# Esta clase representa el frame de resultados de la simulacion
class ResultadoSimulacionFrame(AppWindow):

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

        self._sim = {}
        self._inputs = []
        self._inputs_displayed = []

    def __agregar_input(self, info:str) -> None:

        input = tk.Frame(self)
        input.rowconfigure(1)

        width = self._sim_canvas.winfo_width()
        display = self._sim_canvas.create_window(width/2,45*len(self._inputs), anchor=tk.N, window=input)

        input_label = tk.Label(input, width=40,height=1,text=info, font= super().h4)
        input_label.pack(padx=5, pady=5)

        if(40*len(self._inputs) > self._sim_canvas.winfo_height()):
            self._sim_canvas.config(scrollregion=(0,0,0,45*(len(self._inputs)+1)))

        self._inputs.append(input)
        self._inputs_displayed.append(display)

    def reset(self) -> None:
        self._sim = self.app.userHandler.dataManager.getSimulacionesCompleto(self.app.userHandler.userIngresado, self.app.tempStorage)
        for input in self._inputs:
            input.destroy()

        self._inputs.clear()
        self._inputs_displayed.clear()

        for k in self._sim.keys():
            match k:
                case "cantidad_meseros":
                    self.__agregar_input("Cantidad de Meseros: " + str(self._sim[k]))
                case "cantidad_cocineros":
                    self.__agregar_input("Cantidad de Cocineros: " + str(self._sim[k]))
                case "clientes_por_hora":
                    self.__agregar_input("Cantidad de Clientes por Hora: " + str(self._sim[k]))
                case "lista_mesas":
                    asientos = []
                    for mesa in self._sim[k].values():
                        asientos.append(mesa)
                    
                    self.__agregar_input("Cantidad de mesas: " + str(len(self._sim[k])))
                    self.__agregar_input("Cantidad de asientos c/una: " + str(asientos))
                case "lista_platos":
                    for nombre in self._sim[k].keys():
                        self.__agregar_input("Nombre de Plato: " + nombre)
                        self.__agregar_input("Tiempo de Coccion: " + str(self._sim[k][nombre]))
                case "tiempo_simulado":
                    self.__agregar_input("Tiempo Simulado: " + str(self._sim[k]))
                case "tiempo_por_tick":
                    self.__agregar_input("Tiempo por Tick: " + str(self._sim[k]))
                case "eventos":
                    self.__agregar_input("Cantidad de Eventos: " + str(len(self._sim[k][0])))
                case _:
                    pass


    def __loadCallbacks(self) -> None:
        pass

    def volver_menu_ppal(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    def __loadWidgets(self) -> None:
        
        self._informacion_label = tk.Label(self, text="Se realizó la simulación correctamente, encontrarán los datos generados en el archivo database.json")
        self._informacion_label.grid(row=1,column=2)

        self._sim_display_frame = tk.Frame(self, height= 2*self.winfo_reqheight()/3, width=self.winfo_reqwidth())
        self._sim_display_frame.grid(row=2, column=2)

        self._sim_canvas = tk.Canvas(self._sim_display_frame)

        self._sim_canvas_vbar = tk.Scrollbar(self._sim_display_frame, orient=tk.VERTICAL, command=self._sim_canvas.yview)
        self._sim_canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._sim_canvas.config(yscrollcommand=self._sim_canvas_vbar.set)
        self._sim_canvas.pack(side=tk.LEFT, expand=True, fill= tk.BOTH)

        self._volver_menu_ppal_button = tk.Button(self, text="Volver al Menu Principal", command = self.volver_menu_ppal)
        self._volver_menu_ppal_button.grid(row=3,column=2)
        

class TodasSimulacionesFrame(AppWindow):

    def __init__(self, master: tk.Tk, app: App, *args, **kwargs) -> None:
        super().__init__(master, app, *args, **kwargs)

        self.__loadCallbacks()
        self.__loadWidgets()

        self._simulaciones: list[tk.Frame] = []
        self._sims_displayed: list[int] = []

    def __ver_resultados(self, nombre: str) -> None:
        self.app.tempStorage = nombre
        self.app.windowHandler.cambiarWindow(WindowState.RESULTS_SIMULATION)

    def __agregar_sim(self, nombre:str) -> None:

        simulacion = tk.Frame(self)
        simulacion.columnconfigure(3)
        simulacion.rowconfigure(1)

        width = self._sim_canvas.winfo_width()
        display = self._sim_canvas.create_window(width/2,70*len(self._simulaciones), anchor=tk.N, window=simulacion)

        sim_button = tk.Button(simulacion, width=20,height=1,text=nombre, font= super().h2, command=lambda:self.__ver_resultados(nombre))
        sim_button.pack(padx=5, pady=5)

        if(40*len(self._simulaciones) > self._sim_canvas.winfo_height()):
            self._sim_canvas.config(scrollregion=(0,0,0,70*(len(self._simulaciones)+1)))

        self._simulaciones.append(simulacion)
        self._sims_displayed.append(display)


    def reset(self):

        for sim in self._simulaciones:
            sim.destroy()

        self._simulaciones.clear()
        self._sims_displayed.clear()

        listaSim = self.app.userHandler.dataManager.getSimulaciones(self.app.userHandler.userIngresado)
        for sim in listaSim:
            self.__agregar_sim(sim)

        pass

    def __loadCallbacks(self) -> None:
        pass

    def go_back(self) -> None:
        self.app.windowHandler.cambiarWindow(WindowState.MAIN_MENU)

    def __loadWidgets(self) -> None:

        self._sim_display_frame = tk.Frame(self, height= 2*self.winfo_reqheight()/3, width=self.winfo_reqwidth())
        self._sim_display_frame.grid(row=1, rowspan=2, column=1,columnspan=3)

        self._sim_canvas = tk.Canvas(self._sim_display_frame)

        self._sim_canvas_vbar = tk.Scrollbar(self._sim_display_frame, orient=tk.VERTICAL, command=self._sim_canvas.yview)
        self._sim_canvas_vbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._sim_canvas.config(yscrollcommand=self._sim_canvas_vbar.set)
        self._sim_canvas.pack(side=tk.LEFT, expand=True, fill= tk.BOTH)
        _go_back_button = tk.Button(self, text="Go Back", command = self.go_back)
        _go_back_button.grid(row=3,column=2)
        pass
