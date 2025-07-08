import argparse
from cifrado import create_context, encrypt, decrypt
import requests

def parse_vector(texto):
    return [float(x) for x in texto.split(",")]

# ...existing imports...
def send_request(context, v1_bytes, operacion, vect2_bytes=None, escalar=None):
    url = f"http://127.0.0.1:8000/operar/{operacion}"
    files = {
        "v1": v1_bytes,
        "context": context.serialize(save_secret_key=True)
    }
    if vect2_bytes:
        files["v2"] = vect2_bytes
    data = {}
    if escalar is not None:
        data["escalar"] = escalar
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    from tenseal import ckks_vector_from
    return ckks_vector_from(context, response.content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("operacion", choices=["sumar", "multiplicar", "multiplicar_escalar"])
    parser.add_argument("--v1", required=True, help="Vector 1 como coma-separated, ej: 1.0,2.0,3.0")
    parser.add_argument("--v2", help="Vector 2 como coma-separated (no para escalar)")
    parser.add_argument("--escalar", type=float, help="Escalar (solo para multiplicar_escalar)")
    args = parser.parse_args()

    contexto = create_context()
    v1 = parse_vector(args.v1)
    v1_cif = encrypt(contexto, v1)

    v2_cif = None
    if args.operacion in ("sumar", "multiplicar"):
        if not args.v2:
            parser.error(f"Operación {args.operacion} requiere --v2")
        v2 = parse_vector(args.v2)
        v2_cif = encrypt(contexto, v2)

    result_cif = send_request(
        contexto,
        v1_cif.serialize(),
        args.operacion,
        vect2_bytes=v2_cif.serialize() if v2_cif else None,
        escalar=args.escalar
    )

    result = decrypt(result_cif)
    print("Resultado:", [round(x, 3) for x in result])

if __name__ == "__main__":
    main()