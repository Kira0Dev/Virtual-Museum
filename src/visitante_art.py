# visitante_art.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import session

from obras import Obras
from usuario import Visitante


def abrir_visitante_art(obra_dict):
    """
    Recibe un diccionario con datos de la obra desde la ventana anterior.
    Luego pide la obra completa usando obtener_obra_por_id.
    """
    titulo = obra_dict["titulo"]

    #obtener la obra completa desde la BD
    try:
        obra = Obras.obtener_obra_por_titulo(titulo)
        obra_id = obra.id
    except Exception:
        messagebox.showerror("Error", "No se pudo cargar la obra.")
        return

    #crear ventana
    ventana = tk.Toplevel()
    ventana.title(obra.titulo)
    ventana.geometry("600x400")

    #título
    lbl_titulo = tk.Label(ventana, text=obra.titulo, font=("Arial", 18, "bold"))
    lbl_titulo.pack(pady=10)

    #archivo URL
    lbl_archivo = tk.Label(ventana, text=f"Archivo: {obra.archivo_url}", font=("Arial", 12))
    lbl_archivo.pack(pady=5)

    #descripción
    lbl_desc = tk.Label(ventana, text=f"Descripción:\n{obra.descripcion}", font=("Arial", 12), justify="left")
    lbl_desc.pack(pady=10)

    #tags
    tags_texto = ", ".join(obra.tags) if obra.tags else "Sin tags"
    lbl_tags = tk.Label(ventana, text=f"Tags: {tags_texto}", font=("Arial", 12))
    lbl_tags.pack(pady=5)

    frame_btn = tk.Frame(ventana)
    frame_btn.pack(pady=15)

    #visitante = Visitante(session.usuario_id, session.usuario_nombre)

    #botón Like
    def agregar_like():
        try:
            Visitante.agregar_favorito(session.usuario_id, obra_id)
            messagebox.showinfo("Favorito", "Has dado like a esta obra.")
        except Exception:
            messagebox.showerror("Error", "No se pudo agregar a favoritos.")

    btn_like = tk.Button(frame_btn, text="Like", width=12, command=agregar_like)
    btn_like.grid(row=0, column=0, padx=10)

    #botón Quitar Like
    def quitar_like():
        try:
            Visitante.eliminar_favorito(session.usuario_id, obra_id)
            messagebox.showinfo("Favorito", "Se removió tu like.")
        except Exception:
            messagebox.showerror("Error", "No se pudo quitar de favoritos.")

    btn_unlike = tk.Button(frame_btn, text="Quitar Like", width=12, command=quitar_like)
    btn_unlike.grid(row=0, column=1, padx=10)

    #botón Comentar
    def comentar():
        texto = simpledialog.askstring("Comentario", "Escribe tu comentario:")
        if not texto:
            return

        try:
            Visitante.agregar_comentario(session.usuario_id, obra_id, texto)
            messagebox.showinfo("Comentario", "Comentario enviado.")
        except Exception:
            messagebox.showerror("Error", "No se pudo agregar el comentario.")

    btn_comentar = tk.Button(frame_btn, text="Comentar", width=12, command=comentar)
    btn_comentar.grid(row=1, column=0, pady=10)

    #botón Reportar
    def reportar():
        motivo = simpledialog.askstring("Reporte", "Motivo del reporte:")
        if not motivo:
            return

        try:
            Visitante.crear_reporte(session.usuario_id, obra_id, motivo)
            messagebox.showinfo("Reporte", "Reporte enviado.")
        except Exception:
            messagebox.showerror("Error", "No se pudo enviar el reporte.")

    btn_reportar = tk.Button(frame_btn, text="Reportar", width=12, command=reportar)
    btn_reportar.grid(row=1, column=1, pady=10)

    btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(pady=20)
