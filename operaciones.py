def sumar(v1_cif, v2_cif):
    """
    Suma dos vectores de la misma longitud.
    """
    # TenSEAL comprueba internamente la longitud y el contexto
    return v1_cif + v2_cif

def multiplicar(v1_cif, v2_cif):
    """
    Multiplica dos vectores cifrados .
    """
    # TenSEAL comprueba internamente el contexto
    return v1_cif * v2_cif

def multiplicar_escalar(v1_cif, escalar):
    """
    Multiplica un vector cifrado por un escalar.
    """
    return v1_cif * escalar
