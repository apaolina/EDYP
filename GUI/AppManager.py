from Frames import *
# Este es el controllador principal de todo el GUI, entonces esto manejara la logica

class AppManager():

    def __init__(self) -> None:
        self.app = App()

        self.app.mainloop()
        pass


AppManager()
