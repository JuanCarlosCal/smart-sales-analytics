import pandas as pd
import io

def leer_csv(contenido):

    df = pd.read_csv(
        io.StringIO(
            contenido.decode("utf-8")
        )
    )

    return df