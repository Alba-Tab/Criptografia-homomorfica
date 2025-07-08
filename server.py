from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import Response
import tenseal as ts
from operaciones import sumar, multiplicar, multiplicar_escalar

app = FastAPI()

@app.post("/operar/sumar")
async def sumar_endpoint(v1: UploadFile, v2: UploadFile):
    v1_bytes = await v1.read()
    v2_bytes = await v2.read()
    # El contexto debe venir del cliente, pero aquí asumimos que ambos vectores usan el mismo contexto
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, 
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40
    context.generate_galois_keys()
    v1_cif = ts.ckks_vector_from(context, v1_bytes)
    v2_cif = ts.ckks_vector_from(context, v2_bytes)
    resultado = sumar(v1_cif, v2_cif)
    return Response(content=resultado.serialize(), media_type="application/octet-stream")

from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import Response
import tenseal as ts
from operaciones import sumar, multiplicar, multiplicar_escalar

app = FastAPI()

@app.post("/operar/multiplicar")
async def multiplicar_endpoint(v1: UploadFile, v2: UploadFile, context: UploadFile):
    context_bytes = await context.read()
    context = ts.context_from(context_bytes)
    v1_bytes = await v1.read()
    v2_bytes = await v2.read()
    v1_cif = ts.ckks_vector_from(context, v1_bytes)
    v2_cif = ts.ckks_vector_from(context, v2_bytes)
    resultado = multiplicar(v1_cif, v2_cif)
    return Response(content=resultado.serialize(), media_type="application/octet-stream")
@app.post("/operar/multiplicar_escalar")
async def multiplicar_escalar_endpoint(v1: UploadFile, escalar: float = Form(...)):
    v1_bytes = await v1.read()
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, 
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40
    context.generate_galois_keys()
    v1_cif = ts.ckks_vector_from(context, v1_bytes)
    resultado = multiplicar_escalar(v1_cif, escalar)
    return Response(content=resultado.serialize(), media_type="application/octet-stream")