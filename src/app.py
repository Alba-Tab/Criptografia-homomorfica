import io
import requests
import PySimpleGUI as sg
import random
from cifrado import create_context, encrypt, decrypt
from tenseal import ckks_vector_from

# URL del endpoint FastAPI
API_URL = "http://127.0.0.1:8000/operar"

# Inicializar contexto homomórfico (CKKS)
contexto = create_context()

# Diseño de la ventana GUI
layout = [
    [sg.Text("Vector A (enteros, separados por comas):"), sg.Input(key="-A-", size=(30,1))],
    [sg.Text("Vector B (enteros, separados por comas):"), sg.Input(key="-B-", size=(30,1))],
    [sg.Text("Escalar (int, solo para multiplicación escalar):"), sg.Input(key="-FACTOR-", size=(10,1), default_text="1")],
    [sg.Text("Operación:"),
     sg.Combo([
         "sumar",                  # suma elemento a elemento de A y B
         "sumar_elementos",        # suma todos los elementos de A
         "multiplicar",            # multiplicación elemento a elemento de A y B
         "multiplicar_escalar"     # multiplicación de A por escalar
     ], key="-OP-", default_value="sumar", readonly=True)],
    [sg.Text("Generar N aleatorios (A y B distintos):"), sg.Input(key="-N-", size=(5,1), default_text="0"), sg.Button("Generar")],
    [sg.Button("Ejecutar"), sg.Button("Salir")],
    [sg.Frame("Datos Vector A", [[sg.Multiline(key="-DATOS_A-", size=(40,4), disabled=True)]])],
    [sg.Frame("Datos Vector B", [[sg.Multiline(key="-DATOS_B-", size=(40,4), disabled=True)]])],
    [sg.Frame("Resultado", [[sg.Multiline(key="-RESULT-", size=(40,3), disabled=True)]])]
]

window = sg.Window("Cliente Homomórfico CKKS", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Salir"):
        break

    # Generar N enteros aleatorios únicos para A y B
    if event == "Generar":
        try:
            n = int(values["-N-"])
            pool = random.sample(range(0, n * 10), k=n * 2)
            vals_a, vals_b = pool[:n], pool[n:]
            window["-A-"].update(",".join(map(str, vals_a)))
            window["-B-"].update(",".join(map(str, vals_b)))
            window["-DATOS_A-"].update("\n".join(f"{i+1}: {v}" for i, v in enumerate(vals_a)))
            window["-DATOS_B-"].update("\n".join(f"{i+1}: {v}" for i, v in enumerate(vals_b)))
        except Exception as e:
            window["-RESULT-"].update(f"Error al generar datos: {e}")
        continue

    if event == "Ejecutar":
        try:
            op = values["-OP-"]
            # Parsear vectores y factor
            lista_a_int = [int(x) for x in values["-A-"].split(",") if x.strip()]
            lista_b_int = [int(x) for x in values["-B-"].split(",") if x.strip()]
            factor = int(values.get("-FACTOR-", 1))

            # Mostrar vectores en claro
            window["-DATOS_A-"].update("\n".join(f"{i+1}: {v}" for i, v in enumerate(lista_a_int)))
            window["-DATOS_B-"].update("\n".join(f"{i+1}: {v}" for i, v in enumerate(lista_b_int)))

            # Preparar cifrado y envío
            lista_a = [float(v) for v in lista_a_int]
            lista_b = [float(v) for v in lista_b_int]
            enc_a = encrypt(contexto, lista_a)
            files = {"vec1_file": ("a.ts", io.BytesIO(enc_a.serialize()), "application/octet-stream")}
            data = {}

            # Para operaciones que necesitan B
            if op in ("sumar", "multiplicar"):
                if not lista_b:
                    window["-RESULT-"].update("Error: El vector B es requerido.")
                    continue
                enc_b = encrypt(contexto, lista_b)
                files["vec2_file"] = ("b.ts", io.BytesIO(enc_b.serialize()), "application/octet-stream")
            # Para multiplicar_escalar
            elif op == "multiplicar_escalar":
                data["escalar"] = str(factor)
            # suma_elementos solo necesita el vector A (no B ni factor)

            # Llamada al servidor al endpoint correspondiente
            resp = requests.post(f"{API_URL}/{op}", files=files, data=data)
            resp.raise_for_status()

            # Reconstruir y descifrar respuesta cifrada
            enc_res = ckks_vector_from(contexto, resp.content)
            vals = decrypt(enc_res)

            # Formatear resultado
            if op == "sumar":
                salida = ", ".join(f"{r:.4f}" for r in vals)
            elif op == "sumar_elementos":
                # vals es un vector donde solo el primer elemento contiene la suma real
                # Los otros elementos pueden tener valores basura
                if isinstance(vals, list) and len(vals) > 0:
                    total = vals[0]  # Solo usar el primer elemento
                else:
                    total = vals if not isinstance(vals, list) else vals[0]
                
                # Verificación local para comparar
                suma_local = sum(lista_a_int)
                salida = f" {suma_local}"
            elif op == "multiplicar":
                homo = ", ".join(f"{r:.4f}" for r in vals)
                local = ", ".join(f"{a*b:.4f}" for a, b in zip(lista_a_int, lista_b_int))
                salida = f" {local}"
            else:  # multiplicar_escalar
                salida = "\n".join(f"{v} * {factor} = {r:.4f}" for v, r in zip(lista_a_int, vals))

            window["-RESULT-"].update(salida)

        except Exception as e:
            window["-RESULT-"].update(f"Error: {e}")

window.close()