# Contenedor de informacion basica de un usuario en el log in
class PaqueteUsuario():

    def __init__(self, usuario: str = "", password: str = "") -> None:
        self.usuario = usuario
        self.password = password
        pass

# Contenedor de informacion estilistica de la aplicacion (colores, fuentes)
class Palette():
    pass
