from SimClasses import instance
import time
from GUI import *
from tkinter import *
from tkinter import messagebox

Button(root, text="Iniciar sesión", command=login).grid(row=3)

Button(root, text="Crear cuenta", command=create_account).grid(row=4)

root.mainloop()



#instance.mesaManager.crearMesa(2)
#instance.mesaManager.crearMesa(2)

#start = time.time()
#instance.simular(tiempoSimulacion = (60*60*8), tiempoPorTick = 1)
#end = time.time()

"""

Lo que esta pasando en la funcion de arriba es lo siguiente:

La instancia pide 2 argumentos, cuanto tardaria la simulacion y el tiempo entre cada "chequeo" del sistema en la simulacion

Esto lo que va a hacer (por ahora!!!) es llamar a un evento llamado on_tick que basicamente es una funcion que llama a otras funciones sin que ellas tengan que saber porque

Entonces, cada vez que se llama on_tick, el sistema (por ahora!!!) esta diseñado para que utilice el objeto FabricaClientes, especificamente su funcion de fabricarCliente

Por ahora aun no implemente el asunto de varianza de cuando llegan los clientes, pero sepan que deje la infraestructura ahi para implementarlo en FabricClientes.py

En fin, cuando se crea un nuevo grupo y automaticamente se une a la fila de clientes esperando para una mesa

Todo los cambios que pasaron en este push son basicamente la IMPLEMENTACION DEL TIEMPO A NUESTRA SIMULACION!!

"""


#print(f"grupos: {instance.grupoManager.getCantidadGrupoClientes()}")
#print(f"en cola: {instance.grupoManager.colaSentar.totalnodos}")
#print(instance.mesaManager.verEstadoMesas())
#print(end-start)
