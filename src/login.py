#login.py
from usuario import Usuario, hash_password
import session
from usuario import Visitante
from usuario import Artista
from usuario import Moderador
from obras import Obras
from reportes import Reportes
from salas import Salas
from comentarios import Comentarios

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import sys
import os

def iniciar_sesion():
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not email or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    password_hashed = hash_password(password)


    if Usuario.autenticar(email, password_hashed):
        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        session.usuario_id = Usuario.obtener_id_por_email(email)
        session.usuario_nombre = Usuario.obtener_nombre_por_id(session.usuario_id)
        session.usuario_email = email
        session.usuario_rol = Usuario.obtener_rol_por_email(email)
        # Aquí llevarías a la ventana principal de la aplicación
    else:
        messagebox.showerror("Error", "Email o contraseña incorrectos")


def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()

#ventana
root = tk.Tk()
root.title("Iniciar sesión")
root.geometry("350x300")

#widgets
label_email = tk.Label(root, text="Email:")
label_email.pack(pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack()

btn_iniciar = tk.Button(root, text="Iniciar sesión", font=("Arial", 12), command=iniciar_sesion)
btn_iniciar.pack(pady=20)

btn_regresar = tk.Button(root, text="Regresar", font=("Arial", 10), command=lambda: ejecutar_archivo("execute.py"))
btn_regresar.pack(pady=10)

root.mainloop()