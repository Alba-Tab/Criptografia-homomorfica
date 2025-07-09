import time
import csv
import tenseal as ts
from cifrado import create_context
from operaciones import suma  # implementa suma elemento a elemento

BATCH_SIZE = 5000

def leer_datos(path):
    """Lee un CSV de una columna numérica y devuelve lista de floats."""
    with open(path, newline='') as f:
        return [float(row[0]) for row in csv.reader(f)]

def procesar_lote(contexto, datos):
    """Cifra, suma homomórficamente y desencripta un lote de datos."""
    # Cifrar lote
    enc = ts.ckks_vector(contexto, datos)
    # Operación homomórfica: sumar todos los elementos
    # Se puede vectorializar o hacerlo reduciendo
    suma_enc = enc.sum()  # suma todos los elementos del vector
    # Desencriptar
    return suma_enc.decrypt()[0]

def main():
    contexto = create_context()  # CKKS, con claves generadas
    datos = leer_datos("datos/gran_dataset.csv")  # e.g. 100 000 filas

    total_claro = sum(datos)  # para validar
    print(f"Sum a claro: {total_claro:.4f}")

    resultados = []
    t0 = time.time()
    # Procesar en lotes
    for i in range(0, len(datos), BATCH_SIZE):
        lote = datos[i : i + BATCH_SIZE]
        t_start = time.time()
        suma_lote = procesar_lote(contexto, lote)
        t_end = time.time()
        resultados.append((i, suma_lote, t_end - t_start))
        print(f"Lote {i//BATCH_SIZE + 1}: suma={suma_lote:.4f}, tiempo={(t_end-t_start):.2f}s")
    t1 = time.time()

    # Reconstruir suma total homomórfica
    suma_homo = sum(r[1] for r in resultados)
    print(f"Suma homomórfica total: {suma_homo:.4f}")
    print(f"Tiempo total homomórfico: {(t1 - t0):.2f}s")

if __name__ == "__main__":
    main()
