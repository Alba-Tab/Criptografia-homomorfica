import tenseal as ts

def create_context():
    """
    Crea un contexto de cifrado homomórfico utilizando TenSEAL.
    usando el esquema CKKS.
    Este contexto sirve como entorno de cifrado/descifrado.
    """
    context = ts.context(
        # Tipo de esquema de cifrado homomórfico(para operaciones en punto flotante)
        ts.SCHEME_TYPE.CKKS, 

        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60])
    # Establece el nivel de precisión y el tamaño del espacio de escala
    context.global_scale = 2**40
    context.generate_galois_keys()
    context.generate_relin_keys()
    
    return context

def encrypt(context, data):
    """
    Cifra los datos utilizando el contexto proporcionado.
    Recibe un contexto y un vector numérico

    :param context: Contexto de cifrado homomórfico.
    :param data: Datos a cifrar (deben ser un vector de números).
    :return: Datos cifrados.
    (ej. [1000, 1500]) y devuelve un objeto cifrado.
    """
    encrypted_data = ts.ckks_vector(context, data)
    return encrypted_data

def decrypt( encrypted_object):
    """
    Descifra los datos cifrados utilizando el contexto proporcionado.
    Recibe un contexto y un objeto cifrado, y devuelve los datos descifrados.

    :param context: Contexto de cifrado homomórfico.
    :param encrypted_data: Datos cifrados a descifrar.
    :return: Datos descifrados (vector de números).
    """
    decrypted_data = encrypted_object.decrypt()
    return decrypted_data