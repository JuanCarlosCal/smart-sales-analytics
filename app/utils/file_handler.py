import pandas as pd
import io

from fastapi import HTTPException

COLUMNAS_REQUERIDAS = [
    "producto",
    "cantidad",
    "precio"
]

def leer_csv(contenido):

    if not contenido:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío"
        )

    try:

        df = pd.read_csv(
            io.StringIO(
                contenido.decode("utf-8")
            )
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Archivo CSV inválido"
        )

    columnas_faltantes = [
        columna
        for columna in COLUMNAS_REQUERIDAS
        if columna not in df.columns
    ]

    if columnas_faltantes:
        raise HTTPException(
            status_code=400,
            detail=f"Faltan columnas: {columnas_faltantes}"
        )

    return df