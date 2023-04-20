from SimClasses import Persona as p
from SimClasses import instance


cliente1 = p.Cliente("Joaquin Ramos")
cliente2 = p.Cliente("Lionel Messi")
cliente3 = p.Cliente("Julian Alvarez")

grupo = p.GrupoClientes(cliente1,cliente2,cliente3, cliente1) # Hay dos clientes en un grupo de clientes que son el mismo. Esto es para probar que no se repitan los clientes en el grupo
rupo = p.GrupoClientes(cliente1,cliente2,cliente3, cliente1)
upo = p.GrupoClientes(cliente1)
po = p.GrupoClientes(cliente1,cliente2,cliente3, cliente1)
o = p.GrupoClientes(cliente1,cliente2,cliente3, cliente1)

lista = [grupo, rupo, upo, po, o]
instance.mesaController.crearMesa(1) # Se le esta asignando a esta mesa un grupo de clientes de 3 cuando es mejor asignarle la mesa de 10 de capacidad.
instance.mesaController.crearMesa(10)

for grupo in lista:
    grupo.requestMesa()

print(instance.mesaController.mesas[1].getEstado())
print(instance.grupoController.colaSentar.totalnodos)



