
def suma(vector_cifrado1, vector_cifrado2):
    """
    Suma dos vectores de la misma longitud.
    """
    # TenSEAL comprueba internamente la longitud y el contexto
    return vector_cifrado1 + vector_cifrado2

def suma_por_reduccion(vector_cifrado):
    """
    Suma todos los elementos de un vector cifrado.
    """
    # TenSEAL sum() devuelve un vector donde el primer elemento contiene la suma
    resultado = vector_cifrado.sum()
    return resultado

def multiplicacion(vector_cifrado, vector_cifrado2):
    """
    Multiplica dos vectores cifrados .
    """
    # TenSEAL comprueba internamente el contexto
    prod = vector_cifrado * vector_cifrado2
    return prod

def multiplicacion_por_escalar(vector_cifrado, escalar):
    """
    Multiplica un vector cifrado por un escalar.
    """
    # TenSEAL comprueba internamente el contexto
    return vector_cifrado * escalar
