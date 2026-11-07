"""
main.py - Punto de entrada del notebook del integrador.

Ubicación: src/notebook/main.py
Uso (desde la raíz del proyecto, con el .venv activado):
    python src/notebook/main.py                  # simula + exporta
    python src/notebook/main.py --solo-simular   # solo simula y muestra el resumen

Pasos integrados hoy: simulaciones -> exportaciones.
Pendientes de agregar aquí: limpiezas, consultas, graficas.
"""
import argparse
import os

from simulaciones.simular_usuarios import generar_usuarios
from exportaciones.exportar_usuarios import exportar, RAIZ_PROYECTO


def paso_simulacion():
    """HU F01: genera los usuarios sucios, muestra el resumen y devuelve el DataFrame."""
    df = generar_usuarios()
    print("[1/2] Simulación")
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
    return df


def paso_exportacion(df):
    """HU X01: exporta el DataFrame a data/crudo e imprime ruta y tamaño de cada archivo."""
    print("\n[2/2] Exportación")
    for ruta, forma in exportar(df):
        print(f"{os.path.relpath(ruta, RAIZ_PROYECTO)}  {forma}")


def main():
    """Lee los argumentos y ejecuta los pasos en orden."""
    parser = argparse.ArgumentParser(description="Pipeline del integrador (usuarios).")
    parser.add_argument("--solo-simular", action="store_true",
                        help="ejecuta únicamente la simulación (no exporta archivos)")
    args = parser.parse_args()

    df = paso_simulacion()
    if not args.solo_simular:
        paso_exportacion(df)


if __name__ == "__main__":
    main()