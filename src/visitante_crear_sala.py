#visitante_Crear_Sala.py
import session
import tkinter as tk
from tkinter import messagebox, simpledialog
from obras import Obras
from usuario import Visitante
from salas import Salas


def abrir_crear_Sala():
    ventana = tk.Toplevel()
    ventana.title("Crear sala")
    ventana.geometry("500x550")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Crear nueva sala", font=("Arial", 18)).pack(pady=15)

    frame = tk.Frame(ventana)
    frame.pack(pady=10)

    tk.Label(frame, text="Nombre de la sala:").pack(anchor="w")
    entrada_nombre = tk.Entry(frame, width=40)
    entrada_nombre.pack(pady=5)

    tk.Label(frame, text="Descripción:").pack(anchor="w")
    entrada_descripcion = tk.Text(frame, width=35, height=5)
    entrada_descripcion.pack(pady=5)

    tk.Label(frame, text="Privacidad:").pack(anchor="w", pady=5)

    privacidad_var = tk.StringVar(value="PUBLICA")

    rb_publica = tk.Radiobutton(frame, text="PUBLICA", variable=privacidad_var, value="PUBLICA",
                                command=lambda: actualizar_codigo(False))
    rb_privada = tk.Radiobutton(frame, text="PRIVADA", variable=privacidad_var, value="PRIVADA",
                                command=lambda: actualizar_codigo(True))

    rb_publica.pack(anchor="w")
    rb_privada.pack(anchor="w")

    label_codigo = tk.Label(frame, text="Código de acceso:")
    entrada_codigo = tk.Entry(frame, width=20)

    def actualizar_codigo(es_privada):
        if es_privada:
            label_codigo.pack(anchor="w", pady=5)
            entrada_codigo.pack(pady=5)
        else:
            label_codigo.pack_forget()
            entrada_codigo.pack_forget()

    actualizar_codigo(False)

    def crear_sala_action():
        nombre = entrada_nombre.get().strip()
        descripcion = entrada_descripcion.get("1.0", tk.END).strip()
        privacidad = privacidad_var.get()
        codigo = entrada_codigo.get().strip() if privacidad == "PRIVADA" else None

        if not nombre and not descripcion:
            messagebox.showerror("Error", "Debes llenar todos los campos.")
            return

        try:
            nueva_sala = Salas.crear_sala(
                autor_id=session.usuario_id,
                nombre=nombre,
                descripcion=descripcion,
                privacidad=privacidad,
                codigo_acceso=codigo
            )

            messagebox.showinfo("Sala creada", f"Sala creada con ID: {nueva_sala.id}")
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la sala.\n{e}")

    tk.Button(ventana, text="Crear sala", font=("Arial", 14),
              command=crear_sala_action).pack(pady=25)
