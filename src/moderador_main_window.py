# moderador_main_window.py
import tkinter as tk
from tkinter import messagebox
import session
from usuario import Moderador
from obras import Obras
from salas import Salas
from reportes import Reportes
from comentarios import Comentarios


def abrir_ventana_moderador():
    ventana = tk.Toplevel()
    ventana.title("Panel de Moderador")
    ventana.geometry("790x600")

    label_titulo = tk.Label(
        ventana,
        text="Panel de Moderación",
        font=("Arial", 16, "bold")
    )
    label_titulo.pack(pady=10)

    #menu arriba
    menubar = tk.Menu(ventana)
    ventana.config(menu=menubar)

    menu_obras = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Obras", menu=menu_obras)

    menu_reportes = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Reportes", menu=menu_reportes)

    menu_usuarios = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Usuarios", menu=menu_usuarios)

    #lista base
    lista = tk.Listbox(ventana, width=100, height=22)
    lista.pack(pady=10)

    obras_cargadas = []
    reportes_cargados = []
    modo_actual = None

    frame_acciones = tk.Frame(ventana)
    frame_acciones.pack(pady=10)

    #obras
    btn_aprobar = tk.Button(frame_acciones, text="Aprobar obra")
    btn_rechazar = tk.Button(frame_acciones, text="Rechazar obra")

    #reportes
    btn_borrar_obra = tk.Button(frame_acciones, text="Borrar obra")
    btn_ignorar = tk.Button(frame_acciones, text="Ignorar reporte")

    #ocultar botones
    def ocultar_botones():
        btn_aprobar.pack_forget()
        btn_rechazar.pack_forget()
        btn_borrar_obra.pack_forget()
        btn_ignorar.pack_forget()

    #cargar obras
    def cargar_obras_pendientes():
        nonlocal obras_cargadas, modo_actual
        modo_actual = "obras"

        ocultar_botones()

        try:
            obras_cargadas = Obras.listar_obras_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar las obras pendientes.")
            return

        lista.delete(0, tk.END)

        if not obras_cargadas:
            lista.insert(tk.END, "No hay obras pendientes.")
            return

        for i, obra in enumerate(obras_cargadas):
            texto = f"{i+1}. {obra.titulo} | Autor ID: {obra.autor_id}"
            lista.insert(tk.END, texto)

        #mostrar botones de obras
        btn_aprobar.pack(side="left", padx=20)
        btn_rechazar.pack(side="left", padx=20)

    menu_obras.add_command(label="Obras pendientes", command=cargar_obras_pendientes)

    #cargar reportes
    def cargar_reportes_pendientes():
        nonlocal reportes_cargados, modo_actual
        modo_actual = "reportes"

        ocultar_botones()

        try:
            reportes_cargados = Reportes.obtener_reportes_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar los reportes.")
            return

        lista.delete(0, tk.END)

        if not reportes_cargados:
            lista.insert(tk.END, "No hay reportes pendientes.")
            return

        for i, r in enumerate(reportes_cargados):
            texto = (
                f"{i+1}. Reporte ID: {r.id} | Obra ID: {r.obra_id} | "
                f"Autor reporte ID: {r.autor_id} | Motivo: {r.motivo}"
            )
            lista.insert(tk.END, texto)

        #mostrar botones de reportes
        btn_borrar_obra.pack(side="left", padx=20)
        btn_ignorar.pack(side="left", padx=20)

    menu_reportes.add_command(label="Reportes pendientes", command=cargar_reportes_pendientes)

    #ver bloqeuados
    def cargar_bloqueados():
        nonlocal modo_actual
        modo_actual = "bloqueados"

        ocultar_botones()

        try:
            bloqueados = Moderador.listar_bloqueados(session.usuario_id)
        except Exception:
            messagebox.showerror("Error", "No se pudieron cargar los usuarios bloqueados.")
            return

        lista.delete(0, tk.END)

        if not bloqueados:
            lista.insert(tk.END, "No hay usuarios bloqueados.")
            return

        for i, uid in enumerate(bloqueados):
            lista.insert(tk.END, f"{i+1}. Usuario bloqueado ID: {uid}")

    menu_usuarios.add_command(label="Usuarios bloqueados", command=cargar_bloqueados)

    #acciones en obras
    def aprobar_obra():
        if modo_actual != "obras":
            return

        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una obra primero.")
            return

        obra = obras_cargadas[seleccion[0]]

        try:
            Moderador.aprobar_obra(obra.id)
            messagebox.showinfo("Éxito", "La obra ha sido aprobada.")
            cargar_obras_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudo aprobar la obra.")

    def rechazar_obra():
        if modo_actual != "obras":
            return

        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una obra primero.")
            return

        obra = obras_cargadas[seleccion[0]]

        try:
            Moderador.rechazar_obra(obra.id)
            messagebox.showinfo("Obra rechazada", "La obra ha sido rechazada.")
            cargar_obras_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudo rechazar la obra.")

    btn_aprobar.config(command=aprobar_obra)
    btn_rechazar.config(command=rechazar_obra)

    #rportes
    def borrar_obra_reporte():
        if modo_actual != "reportes":
            return

        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un reporte primero.")
            return

        rep = reportes_cargados[seleccion[0]]

        try:
            Moderador.resolver_reporte_borrar_obra(session.usuario_id, rep.id, rep.obra_id)
            messagebox.showinfo("Éxito", "La obra fue eliminada y el reporte resuelto.")
            cargar_reportes_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudo resolver el reporte.")

    def ignorar_reporte():
        if modo_actual != "reportes":
            return

        seleccion = lista.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un reporte primero.")
            return

        rep = reportes_cargados[seleccion[0]]

        try:
            Moderador.resolver_reporte_ignorar(session.usuario_id, rep.id)
            messagebox.showinfo("Reporte ignorado", "El reporte ha sido ignorado.")
            cargar_reportes_pendientes()
        except Exception:
            messagebox.showerror("Error", "No se pudo ignorar el reporte.")

    btn_borrar_obra.config(command=borrar_obra_reporte)
    btn_ignorar.config(command=ignorar_reporte)
