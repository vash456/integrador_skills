"""
HU F01 - Simulación de la tabla usuarios (datos sucios a propósito).

Ubicación: src/notebook/simulaciones/simular_usuarios.py
Uso directo (desde la raíz del proyecto):
    python src/notebook/simulaciones/simular_usuarios.py
Para generar y exportar todo junto: python src/notebook/main.py
"""
import random

import numpy as np
import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# Constantes (al inicio, como pide la HU)
# ---------------------------------------------------------------------------
SEMILLA = 42
CANTIDAD_FILAS = 400
PCT_DUPLICADOS_EXACTOS = 0.05          # 5% de filas repetidas tal cual

ROLES = ["usuario", "admin"]
ESTADOS = ["activo", "suspendido", "baneado"]
GENEROS = ["masculino", "femenino", "otro"]
PROVEEDORES_AUTH = ["email", "google"]
IDS_PLAN = [1, 2, 3]

# Semilla fija: el archivo generado es reproducible
random.seed(SEMILLA)
np.random.seed(SEMILLA)
Faker.seed(SEMILLA)
fake = Faker("es_CO")


def generar_usuarios_limpios(n=CANTIDAD_FILAS):
    """Genera n usuarios con datos limpios y devuelve un DataFrame."""
    registros = []
    for i in range(1, n + 1):
        rol = random.choices(ROLES, weights=[0.85, 0.15])[0]          # 85% usuario, 15% admin
        estado = random.choices(ESTADOS, weights=[0.80, 0.15, 0.05])[0]
        proveedor = random.choices(PROVEEDORES_AUTH, weights=[0.7, 0.3])[0]
        fecha_nac = fake.date_of_birth(minimum_age=18, maximum_age=65)
        fecha_reg = fake.date_time_between(start_date="-2y", end_date="now")

        registros.append({
            "id_usuario": i,
            "nombre_usuario": fake.user_name(),
            "correo": fake.unique.email(),
            "genero": random.choice(GENEROS),
            "contrasena_hash": fake.sha256(),
            "proveedor_auth": proveedor,
            "id_plan": random.choice(IDS_PLAN),
            "fecha_nacimiento": fecha_nac.strftime("%Y-%m-%d"),
            "edad_verificada": 1 if random.random() > 0.3 else 0,
            "gemas_saldo": random.randint(0, 500),
            "estado": estado,
            "fecha_registro": fecha_reg,
            "rol": rol,
        })
    return pd.DataFrame(registros)


def obtener_muestra_indices(df, fraccion):
    """Devuelve los índices de una muestra aleatoria (reproducible por la semilla)."""
    return df.sample(frac=fraccion, random_state=random.randint(1, 10000)).index


def ensuciar_texto(texto):
    """Devuelve el texto con mayúsculas/minúsculas raras, espacios o 'N/A' / 'NULL'."""
    variantes = [texto.lower(), texto.upper(), texto.title(), f"  {texto}  ", "N/A", "NULL"]
    return random.choice(variantes)


def ensuciar_booleano(valor):
    """Convierte 1/0 en representaciones inconsistentes (SI, no, True, falso...)."""
    if valor == 1:
        return random.choice(["SI", "si", "True", "1", "verdadero"])
    return random.choice(["NO", "no", "False", "0", "falso"])


def ensuciar_datos(df_original):
    """Aplica los errores controlados que luego se resuelven en la fase de limpieza."""
    df = df_original.copy()

    # 1) Espacios sobrantes en nombre_usuario (12%)
    idx = obtener_muestra_indices(df, 0.12)
    df.loc[idx, "nombre_usuario"] = "  " + df.loc[idx, "nombre_usuario"] + " "

    # 2) nombre_usuario en mayúsculas (8%)
    idx = obtener_muestra_indices(df, 0.08)
    df.loc[idx, "nombre_usuario"] = df.loc[idx, "nombre_usuario"].str.upper()

    # 3) Correos sin '@' (5%)
    idx = obtener_muestra_indices(df, 0.05)
    df.loc[idx, "correo"] = df.loc[idx, "correo"].str.replace("@", "", regex=False)

    # 4) Correos nulos (4%)
    idx = obtener_muestra_indices(df, 0.04)
    df.loc[idx, "correo"] = None

    # 5) Géneros nulos (10%)
    idx = obtener_muestra_indices(df, 0.10)
    df.loc[idx, "genero"] = None

    # 6) Inconsistencias tipográficas en rol (10%)
    idx = obtener_muestra_indices(df, 0.10)
    df.loc[idx, "rol"] = df.loc[idx, "rol"].map(ensuciar_texto)

    # 7) edad_verificada con texto mixto (15%)
    df["edad_verificada"] = df["edad_verificada"].astype(object)
    idx = obtener_muestra_indices(df, 0.15)
    df.loc[idx, "edad_verificada"] = df.loc[idx, "edad_verificada"].map(ensuciar_booleano)

    # 8) fecha_registro con dos formatos mezclados (25% en formato latino)
    iso = df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    df["fecha_registro"] = iso
    idx = obtener_muestra_indices(df, 0.25)
    df.loc[idx, "fecha_registro"] = latino.loc[idx]

    # 9) gemas_saldo negativo (3%)
    idx = obtener_muestra_indices(df, 0.03)
    df.loc[idx, "gemas_saldo"] = -1 * df.loc[idx, "gemas_saldo"]

    # 10) Filas repetidas tal cual: 5% del total
    n_duplicados = round(len(df) * PCT_DUPLICADOS_EXACTOS)
    duplicadas = df.sample(n=n_duplicados, random_state=SEMILLA)
    return pd.concat([df, duplicadas], ignore_index=True)


def generar_usuarios(n=CANTIDAD_FILAS):
    """Genera los usuarios limpios, los ensucia y DEVUELVE el DataFrame (para exportarlo)."""
    df = ensuciar_datos(generar_usuarios_limpios(n))
    return df


if __name__ == "__main__":
    df = generar_usuarios()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())