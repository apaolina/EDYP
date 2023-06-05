import tkinter as tk

# Este es nuestra clase generica de applicacion, cualquier cambio que queremos que ocurra en toda la applicacion se aplica aca.
class AppWindow(tk.Tk):

    h1 = ("Times New Roman", 50)
    h2 = ("Times New Roman", 20)
    h3 = ("Times New Roman", 10)
    h4 = ("Times New Roman", 9)

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # configurar root window
        self.title('My Awesome App')
        self.state("zoomed")
        self.minsize(width=500, height= 300)


# Esta clase representa el login de la aplicacion principal
class Login(AppWindow):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        # Lista de Variables a Utilizar
        self.textoUsuario:str
        self.textoPassword:str

        # Lista de Widgets presentes
        self._titulo = tk.Label(self, text= "Login", font=super().h1)
        self._titulo.pack(pady= 10)

        self._label_usuario = tk.Label(self, text= "Ingresar Usuario", font= super().h2)
        self._label_usuario.pack()

        self._entry_usuario = tk.Entry(self, width= 40, font= super().h2)
        self._entry_usuario.pack(padx= 5, pady=5)

        self._label_password = tk.Label(self, text= "Ingresar Contraseña", font= super().h2)
        self._label_password.pack()

        self._entry_password = tk.Entry(self, width=40,show="*", font= super().h2)
        self._entry_password.pack(padx= 5, pady= 5)

        self._request_login_button = tk.Button(self, width=10, height=2, text= "Log In", font= super().h3)
        self._request_login_button.pack(pady=5)

        self._request_registrar_button = tk.Button(self, width=50, height=1, text= "No tienes Usuario? Registrarse aqui", font= super().h4)
        self._request_registrar_button.pack(pady=5, side= "bottom")


class RegistroUsuario(AppWindow):

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)