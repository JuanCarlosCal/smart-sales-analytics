import pandas as pd

def analizar_ventas(df):

    ingresos_totales = (
        df["cantidad"] * df["precio"]
    ).sum()

    producto_mas_vendido = (
        df.groupby("producto")["cantidad"]
        .sum()
        .idxmax()
    )

    promedio_venta = (
        df["precio"]
        .mean()
    )

    ventas_por_producto = (
        df.groupby("producto")["cantidad"]
        .sum()
        .to_dict()
    )

    return {
        "registros": len(df),
        "ingresos_totales": float(ingresos_totales),
        "producto_mas_vendido": producto_mas_vendido,
        "promedio_venta": float(promedio_venta),
        "ventas_por_producto": ventas_por_producto
    }