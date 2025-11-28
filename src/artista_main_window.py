#artista_main_window.py


import tkinter as tk
import subprocess
import sys
import os

def ejecutar_archivo(nombre_archivo):
    ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
    subprocess.Popen([sys.executable, ruta])
    root.destroy()


#ventana principal artista
root = tk.Tk()
root.title("Ventana Principal - Artista")
root.geometry("600x400")

#widgets
label_bienvenida = tk.Label(root, text="Bienvenido, Artista!", font=("Arial", 16))
label_bienvenida.pack(pady=20)

btn_actualizar_biografia = tk.Button(root, text="Actualizar Biografía", font=("Arial", 12), command=ejecutar_archivo("artista_biografia.py"))
btn_actualizar_biografia.pack(pady=10)

btn_ver_portafolio = tk.Button(root, text="Ver Portafolio", font=("Arial", 12), command=ejecutar_archivo("artista_portafolio.py"))
btn_ver_portafolio.pack(pady=10)

btn_subir_obra = tk.Button(root, text="Crear Nueva Obra", font=("Arial", 12), command=ejecutar_archivo("artista_subir_obra.py"))
btn_subir_obra.pack(pady=10)

btn_borrar_obra = tk.Button(root, text="Borrar Obra", font=("Arial", 12), command=ejecutar_archivo("artista_borrar_obra.py"))
btn_borrar_obra.pack(pady=10)

root.mainloop()




