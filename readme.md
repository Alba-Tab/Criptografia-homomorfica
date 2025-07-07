# Proyecto de Cifrado Homomórfico Parcial en Python con TenSEAL

Este proyecto implementa un sistema completo de **cifrado homomórfico parcial** utilizando la librería [TenSEAL](https://github.com/OpenMined/TenSEAL) y **FastAPI** para exponer operaciones como servicio web. Permite realizar operaciones aritméticas (suma, multiplicación elemento a elemento, multiplicación por escalar) directamente sobre datos cifrados.

## 🔐 ¿Qué es el cifrado homomórfico?

Permite operar sobre datos cifrados sin necesidad de descifrarlos, obteniendo un resultado cifrado que, al desencriptarse, coincide con el resultado de operar los datos en claro.

## 📦 Estructura del Proyecto

```
Criptografia homomorfica/
├── cifrado.py            # Crear contexto, cifrar y descifrar
├── operaciones.py        # Suma, multiplicación, escalar homomórficos
├── server.py             # API FastAPI para procesar vectores cifrados
├── client.py             # Cliente CLI que cifra, envía y descifra
├── main.py               # Ejemplo monolítico local (pruebas rápidas)
├── datos/                # Carpeta para almacenamiento opcional de .bin
├── resultados/           # Carpeta para almacenar resultados (opcional)
├── .gitignore            # Ignora venv, __pycache__, datos, resultados, etc.
└── venv/                 # Entorno virtual (no subir a Git)
```

## ⚙️ Requisitos

- Python 3.9.x
- Pip ≥ 22.0
- CMake ≥ 3.24
- Visual Studio Build Tools 2022 (para compilar TenSEAL)
- Git (opcional)

## 🚀 Instalación

1. Clonar el repositorio:

   ```bash
   git clone [https://github.com/Alba-Tab/Criptografia-homomorfica.git](https://github.com/Alba-Tab/Criptografia-homomorfica.git)
   ```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Instalar dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

o manualmente instalar las dependencias

```bash
pip install --upgrade pip
pip install tenseal fastapi uvicorn python-multipart request
```

## 📝 Uso local (monolítico)

Ejecuta `main.py` para probar en local sin servidor:

```bash
python main.py
```

Imprime sueldos, bonus, total y retención usando operaciones homomórficas.

## 🌐 API REST con FastAPI

Arranca el servicio:

```bash
uvicorn server:app --reload
```

### Endpoints disponibles

- **POST /operar/sumar**
- **POST /operar/multiplicar**
- **POST /operar/multiplicar_escalar**

Cada petición multipart/form-data debe incluir:

- `vec1_file`: bytes del primer vector cifrado
- `vec2_file` (opcional para escalar): bytes del segundo vector cifrado
- `escalar` (solo para multiplicar_escalar): float en form-data

La respuesta es `application/octet-stream` con el vector cifrado resultante.

## 📡 Cliente CLI

Utiliza `client.py` para interactuar con la API de forma dinámica:

```bash
# Suma
python client.py sumar --v1 10,20,30 --v2 1,2,3

# Multiplicación elemento a elemento
python client.py multiplicar --v1 2,4,6 --v2 3,5,7

# Multiplicación por escalar
python client.py multiplicar_escalar --v1 10,20,30 --escalar 0.5
```

El cliente:

1. Crea contexto CKKS
2. Cifra vectores dados como CSV
3. Envía petición a la API
4. Deserializa y descifra resultado
5. Muestra vector en claro
