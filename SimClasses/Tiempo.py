import numpy as np

# Se le debe ingresar un valor en segundos 
def tiempo_aleatorio(lamda: int) -> int:
    return np.random.poisson(lamda, 1)

def tiempo_aleatorio_normal(mu: int, sigma: int) -> int:
    return np.random.normal(mu, sigma, 1)