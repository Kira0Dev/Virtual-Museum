#execute.py
import tkinter as tk
import subprocess
import sys
import os

#función para ejecutar otro archivo python
def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()

#ventana principal
root = tk.Tk()
root.title("Bienvenido")
root.geometry("300x200")

btn_login = tk.Button(root, text="Ya tengo cuenta", font=("Arial", 12), width=20,
                      command=lambda: ejecutar_archivo("login.py"))
btn_login.pack(pady=15)

btn_signup = tk.Button(root, text="Crear cuenta", font=("Arial", 12), width=20,
                       command=lambda: ejecutar_archivo("signup.py"))
btn_signup.pack(pady=15)

root.mainloop()
