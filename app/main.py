from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensaje": "Smart Sales Analytics 🚀"
    }

@app.get("/ventas")
def analizar_ventas():

    df = pd.read_csv("data/ventas.csv")

    df["total"] = df["cantidad"] * df["precio"]

    ingresos_totales = df["total"].sum()

    producto_mas_vendido = (
        df.groupby("producto")["cantidad"]
        .sum()
        .idxmax()
    )

    promedio_venta = df["total"].mean()

    ventas_por_producto = (
    df.groupby("producto")["cantidad"]
    .sum()
    .to_dict()
    )

    return {
    "empresa": "Smart Sales Analytics",
    "ingresos_totales": int(ingresos_totales),
    "producto_mas_vendido": producto_mas_vendido,
    "promedio_venta": float(promedio_venta),
    "ventas_por_producto": ventas_por_producto,
    "cantidad_registros": len(df)
}