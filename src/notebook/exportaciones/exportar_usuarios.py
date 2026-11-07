"""
HU X01 - Exporta la simulación de usuarios a CSV, Excel y JSON.

Ubicación: src/notebook/exportaciones/exportar_usuarios.py
Salida: data/crudo/ en la raíz del proyecto (integrador_darlin/data/crudo).
Uso directo (desde cualquier carpeta):
    python src/notebook/exportaciones/exportar_usuarios.py
Para generar y exportar todo junto: python src/notebook/main.py
"""
import os
import sys
from pathlib import Path

# Permite importar "simulaciones" aunque este archivo se ejecute directamente
RAIZ_NOTEBOOK = Path(__file__).resolve().parents[1]      # src/notebook
sys.path.insert(0, str(RAIZ_NOTEBOOK))

from simulaciones.simular_usuarios import generar_usuarios  # noqa: E402  (no se copia el código)

RAIZ_PROYECTO = RAIZ_NOTEBOOK.parents[1]                  # integrador_darlin
CARPETA = str(RAIZ_PROYECTO / "data" / "crudo")
NOMBRE = "usuarios_sucio"


def exportar(df):
    """Escribe CSV, Excel y JSON en data/crudo y devuelve [(ruta, df.shape), ...]."""
    os.makedirs(CARPETA, exist_ok=True)
    ruta_csv = os.path.join(CARPETA, f"{NOMBRE}.csv")
    ruta_xlsx = os.path.join(CARPETA, f"{NOMBRE}.xlsx")
    ruta_json = os.path.join(CARPETA, f"{NOMBRE}.json")

    df.to_csv(ruta_csv, index=False, encoding="utf-8")
    df.to_excel(ruta_xlsx, index=False, sheet_name="usuarios")
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)
    return [(ruta_csv, df.shape), (ruta_xlsx, df.shape), (ruta_json, df.shape)]


if __name__ == "__main__":
    df = generar_usuarios()
    for ruta, forma in exportar(df):
        print(f"{os.path.relpath(ruta, RAIZ_PROYECTO)}  {forma}")