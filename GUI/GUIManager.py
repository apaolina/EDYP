from Windows import Login, WindowEnum
# Este es el controllador principal de todo el GUI, entonces esto manejara la logica

# Prueba funcion cambiar Window rapido, hay que crear un Objeto General primero.
def callback(nextWindow: WindowEnum):
    print(nextWindow)

instance = Login(callback=callback)

instance.mainloop()
