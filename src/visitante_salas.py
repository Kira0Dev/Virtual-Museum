#visitante_salas.py
import session
import tkinter as tk
from tkinter import messagebox, simpledialog
from obras import Obras
from usuario import Visitante
from salas import Salas

def abrir_Salas(sala):
    ventana = tk.Toplevel()
    ventana.title("Sala: " + sala.nombre)
    ventana.geometry("700x520")

    label_bienvenida = tk.Label(
        ventana,
        text=f"Sala: {sala.nombre}",
        font=("Arial", 16)
    )
    label_bienvenida.pack(pady=10)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    lista_obras = tk.Listbox(ventana, width=100, height=15)
    lista_obras.pack(pady=10)

    obras_cargadas = []

    def cargar_obras():
        nonlocal obras_cargadas
        lista_obras.delete(0, tk.END)

        try:
            ids_obras = Salas.show_obras_en_sala(sala.id)
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar las obras.")
            return

        if not ids_obras:
            lista_obras.insert(tk.END, "La sala no tiene obras aún.")
            return

        obras_cargadas = [] 

        #recorrer cada ID y traer info completa
        for obra_id in ids_obras:
            try:
                obra = Obras.show_obra_visitante_por_id(obra_id)
                obras_cargadas.append(obra)
            except Exception:
                #continue 
                messagebox.showerror("Error", "No se pudo cargar obra")

        if not obras_cargadas:
            lista_obras.insert(tk.END, "No se pudieron cargar detalles de las obras.")
            return

        for i, obra in enumerate(obras_cargadas):
            texto = f"{i+1}. {obra['titulo']}  | Autor ID: {obra['autor_id']} | Descripción: {obra['descripcion']} | Etiquetas: {obra['tags']}"
            lista_obras.insert(tk.END, texto)



    cargar_obras()

