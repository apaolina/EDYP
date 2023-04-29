# from SimClasses import Persona
# from SimClasses import Mesa

# mesa = Mesa.Mesa(4)
# cliente1 = Persona.Cliente("Joaquin Ramos")
# cliente2 = Persona.Cliente("Lionel Messi")

# grupo = Persona.GrupoClientes(cliente1)

# grupo.addCliente(cliente2)

# mesa.ocupar(grupo)

# print(mesa.getEstado)

import hashlib
import os

def hash_password(password):
    # Generar una sal aleatoria
    salt = os.urandom(16)
    # Aplicar el hash a la contraseña junto con la sal
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    # Devolver la sal y el hash de la contraseña
    return salt + hashed_password

def verify_password(stored_password, entered_password):
    # Obtener la sal y el hash de la contraseña almacenada
    salt = stored_password[:16]
    stored_hash = stored_password[16:]
    # Aplicar el hash a la contraseña ingresada junto con la sal
    entered_hash = hashlib.pbkdf2_hmac("sha256", entered_password.encode(), salt, 100000)
    # Comparar los hashes
    return entered_hash == stored_hash

# Ejemplo de cómo verificar si la contraseña ingresada es correcta

# Obtener la contraseña almacenada del usuario (que incluye la sal y el hash de la contraseña)
stored_password = hash_password("mypassword123")
print(stored_password)
stored_password1 = hash_password("mypassword123")
print(stored_password1)
# Obtener la contraseña ingresada por el usuario
entered_password = "mypassword123"
# Verificar si la contraseña ingresada es correcta
if verify_password(stored_password, entered_password):
    print("Contraseña correcta!")
else:
    print("Contraseña incorrecta.")
