import streamlit as st
from client import create_context, encrypt, decrypt, parse_vector, send_request
from db_utils import init_db, guardar_operacion, obtener_historial

init_db()

st.title("Criptografía Homomórfica")

menu = st.sidebar.selectbox("Menú", ["Calculadora", "Historial"])

if menu == "Calculadora":
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
            resultado_str = ', '.join(str(round(x, 3)) for x in result)
            guardar_operacion(
                operacion,
                v1,
                v2 if v2 else "",
                float(escalar) if escalar else None,
                resultado_str
            )
            st.success(f"Resultado: {resultado_str}")
        except Exception as e:
            st.error(str(e))

elif menu == "Historial":
    st.header("Historial de operaciones")
    historial = obtener_historial()
    if historial:
        st.table([
            {
                "Operación": op,
                "Vector 1": v1,
                "Vector 2": v2,
                "Escalar": esc,
                "Resultado": res,
                "Fecha": fecha
            }
            for op, v1, v2, esc, res, fecha in historial
        ])
    else:
        st.info("No hay operaciones registradas.")