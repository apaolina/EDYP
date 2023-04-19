from SimClasses import Persona
from SimClasses import Mesa

mesa = Mesa.Mesa(4)
cliente1 = Persona.Cliente("Joaquin Ramos")
cliente2 = Persona.Cliente("Lionel Messi")

grupo = Persona.GrupoClientes(cliente1,cliente2)

mesa.ocupar(grupo)