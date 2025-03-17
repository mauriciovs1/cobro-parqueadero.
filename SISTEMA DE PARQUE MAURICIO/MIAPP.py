import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime, timedelta

def guardar_datos():
    placa = placa_entry.get()
    nombre = nombre_entry.get()
    telefono = telefono_entry.get()
    tipo_vehiculo = tipo_vehiculo_var.get()

    if not placa or not nombre or not telefono or not tipo_vehiculo:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("parqueadero.csv", mode="a", newline="") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([placa, fecha_hora, nombre, telefono, tipo_vehiculo])
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {e}")

def limpiar_campos():
    placa_entry.delete(0, tk.END)
    nombre_entry.delete(0, tk.END)
    telefono_entry.delete(0, tk.END)
    tipo_vehiculo_var.set("Carro")  # Restablecer a "Carro" por defecto

def calcular_costo():
    placa_cobro = placa_cobro_entry.get()
    if not placa_cobro:
        messagebox.showerror("Error", "Por favor, ingresa la placa del vehículo.")
        return

    try:
        with open("parqueadero.csv", mode="r") as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                if fila and fila[0] == placa_cobro:
                    fecha_hora_ingreso = datetime.strptime(fila[1], "%Y-%m-%d %H:%M:%S")
                    fecha_hora_salida = datetime.now()
                    tiempo_estacionado = fecha_hora_salida - fecha_hora_ingreso

                    horas_estacionadas = tiempo_estacionado.seconds // 3600
                    minutos_adicionales = (tiempo_estacionado.seconds % 3600) // 60
                    tipo_vehiculo = fila[4]  # Obtener el tipo de vehículo de la fila

                    if tipo_vehiculo == "Carro":
                        costo_hora = 4000
                        costo_media_hora = 2000
                    elif tipo_vehiculo == "Moto":
                        costo_hora = 2000
                        costo_media_hora = 1000
                    else:
                        messagebox.showerror("Error", "Tipo de vehículo no válido.")
                        return

                    costo = horas_estacionadas * costo_hora

                    if horas_estacionadas == 0 and minutos_adicionales < 30 and tiempo_estacionado.days == 0:
                        costo = costo_media_hora
                    elif minutos_adicionales > 0:
                        costo += costo_media_hora

                    messagebox.showinfo("Costo", f"Tiempo estacionado: {horas_estacionadas} horas, {minutos_adicionales} minutos.\nCosto total: ${costo}\n\nGracias por usar nuestros servicios.")
                    return
            messagebox.showerror("Error", "No se encontró la placa del vehículo.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al calcular el costo: {e}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Parqueadero")
ventana.configure(bg="#E3F2FD")

ancho_ventana = int(ventana.winfo_screenwidth() / 2)
alto_ventana = int(ventana.winfo_screenheight() / 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

fuente_grande = ("Arial", 24)

# Etiquetas y entradas para el registro de vehículos
tk.Label(ventana, text="Placa:", bg="#E3F2FD", font=fuente_grande).grid(row=0, column=0, padx=20, pady=10)
placa_entry = tk.Entry(ventana, font=fuente_grande)
placa_entry.grid(row=0, column=1, padx=20, pady=10)

tk.Label(ventana, text="Nombre del Dueño:", bg="#E3F2FD", font=fuente_grande).grid(row=1, column=0, padx=20, pady=10)
nombre_entry = tk.Entry(ventana, font=fuente_grande)
nombre_entry.grid(row=1, column=1, padx=20, pady=10)

tk.Label(ventana, text="Teléfono:", bg="#E3F2FD", font=fuente_grande).grid(row=2, column=0, padx=20, pady=10)
telefono_entry = tk.Entry(ventana, font=fuente_grande)
telefono_entry.grid(row=2, column=1, padx=20, pady=10)

# Selección del tipo de vehículo
tk.Label(ventana, text="Tipo de Vehículo:", bg="#E3F2FD", font=fuente_grande).grid(row=3, column=0, padx=20, pady=10)
tipo_vehiculo_var = tk.StringVar(ventana)
tipo_vehiculo_var.set("Carro")  # Valor predeterminado
tipo_vehiculo_menu = tk.OptionMenu(ventana, tipo_vehiculo_var, "Carro", "Moto")
tipo_vehiculo_menu.config(font=fuente_grande)
tipo_vehiculo_menu.grid(row=3, column=1, padx=20, pady=10)

# Botón de guardar
guardar_button = tk.Button(ventana, text="Guardar", command=guardar_datos, bg="#1976D2", fg="white", font=fuente_grande)
guardar_button.grid(row=4, column=0, columnspan=2, pady=20)

# Etiquetas y entradas para el cobro
tk.Label(ventana, text="Placa para Cobro:", bg="#E3F2FD", font=fuente_grande).grid(row=5, column=0, padx=20, pady=10)
placa_cobro_entry = tk.Entry(ventana, font=fuente_grande)
placa_cobro_entry.grid(row=5, column=1, padx=20, pady=10)

# Botón de calcular costo
calcular_button = tk.Button(ventana, text="Calcular Costo", command=calcular_costo, bg="#4CAF50", fg="white", font=fuente_grande)
calcular_button.grid(row=6, column=0, columnspan=2, pady=20)

ventana.mainloop()

