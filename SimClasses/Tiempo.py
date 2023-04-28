import numpy as np

# Se le debe ingresar un valor de segundos 
def tiempo_aleatorio(lamda: int) -> int:
    return np.random.poisson(lamda, 1)
