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