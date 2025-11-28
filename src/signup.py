#signup.py
from usuario import Usuario, hash_password  # si necesitas el hash
import session

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import os

import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def registrar_usuario():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    rol = combo_rol.get()

    if not nombre or not email or not password or not rol:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    password_hashed = hash_password(password)

    Usuario.crear(nombre, email, password_hashed, rol)
    session.usuario_id = Usuario.obtener_id_por_email(email)
    session.usuario_nombre = nombre
    session.usuario_email = email
    session.usuario_rol = rol
    messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
    if rol == "ARTISTA":
        ejecutar_archivo("artista_crear_biografia.py")


def ejecutar_archivo(nombre_archivo):
    root.destroy()

    if nombre_archivo == "artista_crear_biografia.py":
        import artista_crear_biografia
        artista_crear_biografia.abrir_ventana_biografia()

#ventana
root = tk.Tk()
root.title("Crear cuenta")
root.geometry("400x350")

#widgets
label_nombre = tk.Label(root, text="Nombre:")
label_nombre.pack(pady=5)
entry_nombre = tk.Entry(root, width=30)
entry_nombre.pack()

label_email = tk.Label(root, text="Email:")
label_email.pack(pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack()

label_rol = tk.Label(root, text="Rol:")
label_rol.pack(pady=5)

combo_rol = ttk.Combobox(root, values=["VISITANTE", "ARTISTA", "MODERADOR"], state="readonly", width=27)
combo_rol.pack()
combo_rol.current(0)

btn_registrar = tk.Button(root, text="Registrarse", font=("Arial", 12), command=registrar_usuario)
btn_registrar.pack(pady=20)

btn_regresar = tk.Button(root, text="Regresar", font=("Arial", 10), command=lambda: ejecutar_archivo("execute.py"))
btn_regresar.pack(pady=10)

root.mainloop()
