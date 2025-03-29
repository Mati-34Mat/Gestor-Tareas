import os
from datetime import datetime
from plyer import notification

ARCHIVO = "tareas.txt"

def leer_tareas():
    tareas = []
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as archivo:
            for linea in archivo:
                nombre, fecha, estado = linea.strip().split(", ")
                tareas.append({"nombre": nombre, "fecha": fecha, "estado": estado})
    return tareas

def guardar_tareas(tareas):
    with open(ARCHIVO, "w") as archivo:
        for tarea in tareas:
            archivo.write(f"{tarea['nombre']}, {tarea['fecha']}, {tarea['estado']}\n")

def agregar_tarea(nombre, fecha):
    tareas = leer_tareas()
    nueva_tarea = {"nombre": nombre, "fecha": fecha, "estado": "pendiente"}
    tareas.append(nueva_tarea)
    guardar_tareas(tareas)
    print(f"Tarea '{nombre}' agregada para {fecha}.")

def mostrar_tareas():
    tareas = leer_tareas()
    if not tareas:
        print("No hay tareas.")
    else:
        for i, tarea in enumerate(tareas, 1):
            print(f"{i}. {tarea['nombre']} - {tarea['fecha']} - {tarea['estado']}")

def chequear_recordatorios():
    tareas = leer_tareas()
    ahora = datetime.now()
    for tarea in tareas:
        if tarea["estado"] == "pendiente":
            fecha_tarea = datetime.strptime(tarea["fecha"], "%d/%m/%Y %H:%M")
            diferencia = (fecha_tarea - ahora).total_seconds() / 60
            if diferencia <= 5 and diferencia >= 0:
                notification.notify(
                    title="¡Tarea por vencer!",
                    message=f"'{tarea['nombre']}' está a punto de vencer: {tarea['fecha']}",
                    timeout=10
                )
            elif ahora >= fecha_tarea:
                notification.notify(
                    title="¡Tarea vencida!",
                    message=f"'{tarea['nombre']}' venció el {tarea['fecha']}",
                    timeout=10
                )

def marcar_hecha(numero):
    tareas = leer_tareas()
    if 0 < numero <= len(tareas):
        tareas[numero-1]["estado"] = "hecha"
        guardar_tareas(tareas)
        print(f"Tarea {numero} marcada como hecha.")
    else:
        print("Número inválido o no hay tareas.")

def main():
    while True:
        print("\n1. Agregar tarea\n2. Mostrar tareas\n3. Chequear recordatorios\n4. Marcar tarea como hecha\n5. Salir\n")
        opcion = input("Elegí una opción: ")
        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            fecha = input("Fecha límite (dd/mm/yyyy hh:mm): ")
            agregar_tarea(nombre, fecha)
        elif opcion == "2":
            mostrar_tareas()
        elif opcion == "3":
            chequear_recordatorios()
        elif opcion == "4":
            mostrar_tareas()
            try:
                numero = int(input("¿Qué tarea querés marcar como hecha? (número): "))
                marcar_hecha(numero)
            except ValueError:
                print("Por favor, ingresá un número válido.")
            else:
                print("Opción inválida.")
        elif opcion == "5":
            print("Adiós!")
            break

if __name__ == "__main__":
    main()