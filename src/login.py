# login.py
from usuario import Usuario, hash_password
import session
import subprocess

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import sys

def iniciar_sesion():
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not email or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    password_hashed = hash_password(password)

    if Usuario.autenticar(email, password_hashed):
        session.usuario_id = Usuario.obtener_id_por_email(email)
        session.usuario_nombre = Usuario.obtener_nombre_por_id(session.usuario_id)
        session.usuario_email = email
        session.usuario_rol = Usuario.obtener_rol_por_email(email)

        messagebox.showinfo("Éxito", "Inicio de sesión exitoso")

        # Redirige según rol
        if session.usuario_rol == "ARTISTA":
            ejecutar_archivo("artista_main_window.py")
        elif session.usuario_rol == "MODERADOR":
            ejecutar_archivo("moderador_main_window.py")
        else:
            ejecutar_archivo("visitante_main_window.py")
    else:
        messagebox.showerror("Error", "Email o contraseña incorrectos")


def ejecutar_archivo(nombre_archivo):
    root.destroy()

    #abrir la ventana correta de forma directa (top-level) y sin perder session
    if nombre_archivo == "artista_main_window.py":
        import artista_main_window
        artista_main_window.abrir_ventana_artista()

    elif nombre_archivo == "moderador_main_window.py":
        import moderador_main_window
        moderador_main_window.abrir_ventana_moderador()

    elif nombre_archivo == "visitante_main_window.py":
        import visitante_main_window
        visitante_main_window.abrir_ventana_visitante()


def volver(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()


# Ventana
root = tk.Tk()
root.title("Iniciar sesión")
root.geometry("350x300")

# Widgets
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

btn_regresar = tk.Button(root, text="Regresar", font=("Arial", 10), command=lambda: volver("execute.py"))
btn_regresar.pack(pady=10)

root.mainloop()
