import tenseal as ts

def create_context():
    """
    Crea un contexto de cifrado homomórfico utilizando TenSEAL.
    usando el esquema CKKS.
    Este contexto sirve como entorno de cifrado/descifrado.
    """
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, 
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context

def encrypt(context, data):
    """
    Cifra los datos utilizando el contexto proporcionado.
    Recibe un contexto y un vector numérico.
    """
    encrypted_data = ts.ckks_vector(context, data)
    return encrypted_data

def decrypt(encrypted_object):
    """
    Descifra los datos cifrados utilizando el contexto proporcionado.
    """
    decrypted_data = encrypted_object.decrypt()
    return decrypted_data