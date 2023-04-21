from SimClasses import Persona as p
from SimClasses import instance


cliente1 = p.Cliente("Joaquin Ramos")
cliente2 = p.Cliente("Lionel Messi")
cliente3 = p.Cliente("Julian Alvarez")

grupo = p.GrupoClientes(cliente1,cliente2,cliente3)

instance.mesaInterface.crearMesa(1) # Se le esta asignando a esta mesa un grupo de clientes de 3 cuando es mejor asignarle la mesa de 10 de capacidad.
instance.mesaInterface.crearMesa(10)

grupo.requestMesa()

print(instance.mesaInterface.mesas[0].getEstado())




