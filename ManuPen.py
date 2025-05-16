import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

def seleccionar_unidad():
    ruta = filedialog.askdirectory(title="Seleccioná tu pendrive o carpeta")
    if ruta:
        entrada_ruta.delete(0, tk.END)
        entrada_ruta.insert(0, ruta)

def limpiar_pendrive():
    unidad = entrada_ruta.get()
    if not os.path.exists(unidad):
        messagebox.showerror("Error", "Ruta no válida.")
        return

    accesos_directos = []
    archivos_ocultos = []
    carpeta_residuos = os.path.join(unidad, "Residuos_USB")

    for carpeta_raiz, carpetas, archivos in os.walk(unidad):
        for nombre in archivos:
            ruta_completa = os.path.join(carpeta_raiz, nombre)
            try:
                # Obtener atributos del archivo
                atributos = subprocess.check_output(f'attrib "{ruta_completa}"', shell=True).decode()
                # Archivos ocultos o sistema
                if 'H' in atributos or 'S' in atributos:
                    archivos_ocultos.append(ruta_completa)
                # Detectar accesos directos (.lnk)
                if nombre.lower().endswith(".lnk"):
                    accesos_directos.append(ruta_completa)
            except:
                pass

    # Restaurar atributos ocultos y sistema
    subprocess.call(f'attrib -s -h -r /s /d "{unidad}\\*"', shell=True)

    # Crear carpeta de residuos y mover accesos directos
    if accesos_directos:
        os.makedirs(carpeta_residuos, exist_ok=True)
        for acceso in accesos_directos:
            try:
                shutil.move(acceso, carpeta_residuos)
            except:
                pass

    mensaje = f"Archivos ocultos restaurados: {len(archivos_ocultos)}\n"
    mensaje += f"Accesos directos falsos movidos a 'Residuos_USB': {len(accesos_directos)}"
    resultado.set(mensaje)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("MANU - Recuperador de Pendrive")
ventana.geometry("480x210")
ventana.resizable(False, False)
ventana.configure(bg="#f9f9f9")

tk.Label(ventana, text="Ruta del pendrive o carpeta:", bg="#f9f9f9", font=("Arial", 11)).pack(pady=7)
entrada_ruta = tk.Entry(ventana, width=60, font=("Arial", 10))
entrada_ruta.pack()

tk.Button(ventana, text="Buscar carpeta o pendrive", command=seleccionar_unidad, bg="#0078D7", fg="white", font=("Arial", 11)).pack(pady=8)
tk.Button(ventana, text="Limpiar y recuperar archivos", command=limpiar_pendrive, bg="#28A745", fg="white", font=("Arial", 11)).pack(pady=8)

resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado, fg="green", bg="#f9f9f9", font=("Arial", 10)).pack(pady=10)

ventana.mainloop()
