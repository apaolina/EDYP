from SimClasses import Persona as p
from SimClasses import instance


cliente1 = p.Cliente("Joaquin Ramos")
cliente2 = p.Cliente("Lionel Messi")
cliente3 = p.Cliente("Julian Alvarez")

grupo = p.GrupoClientes(cliente1,cliente2,cliente3)