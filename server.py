from fastapi import FastAPI, File, UploadFile, HTTPException, Response, Form
from typing   import Optional
from cifrado import create_context
from operaciones import suma, multiplicacion, multiplicacion_por_escalar
from tenseal import ckks_vector_from

app = FastAPI(title="API Homomórfica CKKS")

# Creamos el contexto una sola vez al iniciar el servidor
contexto = create_context()

OPERACIONES = {
    "sumar": suma,
    "multiplicar": multiplicacion,
    "multiplicar_escalar": multiplicacion_por_escalar,
}

@app.post("/operar/{operacion}")
async def operar(
    operacion: str,
    vec1_file: UploadFile = File(...),
    vec2_file: Optional[UploadFile] = File(None),
    escalar: Optional[float] = Form(None),  # sólo se usa en multiplicar_escalar
):
    """
    Ejecuta operación homomórfica sobre uno o dos vectores cifrados.
    - Para 'sumar' y 'multiplicar' usa dos archivos.
    - Para 'multiplicar_escalar' usa vec1_file + parámetro 'escalar'.
    """
    try:
        # Verificar operación válida
        if operacion not in OPERACIONES:
            raise HTTPException(status_code=404, detail="Operación no soportada")

        # Leer bytes
        vec1_bytes = await vec1_file.read()
        vec1_cif = ckks_vector_from(contexto, vec1_bytes)

        func = OPERACIONES[operacion]

        if operacion == "multiplicar_escalar":
            if escalar is None:
                raise HTTPException(status_code=400, detail="Falta parámetro 'escalar'")
            result_cif = func(vec1_cif, escalar)
        else:
            vec2_bytes = await vec2_file.read()
            vec2_cif = ckks_vector_from(contexto, vec2_bytes)
            result_cif = func(vec1_cif, vec2_cif)

        data = result_cif.serialize()
        return Response(content=data, media_type="application/octet-stream")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))