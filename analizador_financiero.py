import yfinance as yf


def obtener_datos(ticker: str) -> dict:
    """Obtiene datos financieros de un ticker usando yfinance."""
    accion = yf.Ticker(ticker)
    try:
        info = accion.info
    except Exception as exc:
        raise RuntimeError(
            f"Error al obtener datos del ticker {ticker}: {exc}"
        ) from exc

    if not info:
        raise ValueError(f"No se encontraron datos para el ticker {ticker}")

    datos = {
        "Precio actual": info.get("currentPrice"),
        "Capitalizacion bursatil": info.get("marketCap"),
        "Volumen": info.get("volume"),
        "PER": info.get("trailingPE"),
        "P/B": info.get("priceToBook"),
        "Dividend Yield": info.get("dividendYield"),
        "Beta": info.get("beta"),
        "ROE": info.get("returnOnEquity"),
        "ROA": info.get("returnOnAssets"),
        "Margen neto": info.get("netMargins"),
        "Margen operativo": info.get("operatingMargins"),
        "Deuda/Patrimonio": info.get("debtToEquity"),
        "EV/EBITDA": info.get("enterpriseToEbitda"),
    }
    return datos


def explicar_ratio(nombre: str, valor):
    """Devuelve una pequeña explicacion para cada ratio."""
    explicaciones = {
        "Precio actual": "Precio de la ultima operacion en el mercado.",
        "Capitalizacion bursatil": "Valor total de la empresa en bolsa (acciones x precio).",
        "Volumen": "Numero de acciones negociadas en el dia.",
        "PER": "Cuantas veces paga el mercado los beneficios anuales.",
        "P/B": "Relacion entre el precio y el valor contable por accion.",
        "Dividend Yield": "Rendimiento anual por dividendos.",
        "Beta": "Sensibilidad frente al mercado; >1 implica mas volatilidad.",
        "ROE": "Rentabilidad sobre el patrimonio neto.",
        "ROA": "Rentabilidad sobre los activos totales.",
        "Margen neto": "Beneficio neto dividido entre ingresos.",
        "Margen operativo": "Beneficio operativo dividido entre ingresos.",
        "Deuda/Patrimonio": "Proporcion de deuda respecto al patrimonio neto.",
        "EV/EBITDA": "Valora la empresa incluyendo deuda en relacion al EBITDA.",
    }
    return explicaciones.get(nombre, "")


def valorar_empresa(datos: dict) -> str:
    """Estima si la empresa esta sobrevalorada, infravalorada o razonablemente valorada."""
    per = datos.get("PER") or 0
    pb = datos.get("P/B") or 0
    criterio_alto = per > 25 or pb > 3
    criterio_bajo = per < 15 and pb < 1.5
    if criterio_alto:
        return "Sobrevalorada"
    if criterio_bajo:
        return "Infravalorada"
    return "Razonablemente valorada"


def mostrar_resultados(ticker: str, datos: dict):
    print(f"\nAnalisis de {ticker}\n" + "-" * 40)
    for nombre, valor in datos.items():
        if valor is None:
            texto_valor = "N/D"
        elif isinstance(valor, float):
            texto_valor = f"{valor:.4f}"
        else:
            texto_valor = str(valor)
        print(f"{nombre:20}: {texto_valor}")
        print(f"   {explicar_ratio(nombre, valor)}")
    valoracion = valorar_empresa(datos)
    print("\nValoracion global:", valoracion)


def main():
    ticker = input("Introduce el ticker de la empresa: ").strip().upper()
    if not ticker:
        print("Ticker no valido")
        return
    try:
        datos = obtener_datos(ticker)
    except Exception as exc:
        print(f"Error al obtener datos: {exc}")
        return
    mostrar_resultados(ticker, datos)


if __name__ == "__main__":
    main()
