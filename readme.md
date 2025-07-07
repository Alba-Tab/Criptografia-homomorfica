# Proyecto de Cifrado Homomórfico Parcial en Python con TenSEAL

Este proyecto implementa un sistema básico de **cifrado homomórfico parcial** utilizando la librería [TenSEAL](https://github.com/OpenMined/TenSEAL). Permite realizar operaciones aritméticas como sumas y multiplicaciones directamente sobre datos cifrados, sin necesidad de descifrarlos, usando el esquema **CKKS**.

## 🔐 ¿Qué es el cifrado homomórfico?

Es una técnica criptográfica que permite realizar operaciones sobre datos cifrados obteniendo un resultado cifrado, que al descifrarse corresponde al resultado como si se hubiese operado directamente sobre los datos en claro.

---

## 📦 Estructura del Proyecto

```
Criptografia homomorfica/
├── main.py                # Script principal
├── cifrado.py            # Funciones para cifrar/descifrar datos
├── operaciones.py        # Funciones que aplican operaciones homomórficas
├── datos/                # Datos de entrada cifrados (opcional)
├── resultados/           # Resultados en texto o descifrados
└── venv/               # Entorno virtual (no debe subirse a Git)
```

---

## ⚙️ Requisitos

- Python 3.9.x
- Pip ≥ 22.0
- CMake ≥ 3.24
- Visual Studio Build Tools 2022 (para compilar TenSEAL)



---

## 🚀 Instalación

### 1. Clonar el repositorio (si aplica)

```bash
git clone https://github.com/Alba-Tab/Criptografia-homomorfica.git

```

### 2. Crear un entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install .
```

---

## 💡 Uso

Ejecuta el script principal con:

```bash
python main.py
```

Este script:

- Crea un contexto homomórfico
- Cifra datos de prueba
- Ejecuta operaciones sobre ellos
- Descifra los resultados y los imprime

---

## 📚 Ejemplo (desde main.py)

```python
from cifrado import crear_contexto, cifrar, descifrar
from operaciones import suma

contexto = crear_contexto()
x = cifrar(contexto, [3.0])
y = cifrar(contexto, [5.0])
resultado = suma(x, y)
print("Resultado:", descifrar(contexto, resultado))
```
