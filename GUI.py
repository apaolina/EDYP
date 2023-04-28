from tkinter import *
from tkinter import messagebox
import hashlib as hash
from Hasheo import *

root = Tk()
root.title("Inicio de sesión")

Label(root, text="Usuario").grid(row=0)
Label(root, text="Contraseña").grid(row=1)

username_entry = Entry(root)
password_entry = Entry(root, show="*")

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

   


def create_account():
    create_window = Toplevel(root)
    create_window.title("Crear cuenta")

    Label(create_window, text="Nombre de usuario").grid(row=0)
    Label(create_window, text="Contraseña").grid(row=1)

    new_username_entry = Entry(create_window)
    new_password_entry = Entry(create_window, show="*")

    
    new_username_entry.grid(row=0, column=1)
    new_password_entry.grid(row=1, column=1)

    
    def submit():
        new_username = new_username_entry.get()
        new_password = hash_password(new_password_entry.get())
        with open("users.txt", "a") as file:
            file.write(f"{new_username},{new_password}\n")
        messagebox.showinfo("Cuenta creada", "La cuenta ha sido creada con éxito")
        create_window.destroy()
    Button(create_window, text="Crear cuenta", command=submit).grid(row=3)
    
def login():
    username = username_entry.get()
    password = password_entry.get().encode()
    stored_password = None
    stored_username = None
    with open("users.txt", "r") as file:
        for line in file.readlines():
            try:
                stored_username, stored_password = line.strip().split(",")
            except  ValueError:
                print("Error en el archivo de usuarios")
            if (username) == stored_username and verify_password(stored_password, password) == stored_password:
                messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido!")
                root.destroy()
                return
    messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")

