import argparse
import requests
from src.cifrado import create_context, encrypt, decrypt
from tenseal import ckks_vector_from


def parse_vector(s):
    return [float(x) for x in s.split(",") if x.strip()]


def send_request(contexto, vect_bytes, operacion, vect2_bytes=None, escalar=None):
    files = {"vec1_file": ("v1.bin", vect_bytes, "application/octet-stream")}
    data = {}
    if vect2_bytes:
        files["vec2_file"] = ("v2.bin", vect2_bytes, "application/octet-stream")
    if escalar is not None:
        data["escalar"] = escalar
    url = f"http://127.0.0.1:8000/operar/{operacion}"
    resp = requests.post(url, files=files, data=data)
    resp.raise_for_status()
    return ckks_vector_from(contexto, resp.content)

def main():
    parser = argparse.ArgumentParser(description="Cliente homomórfico CKKS")
    parser.add_argument("operacion",
                        choices=["sumar", "multiplicar", "multiplicar_escalar"])
    parser.add_argument("--v1", required=True,
                        help="Vector 1 como coma-separated, ej: 1.0,2.0,3.0")
    parser.add_argument("--v2",
                        help="Vector 2 como coma-separated (no para escalar)")
    parser.add_argument("--escalar", type=float,
                        help="Escalar (solo para multiplicar_escalar)")

    args = parser.parse_args()

    # 1. Crear contexto y cifrar vectores
    contexto = create_context()
    v1 = parse_vector(args.v1)
    v1_cif = encrypt(contexto, v1)

    v2_cif = None
    if args.operacion in ("sumar", "multiplicar"):
        if not args.v2:
            parser.error(f"Operación {args.operacion} requiere --v2")
        v2 = parse_vector(args.v2)
        v2_cif = encrypt(contexto, v2)

    # 2. Enviar petición y recibir resultado cifrado
    result_cif = send_request(
        contexto,
        v1_cif.serialize(),
        args.operacion,
        vect2_bytes=v2_cif.serialize() if v2_cif else None,
        escalar=args.escalar
    )

    # 3. Desencriptar y mostrar
    result = decrypt(result_cif)
    print("Resultado:", [round(x, 3) for x in result])

if __name__ == "__main__":
    main()