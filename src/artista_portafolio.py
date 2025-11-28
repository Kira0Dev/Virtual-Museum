# artista_portafolio
import tkinter as tk
from tkinter import messagebox
from usuario import Artista
import session


def abrir_ventana_portafolio():
    ventana = tk.Toplevel()
    ventana.title("Mi Portafolio")
    ventana.geometry("500x300")

    listbox = tk.Listbox(ventana, width=60, height=15)
    listbox.pack(pady=10)

    def mostrar_portafolio():
        try:
            
            obras = Artista.ver_portafolio(session.usuario_id)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el portafolio:\n{e}")
            return

        listbox.delete(0, tk.END)

        if not obras:
            listbox.insert(tk.END, "No tienes obras registradas.")
            return

        for obra in obras:
            obra_id, titulo, descripcion = obra
            listbox.insert(tk.END, f"{obra_id} - {titulo} | {descripcion}")

  
    btn_cargar = tk.Button(ventana, text="Cargar Portafolio", command=mostrar_portafolio)
    btn_cargar.pack(pady=5)

    btn_regresar = tk.Button(ventana, text="Regresar", font=("Arial", 10), command=ventana.destroy)
    btn_regresar.pack(pady=10)
