from src.cifrado import create_context, encrypt, decrypt
from src.operaciones import suma
from tenseal import ckks_vector_from
import os

def main():
    # 1. Crear el contexto homomórfico
    contexto = create_context()

    # 2. Datos originales
    sueldos = [1000.0, 1200.5, 1100.75]
    bonus   = [100.0,  150.0,  125.0]

    # 3. Cifrar los vectores
    sueldos_cif = encrypt(contexto, sueldos)
    bonus_cif   = encrypt(contexto, bonus)

    # 4. Serializar a disco
    os.makedirs("datos", exist_ok=True)
    with open("datos/sueldos_cif.bin", "wb") as f:
        f.write(sueldos_cif.serialize())
    with open("datos/bonus_cif.bin", "wb") as f:
        f.write(bonus_cif.serialize())
    # … más tarde o en otro proceso: deserializar
    with open("datos/sueldos_cif.bin", "rb") as f:
        sueldos_bytes = f.read()
    with open("datos/bonus_cif.bin", "rb") as f:
        bonus_bytes = f.read()

    sueldos_cif = ckks_vector_from(contexto, sueldos_bytes)
    bonus_cif   = ckks_vector_from(contexto, bonus_bytes)
    
    # 5. Operación homomórfica sobre datos cargados
    enc_total = suma(sueldos_cif, bonus_cif)

    # 6. Descifrar resultado
    resultado = decrypt(enc_total)

    # 7. Mostrar en claro
    print("Suma de sueldos:", [round(x, 2) for x in resultado])

if __name__ == "__main__":
    main()