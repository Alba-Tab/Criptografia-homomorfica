import streamlit as st
from client import create_context, encrypt, decrypt, parse_vector, send_request

st.title("Criptografía Homomórfica")

operacion = st.selectbox("Operación", ["sumar", "multiplicar", "multiplicar_escalar"])
v1 = st.text_input("Vector 1 (ej: 1.0,2.0,3.0)")
v2 = st.text_input("Vector 2 (solo para sumar/multiplicar)")
escalar = st.text_input("Escalar (solo para multiplicar_escalar)")

if st.button("Calcular"):
    try:
        contexto = create_context()
        v1_vec = parse_vector(v1)
        v1_cif = encrypt(contexto, v1_vec)
        v2_cif = None
        if operacion in ("sumar", "multiplicar"):
            v2_vec = parse_vector(v2)
            v2_cif = encrypt(contexto, v2_vec)
        result_cif = send_request(
            contexto,
            v1_cif.serialize(),
            operacion,
            vect2_bytes=v2_cif.serialize() if v2_cif else None,
            escalar=float(escalar) if escalar else None
        )
        result = decrypt(result_cif)
        st.success(f"Resultado: {', '.join(str(round(x, 3)) for x in result)}")
    except Exception as e:
        st.error(str(e))