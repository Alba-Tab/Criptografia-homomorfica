# Criptografía Homomórfica con CKKS

Sistema de criptografía homomórfica que permite realizar operaciones aritméticas sobre datos cifrados sin necesidad de descifrarlos, implementado con el esquema CKKS (Cheon-Kim-Kim-Song).

## 🚀 Características

- **Operaciones soportadas:**
  - Suma elemento a elemento de dos vectores
  - Multiplicación elemento a elemento de dos vectores
  - Multiplicación por escalar
  - Suma de todos los elementos de un vector
- **Interfaz gráfica** intuitiva con PySimpleGUI
- **API REST** con FastAPI para operaciones en servidor
- **Cifrado CKKS** para números de punto flotante
- **Verificación automática** comparando resultados homomórficos vs. locales

## Proyecto de Cifrado Homomórfico Parcial en Python con TenSEAL

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

## 🚀 Uso

### 1. Iniciar el servidor

```bash
python server.py
# o tambien
uvicorn server:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`

### 2. Ejecutar la aplicación cliente

```bash
python src/app.py
```

### 3. Usar la interfaz gráfica

1. **Ingresa vectores:** Números enteros separados por comas
2. **Selecciona operación:** Suma, multiplicación, etc.
3. **Genera datos aleatorios:** (Opcional) Para pruebas rápidas
4. **Ejecuta:** Ve los resultados homomórficos vs. locales

## 🏗️ Estructura del proyecto

```
Criptografia homomorfica/
├── src/
│   ├── app.py              # Interfaz gráfica cliente
│   ├── cifrado.py          # Funciones de cifrado/descifrado
│   └── operaciones.py      # Operaciones homomórficas
├── server.py               # Servidor FastAPI
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 🔧 API Endpoints

### `POST /operar/{operacion}`

**Operaciones disponibles:**

- `sumar` - Suma elemento a elemento
- `multiplicar` - Multiplicación elemento a elemento
- `multiplicar_escalar` - Multiplicación por escalar
- `sumar_elementos` - Suma todos los elementos

**Parámetros:**

- `vec1_file`: Archivo con vector cifrado (requerido)
- `vec2_file`: Segundo vector cifrado (para suma/multiplicación)
- `escalar`: Valor escalar (para multiplicación escalar)

## 📊 Ejemplo de uso

```python
# Vectores de ejemplo
A = [2, 4, 6]
B = [1, 3, 5]

# Resultados esperados:
# Suma: [3, 7, 11]
# Multiplicación: [2, 12, 30]
# Suma elementos A: 12
# Multiplicación escalar A*2: [4, 8, 12]
```

### Dependencias

```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

## 📈 Rendimiento

- **Vectores pequeños (≤10 elementos):** Tiempo de respuesta < 1s
- **Vectores medianos (≤100 elementos):** Tiempo de respuesta < 5s
- **Limitaciones:** CKKS tiene overhead significativo vs. operaciones locales

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
