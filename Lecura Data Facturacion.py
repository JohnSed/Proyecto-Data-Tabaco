
import pandas as pd
import numpy as np

DP = r"D:\Proyectos\Data\Datos Preventa.xlsx"

DN = pd.read_excel(DP, sheet_name="Entregado")

print(DN.head(10))

# Resumir datos por Referencia
RP = DN.groupby("Referencia").agg(
    Cantidad_Registros=("CodigoSAP", "size"),
    TiposVenta=("Tipo", "nunique"),
    ClasificacionesVenta=("Clasificacion De Venta", "nunique"),
    Fechas=("fecha", "nunique")
)

print("\n--- RESUMEN DE REFERENCIAS ---")
print("Referencias únicas:", len(RP))
print(
    "Referencias con varios registros:",
    (RP["Cantidad_Registros"] > 1).sum()
)
print(
    "Referencias con varios tipos de venta:",
    (RP["TiposVenta"] > 1).sum()
)
print(
    "Referencias con varias clasificaciones de venta:",
    (RP["ClasificacionesVenta"] > 1).sum()
)
print(
    "Referencias registradas en varias fechas:",
    (RP["Fechas"] > 1).sum()
)
 
# Identificar referencias con más de un registro
REFERENCIAS_REPETIDAS = RP[
    RP["Cantidad_Registros"] > 1
].index

# Mostrar los registros originales de esas referencias
DETALLE_REPETIDOS = DN[
    DN["Referencia"].isin(REFERENCIAS_REPETIDAS)
].sort_values("Referencia")

print("\n--- EJEMPLOS DE REFERENCIAS REPETIDAS ---")
print(
    DETALLE_REPETIDOS[
        [
            "Referencia",
            "CodigoSAP",
            "fecha",
            "Tipo",
            "Clasificacion De Venta"
        ]
    ].head(20).to_string(index=False)
)


# 1. Contar filas completamente duplicadas
duplicados_exactos = DN.duplicated(keep=False)

print("\n--- DUPLICADOS EXACTOS ---")
print("Filas que pertenecen a grupos duplicados:",
      int(duplicados_exactos.sum()))

print("Filas duplicadas adicionales:",
      int(DN.duplicated().sum()))

# 2. Revisar una referencia que aparece varias veces
referencia_ejemplo = "YM012008509"

detalle = DN.loc[
    DN["Referencia"].eq(referencia_ejemplo)
].T

print(f"\n--- DETALLE DE {referencia_ejemplo} ---")
print(detalle.to_string())


# Revisar la relación entre Referencia, Id y líneas de producto

RESUMEN_FACTURAS = DN.groupby("Referencia").agg(
    Cantidad_Lineas=("Referencia", "size"),
    Id_Distintos=("Id", "nunique"),
    Productos_Distintos=("LineaProducto", "nunique"),
    Total_Lineas=("TotalFactura", "sum"),
    Fecha_Distinta=("fecha", "nunique")
)

print("\n--- VALIDACIÓN DE FACTURAS ---")
print("Referencias con varios Id:",
      (RESUMEN_FACTURAS["Id_Distintos"] > 1).sum())

print("Referencias con varias líneas de producto:",
      (RESUMEN_FACTURAS["Productos_Distintos"] > 1).sum())

print("\n--- EJEMPLO DE REFERENCIA ---")
print(
    DN.loc[
        DN["Referencia"].eq("YM012008509"),
        ["Referencia", "Id", "LineaProducto",
         "Importe", "Descuento", "IVA", "Excice", "TotalFactura"]
    ].to_string(index=False)
)

# Revisar los tipos de venta disponibles
print(DN["Tipo Venta"].value_counts(dropna=False))

# Revisar las clasificaciones de venta
print(DN["Clasificacion De Venta"].value_counts(dropna=False))

# Revisar cómo se distribuyen los registros por tipo y clasificación
print(pd.crosstab(
    DN["Tipo Venta"],
    DN["Clasificacion De Venta"],
    dropna=False
))


# Filtrar los registros clasificados como Autoventa
AUTO = DN[
    DN["Clasificacion De Venta"].astype(str).str.strip().str.casefold()
    == "autoventa"
].copy()

print("\n--- RESUMEN DE AUTOVENTA ---")
print("Registros:", len(AUTO))
print("Facturas únicas:", AUTO["Referencia"].nunique())
print("Clientes únicos:", AUTO["CodigoSAP"].nunique())

print("\n--- AUTOVENTA POR FECHA ---")
print(
    AUTO.groupby(AUTO["fecha"].dt.date)
    .agg(
        Facturas=("Referencia", "nunique"),
        Clientes=("CodigoSAP", "nunique"),
        Registros=("Referencia", "size")
    )
    .head(15)
)

print("\n--- AUTOVENTA POR LÍNEA DE PRODUCTO ---")
print(
    AUTO.groupby("LineaProducto", dropna=False)
    .agg(
        Registros=("Referencia", "size"),
        Facturas=("Referencia", "nunique"),
        Packs=("Cantidad(Packs)", "sum"),
        Sticks=("Cantidad(Sticks)", "sum"),
        Total=("TotalFactura", "sum")
    )
    .sort_values("Registros", ascending=False)
)

print("\n--- EJEMPLOS DE AUTOVENTA ---")
print(
    AUTO[
        [
            "CodigoSAP", "fecha", "Referencia", "Id",
            "LineaProducto", "Cantidad(Packs)",
            "Cantidad(Sticks)", "Tipo Venta",
            "Clasificacion De Venta"
        ]
    ].head(20).to_string(index=False)
)
# ==========================================================
# ANÁLISIS ESTADÍSTICO DE AUTOVENTA
# ==========================================================

# Una fila por factura, evitando contar varias veces
# las facturas que tienen múltiples líneas de producto.
FACTURAS = DN.drop_duplicates(subset="Referencia").copy()

# Normalizar la clasificación
FACTURAS["Clasificacion_Norm"] = (
    FACTURAS["Clasificacion De Venta"]
    .astype(str)
    .str.strip()
    .str.casefold()
)

# Contar facturas por clasificación
DISTRIBUCION = FACTURAS["Clasificacion_Norm"].value_counts(
    dropna=False
)

TOTAL_FACTURAS = len(FACTURAS)
TOTAL_AUTOVENTA = (
    FACTURAS["Clasificacion_Norm"] == "autoventa"
).sum()

TOTAL_PREVENTA = (
    FACTURAS["Clasificacion_Norm"] == "preventa"
).sum()

print("\n--- DISTRIBUCIÓN POR FACTURA ÚNICA ---")
print("Total de facturas:", TOTAL_FACTURAS)
print("Facturas Autoventa:", TOTAL_AUTOVENTA)
print("Facturas Preventa:", TOTAL_PREVENTA)

if TOTAL_FACTURAS > 0:
    print(
        "Participación Autoventa:",
        f"{TOTAL_AUTOVENTA / TOTAL_FACTURAS:.2%}"
    )

    print(
        "Participación Preventa:",
        f"{TOTAL_PREVENTA / TOTAL_FACTURAS:.2%}"
    )

# Distribución de Autoventa por tipo de venta
print("\n--- TIPO DE VENTA EN AUTOVENTA ---")
print(
    pd.crosstab(
        FACTURAS["Tipo Venta"],
        FACTURAS["Clasificacion_Norm"],
        normalize="columns"
    ).round(4)
)