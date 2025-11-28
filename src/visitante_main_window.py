# visitante_main_window.py
import session
import tkinter as tk
from tkinter import messagebox, simpledialog
from obras import Obras
from usuario import Visitante


def abrir_ventana_visitante():
    ventana = tk.Toplevel()
    ventana.title("Ventana Principal - Visitante")
    ventana.geometry("700x520")

    label_bienvenida = tk.Label(
        ventana,
        text=f"Bienvenido, {session.usuario_nombre}!",
        font=("Arial", 16)
    )
    label_bienvenida.pack(pady=10)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_favoritos = tk.Button(frame_botones, text="Mostrar favoritos")
    btn_favoritos.grid(row=0, column=0, padx=5)

    btn_crear_sala = tk.Button(frame_botones, text="Crear sala")
    btn_crear_sala.grid(row=0, column=1, padx=5)

    btn_entrar_sala = tk.Button(frame_botones, text="Entrar a sala")
    btn_entrar_sala.grid(row=0, column=2, padx=5)

    lista_obras = tk.Listbox(ventana, width=100, height=15)
    lista_obras.pack(pady=10)

    obras_cargadas = []
    mostrando_favoritos = False 
    #cargar obras
    def cargar_obras():
        nonlocal obras_cargadas
        try:
            obras_cargadas = Obras.show_obras_visitante()
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar las obras.")
            return

        lista_obras.delete(0, tk.END)

        if not obras_cargadas:
            lista_obras.insert(tk.END, "No hay obras disponibles.")
            return

        for i, obra in enumerate(obras_cargadas):
            texto = f"{i+1}. {obra['titulo']}  | Autor ID: {obra['autor_id']}"
            lista_obras.insert(tk.END, texto)

    #cargar favs
    def cargar_favoritos():
        nonlocal obras_cargadas
        try:
            obras_cargadas = Visitante.listar_favoritos(session.usuario_id)
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar los favoritos.")
            return

        lista_obras.delete(0, tk.END)

        if not obras_cargadas:
            lista_obras.insert(tk.END, "No tienes obras favoritas.")
            return

        for i, obra in enumerate(obras_cargadas):
            texto = f"{i+1}. {obra['titulo']}  | Autor ID: {obra['autor_id']}"
            lista_obras.insert(tk.END, texto)

    #mostrar favs
    def toggle_favoritos():
        nonlocal mostrando_favoritos

        if not mostrando_favoritos:
            cargar_favoritos()
            btn_favoritos.config(text="Ver obras")
            mostrando_favoritos = True
        else:
            cargar_obras()
            btn_favoritos.config(text="Mostrar favoritos")
            mostrando_favoritos = False

    btn_favoritos.config(command=toggle_favoritos)

    #abrir obra
    def abrir_detalles(event):
        seleccion = lista_obras.curselection()
        if not seleccion:
            return

        index = seleccion[0]
        obra = obras_cargadas[index]

        import visitante_art
        visitante_art.abrir_visitante_art(obra)

    lista_obras.bind("<Double-1>", abrir_detalles)

    #crear sala
    def crear_sala():
        import visitante_crear_sala
        visitante_crear_sala.abrir_crear_Sala()

    btn_crear_sala.config(command=crear_sala)

    #salas
    def entrar_sala():
        sala_id = simpledialog.askinteger("Entrar a sala", "Ingresa el ID de la sala:")
        if sala_id is None:
            return

        codigo = simpledialog.askstring("Código de acceso", "Ingresa el código (si es privada):")
        if codigo is None:
            codigo = ""

        #intentar entrar
        from salas import Salas
        sala = Salas.entrar_sala_id(sala_id, codigo)

        if sala is None:
            messagebox.showerror("Error", "No se pudo entrar a la sala. Código o ID incorrecto.")
            return

        import visitante_salas
        visitante_salas.abrir_Salas(sala)

    btn_entrar_sala.config(command=entrar_sala)

    cargar_obras()
