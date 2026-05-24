import matplotlib.pyplot as plt

def generar_grafico(df):

    df["ventas"] = df["cantidad"] * df["precio"]

    ventas_por_producto = df.groupby("producto")["ventas"].sum()

    plt.figure(figsize=(8, 5))

    ventas_por_producto.plot(kind="bar")

    plt.title("Ventas por Producto")

    plt.xlabel("Producto")

    plt.ylabel("Ingresos")

    plt.tight_layout()

    ruta = "charts/ventas_chart.png"

    plt.savefig(ruta)

    plt.close()

    return ruta