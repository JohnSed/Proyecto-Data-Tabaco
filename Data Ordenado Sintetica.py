#IMPORTAR LIBRERÍAS
import pandas as pd
import numpy as np
import streamlit as st
#UBICACIÓN DEL ARCHIVO ORIGINAL
DP = r"D:\Proyectos\Data\Datos Preventa.xlsx"
DN = pd.read_excel(DP,sheet_name="Ordenado")
# ==========================================
# CREAR CATALOGO DE PREVENDEDORES SINTETICOS
# ==========================================

# Cantidad de preventistas que queremos crear
CANTIDAD_PREVENDEDORES = 20

# Generar códigos ficticios para los preventistas
CODIGOS_PREVENDEDORES = [
    f"SYN_PV{i:03d}"
    for i in range(1, CANTIDAD_PREVENDEDORES + 1)
]

# Convertir la lista en un DataFrame
PREVENDEDORES = pd.DataFrame({
    "CodPrevendedor": CODIGOS_PREVENDEDORES
})

# Revisar el resultado
print(PREVENDEDORES.head(10))
print("Total de preventistas:", len(PREVENDEDORES))

# Crear nombres ficticios para los preventistas
PREVENDEDORES["NomPrevendedor"] = [
    f"Preventista Sintetico {i:03d}"
    for i in range(1, CANTIDAD_PREVENDEDORES + 1)
]

print(PREVENDEDORES.head())

# CREAR CATALOGO DE REPARTIDORES SINTETICOS
CANTIDAD_REPARTIDORES = 15
# Generar códigos ficticios para los repartidores
CODIGOS_REPARTIDORES = [
    f"SYN_RP{i:03d}"
    for i in range(1, CANTIDAD_REPARTIDORES + 1)
]
# Convertir la lista en un DataFrame
REPARTIDORES = pd.DataFrame({"CodRepartidor": CODIGOS_REPARTIDORES})
print(REPARTIDORES.head())
#crear nombres ficticios para los repartidores
REPARTIDORES["NomRepartidor"] = [
    f"Repartidor Sintetico {i:03d}"
    for i in range(1, CANTIDAD_REPARTIDORES + 1)
]
print(REPARTIDORES.head())

# ==========================================
# CREAR CATALOGO DE CLIENTES SINTETICOS
# ==========================================

CANTIDAD_CLIENTES = 1000

CODIGOS_CLIENTES = [
    f"{i:05d}"
    for i in range(1, CANTIDAD_CLIENTES + 1)
]

CLIENTES = pd.DataFrame({
    "CodigoCliente": CODIGOS_CLIENTES
})

CLIENTES["NombreCliente"] = [
    f"Tienda Sintetica {i:05d}"
    for i in range(1, CANTIDAD_CLIENTES + 1)
]

print("\n--- CLIENTES SINTETICOS ---")
print(CLIENTES.head())
print("Total de clientes:", len(CLIENTES))

# Uso solamente las filas de solicitudes de pedido
DPED = DN[
    DN["Tipo Visita"].eq("Solicitud De Pedido")
].copy()

print("\n--- FUENTE DE REFERENCIA ---")
print("Registros de solicitudes:", len(DPED))
print("Fecha inicial:", DPED["Fecha"].min())
print("Fecha final:", DPED["Fecha"].max())


# ==========================================
# CONFIGURAR LA GENERACION DE PEDIDOS
# ==========================================

CANTIDAD_PEDIDOS = 30000

FECHA_INICIO = "2026-01-01"
FECHA_FIN = "2026-07-31"

# Generador aleatorio reproducible
rng = np.random.default_rng(42)

# Crear todas las fechas del periodo
FECHAS_DISPONIBLES = pd.date_range(
    start=FECHA_INICIO,
    end=FECHA_FIN,
    freq="D"
)

# Asignar una fecha aleatoria a cada pedido
FECHAS_PEDIDOS = rng.choice(
    FECHAS_DISPONIBLES,
    size=CANTIDAD_PEDIDOS
)

# Crear la tabla inicial de pedidos
PEDIDOS = pd.DataFrame({
    "Fecha": FECHAS_PEDIDOS
})

# Ordenar cronológicamente
PEDIDOS = PEDIDOS.sort_values(
    "Fecha"
).reset_index(drop=True)

print("\n--- PEDIDOS SINTETICOS ---")
print(PEDIDOS.head(10))
print("Total de pedidos:", len(PEDIDOS))
print("Fecha mínima:", PEDIDOS["Fecha"].min())
print("Fecha máxima:", PEDIDOS["Fecha"].max())

# ==========================================
# ASIGNAR CLIENTES Y PERSONAL A LOS PEDIDOS
# ==========================================

# Asignar códigos aleatorios a cada pedido
PEDIDOS["CodPrevendedor"] = rng.choice(
    PREVENDEDORES["CodPrevendedor"],
    size=CANTIDAD_PEDIDOS
)

PEDIDOS["CodRepartidor"] = rng.choice(
    REPARTIDORES["CodRepartidor"],
    size=CANTIDAD_PEDIDOS
)

PEDIDOS["CodigoCliente"] = rng.choice(
    CLIENTES["CodigoCliente"],
    size=CANTIDAD_PEDIDOS
)

# Incorporar los nombres usando los códigos
PEDIDOS = PEDIDOS.merge(
    PREVENDEDORES,
    on="CodPrevendedor",
    how="left"
)

PEDIDOS = PEDIDOS.merge(
    REPARTIDORES.rename(
        columns={"NomRepartidor": "Repartidor"}
    ),
    on="CodRepartidor",
    how="left"
)

PEDIDOS = PEDIDOS.merge(
    CLIENTES,
    on="CodigoCliente",
    how="left"
)

# Agregar la ubicación del proyecto
PEDIDOS["Regional"] = "Regional Sintetica 01"
PEDIDOS["Ciudad"] = "Depto Sintetico 01"

# Revisar el resultado
print("\n--- PEDIDOS CON CLIENTES Y PERSONAL ---")
print(PEDIDOS.head(10))

print("\nTotal de pedidos:", len(PEDIDOS))
print("Códigos de preventista sin nombre:",
      PEDIDOS["NomPrevendedor"].isna().sum())
print("Códigos de repartidor sin nombre:",
      PEDIDOS["Repartidor"].isna().sum())
print("Códigos de cliente sin nombre:",
      PEDIDOS["NombreCliente"].isna().sum())

# ==========================================
# ASIGNAR ESTADOS A LOS PEDIDOS SINTETICOS
# ==========================================

# Calcular la frecuencia de cada estado en la fuente
DISTRIBUCION_ESTADOS = (
    DPED["Estado"]
    .value_counts(normalize=True)
)

print("\n--- DISTRIBUCION ORIGINAL DE ESTADOS ---")
print((DISTRIBUCION_ESTADOS * 100).round(2))

# Obtener estados y sus probabilidades
ESTADOS = DISTRIBUCION_ESTADOS.index.to_numpy()
PROBABILIDADES_ESTADOS = DISTRIBUCION_ESTADOS.to_numpy()

# Asignar un estado aleatorio a cada pedido
PEDIDOS["Estado"] = rng.choice(
    ESTADOS,
    size=CANTIDAD_PEDIDOS,
    p=PROBABILIDADES_ESTADOS
)

print("\n--- ESTADOS SINTETICOS GENERADOS ---")
print(PEDIDOS["Estado"].value_counts())
print(
    (PEDIDOS["Estado"].value_counts(normalize=True) * 100).round(2)
)


# ==========================================
# CREAR IDENTIFICADORES SINTETICOS
# ==========================================

# Identificador único para cada registro
PEDIDOS["Orden Id"] = [
    f"SYN_ORD{i:06d}"
    for i in range(1, CANTIDAD_PEDIDOS + 1)
]

# Número de pedido sintético
PEDIDOS["NumeroPedido"] = [
    f"SYN_PED{i:06d}"
    for i in range(1, CANTIDAD_PEDIDOS + 1)
]

print("\n--- IDENTIFICADORES DE PEDIDOS ---")
print(
    PEDIDOS[
        ["Orden Id", "NumeroPedido", "Fecha", "Estado"]
    ].head(10)
)

print("Orden Id únicos:", PEDIDOS["Orden Id"].nunique())
print("Números de pedido únicos:", PEDIDOS["NumeroPedido"].nunique())


# ==========================================
# GENERAR VALORES DE LOS PEDIDOS
# ==========================================

# Obtener importes válidos de la fuente original
IMPORTES_ORIGINALES = (
    pd.to_numeric(DPED["totalPedido"], errors="coerce")
    .dropna()
)

# Conservar importes positivos y limitar valores extremos
PERCENTIL_99 = IMPORTES_ORIGINALES.quantile(0.99)

IMPORTES_REFERENCIA = IMPORTES_ORIGINALES[
    (IMPORTES_ORIGINALES > 0) &
    (IMPORTES_ORIGINALES <= PERCENTIL_99)
].to_numpy()

# Asignar un importe de referencia a cada pedido sintético
PEDIDOS["totalPedido"] = rng.choice(
    IMPORTES_REFERENCIA,
    size=CANTIDAD_PEDIDOS
)

# Redondear a pesos enteros
PEDIDOS["totalPedido"] = (
    PEDIDOS["totalPedido"].round(0).astype("int64")
)

print("\n--- VALORES DE PEDIDOS SINTETICOS ---")
print(PEDIDOS["totalPedido"].describe().round(0))
print("\nPrimeros 10 importes:")
print(PEDIDOS["totalPedido"].head(10))

# ==========================================
# CALCULAR ENTREGA Y RECHAZO
# ==========================================

# Inicializar los valores en cero
PEDIDOS["TotalEntregado"] = 0
PEDIDOS["Rechazo"] = 0

# Pedido emitido: entrega completa
MASCARA_EMITIDO = PEDIDOS["Estado"].eq("Emitido")

PEDIDOS.loc[MASCARA_EMITIDO, "TotalEntregado"] = (
    PEDIDOS.loc[MASCARA_EMITIDO, "totalPedido"]
)

# Pedido rechazado en reparto: no se entrega
MASCARA_RECHAZADO = PEDIDOS["Estado"].eq("Rechazado en Reparto")

PEDIDOS.loc[MASCARA_RECHAZADO, "Rechazo"] = (
    PEDIDOS.loc[MASCARA_RECHAZADO, "totalPedido"]
)

# Pedido parcialmente rechazado: entrega parcial
MASCARA_PARCIAL = PEDIDOS["Estado"].eq("Rechazo Parcial")

# Generar una proporción entregada entre 20 % y 80 %
PROPORCION_ENTREGADA = rng.uniform(
    0.20,
    0.80,
    size=MASCARA_PARCIAL.sum()
)

PEDIDOS.loc[MASCARA_PARCIAL, "TotalEntregado"] = (
    PEDIDOS.loc[MASCARA_PARCIAL, "totalPedido"].to_numpy()
    * PROPORCION_ENTREGADA
).round(0)

PEDIDOS.loc[MASCARA_PARCIAL, "Rechazo"] = (
    PEDIDOS.loc[MASCARA_PARCIAL, "totalPedido"]
    - PEDIDOS.loc[MASCARA_PARCIAL, "TotalEntregado"]
)

# Convertir importes a pesos enteros
COLUMNAS_VALOR = ["totalPedido", "TotalEntregado", "Rechazo"]

PEDIDOS[COLUMNAS_VALOR] = (
    PEDIDOS[COLUMNAS_VALOR].round(0).astype("int64")
)

print("\n--- VALIDACION DE ENTREGA Y RECHAZO ---")
print(
    PEDIDOS.groupby("Estado")[
        ["totalPedido", "TotalEntregado", "Rechazo"]
    ].sum()
)

print(
    "\nPedidos cuyo entregado + rechazo supera el valor pedido:",
    (
        PEDIDOS["TotalEntregado"] + PEDIDOS["Rechazo"]
        > PEDIDOS["totalPedido"]
    ).sum()
)


# ==========================================
# GENERAR CANTIDADES DE STICKS
# ==========================================

# Obtener cantidades positivas de la fuente original
STICKS_ORIGINALES = pd.to_numeric(
    DPED["Stick_Pedidos"],
    errors="coerce"
).dropna()

STICKS_REFERENCIA = STICKS_ORIGINALES[
    STICKS_ORIGINALES > 0
].to_numpy()

# Cantidad total solicitada en cada pedido
PEDIDOS["Stick_Pedidos"] = rng.choice(
    STICKS_REFERENCIA,
    size=CANTIDAD_PEDIDOS
).round(0).astype("int64")

# Inicializar cantidades entregadas y rechazadas
PEDIDOS["Stick_Entregados"] = 0
PEDIDOS["Stick_Rechazados"] = 0

# Emitido: se entrega toda la cantidad
MASCARA_EMITIDO = PEDIDOS["Estado"].eq("Emitido")

PEDIDOS.loc[MASCARA_EMITIDO, "Stick_Entregados"] = (
    PEDIDOS.loc[MASCARA_EMITIDO, "Stick_Pedidos"]
)

# Rechazado en reparto: se rechaza toda la cantidad
MASCARA_RECHAZADO = PEDIDOS["Estado"].eq(
    "Rechazado en Reparto"
)

PEDIDOS.loc[MASCARA_RECHAZADO, "Stick_Rechazados"] = (
    PEDIDOS.loc[MASCARA_RECHAZADO, "Stick_Pedidos"]
)

# Rechazo parcial: dividir entre entregado y rechazado
MASCARA_PARCIAL = PEDIDOS["Estado"].eq("Rechazo Parcial")

PROPORCION_STICKS = rng.uniform(
    0.20,
    0.80,
    size=MASCARA_PARCIAL.sum()
)

STICKS_PARCIALES = PEDIDOS.loc[
    MASCARA_PARCIAL, "Stick_Pedidos"
].to_numpy()

STICKS_ENTREGADOS = (
    STICKS_PARCIALES * PROPORCION_STICKS
).round(0).astype("int64")

PEDIDOS.loc[
    MASCARA_PARCIAL, "Stick_Entregados"
] = STICKS_ENTREGADOS

PEDIDOS.loc[
    MASCARA_PARCIAL, "Stick_Rechazados"
] = STICKS_PARCIALES - STICKS_ENTREGADOS

# Validar las cantidades
print("\n--- RESUMEN DE STICKS POR ESTADO ---")
print(
    PEDIDOS.groupby("Estado")[
        ["Stick_Pedidos", "Stick_Entregados", "Stick_Rechazados"]
    ].sum()
)

ERROR_STICKS = (
    PEDIDOS["Stick_Entregados"] + PEDIDOS["Stick_Rechazados"]
    > PEDIDOS["Stick_Pedidos"]
).sum()

print("\nPedidos con sticks entregados + rechazados superiores a los pedidos:",
      ERROR_STICKS)

# ==========================================
# GENERAR NUMEROS DE DOCUMENTO SINTETICOS
# ==========================================

PEDIDOS["NumeroDocumento"] = pd.NA

MASCARA_CON_DOCUMENTO = PEDIDOS["Estado"].isin([
    "Emitido",
    "Rechazo Parcial"
])

PEDIDOS.loc[
    MASCARA_CON_DOCUMENTO, "NumeroDocumento"
] = [
    f"SYN_DOC{i:06d}"
    for i in range(1, MASCARA_CON_DOCUMENTO.sum() + 1)
]

print("\n--- DOCUMENTOS SINTETICOS ---")
print(
    PEDIDOS[
        ["NumeroPedido", "Estado", "NumeroDocumento"]
    ].head(15)
)

print(
    "\nPedidos con documento:",
    PEDIDOS["NumeroDocumento"].notna().sum()
)

print(
    "Pedidos sin documento:",
    PEDIDOS["NumeroDocumento"].isna().sum()
)

# ==========================================
# GENERAR MOTIVOS DE RECHAZO SINTETICOS
# ==========================================

# Tomamos los motivos originales que tienen información.
MOTIVOS_ORIGINALES = (
    DPED["MotivoRechazo"]
    .dropna()
    .astype(str)
    .str.strip()
)

MOTIVOS_ORIGINALES = MOTIVOS_ORIGINALES[
    MOTIVOS_ORIGINALES.ne("")
]

# Identificamos los pedidos que requieren motivo.
MASCARA_RECHAZO = PEDIDOS["Estado"].isin([
    "Rechazado en Reparto",
    "Rechazo Parcial"
])

# Evitamos fallar si la fuente no tiene motivos disponibles.
if not MOTIVOS_ORIGINALES.empty:

    PEDIDOS["MotivoRechazo"] = pd.NA

    PEDIDOS.loc[
        MASCARA_RECHAZO, "MotivoRechazo"
    ] = rng.choice(
        MOTIVOS_ORIGINALES.to_numpy(),
        size=MASCARA_RECHAZO.sum()
    )

else:
    PEDIDOS["MotivoRechazo"] = pd.NA

print("\n--- MOTIVOS DE RECHAZO SINTETICOS ---")
print(
    PEDIDOS.loc[
        MASCARA_RECHAZO,
        ["NumeroPedido", "Estado", "MotivoRechazo"]
    ].head(10)
)

print(
    "\nPedidos rechazados sin motivo:",
    PEDIDOS.loc[
        MASCARA_RECHAZO, "MotivoRechazo"
    ].isna().sum()
)


# ==========================================
# GENERAR TIPO DE ORDEN SINTETICO
# ==========================================

TIPOS_ORIGINALES = (
    DPED["TipoOrden"]
    .dropna()
    .astype(str)
    .str.strip()
)

TIPOS_ORIGINALES = TIPOS_ORIGINALES[
    TIPOS_ORIGINALES.ne("")
]

if not TIPOS_ORIGINALES.empty:

    DISTRIBUCION_TIPOS = TIPOS_ORIGINALES.value_counts(
        normalize=True
    )

    PEDIDOS["TipoOrden"] = rng.choice(
        DISTRIBUCION_TIPOS.index.to_numpy(),
        size=len(PEDIDOS),
        p=DISTRIBUCION_TIPOS.to_numpy()
    )

else:
    PEDIDOS["TipoOrden"] = pd.NA

print("\n--- DISTRIBUCION DE TIPO DE ORDEN ---")
print(PEDIDOS["TipoOrden"].value_counts(dropna=False))


# ==========================================
# VALIDAR Y EXPORTAR PREVENTA SINTETICA
# ==========================================

import os

# Definimos el orden de las columnas finales.
COLUMNAS_FINALES = [
    "Orden Id",
    "Fecha",
    "Regional",
    "Ciudad",
    "CodPrevendedor",
    "NomPrevendedor",
    "CodRepartidor",
    "Repartidor",
    "CodigoCliente",
    "NombreCliente",
    "NumeroPedido",
    "NumeroDocumento",
    "Estado",
    "MotivoRechazo",
    "totalPedido",
    "TotalEntregado",
    "Rechazo",
    "Stick_Pedidos",
    "Stick_Entregados",
    "Stick_Rechazados",
    "TipoOrden"
]

# Verificamos que todas las columnas existan.
COLUMNAS_FALTANTES = [
    columna
    for columna in COLUMNAS_FINALES
    if columna not in PEDIDOS.columns
]

if COLUMNAS_FALTANTES:
    raise ValueError(
        f"Faltan columnas: {COLUMNAS_FALTANTES}"
    )

# Conservamos únicamente las columnas finales y
# en el orden definido.
PEDIDOS = PEDIDOS[COLUMNAS_FINALES].copy()

# Validaciones principales.
assert len(PEDIDOS) == 30000, (
    "La cantidad de pedidos no es 30.000"
)

assert PEDIDOS["Orden Id"].is_unique, (
    "Hay Orden Id duplicados"
)

assert PEDIDOS["NumeroPedido"].is_unique, (
    "Hay números de pedido duplicados"
)

assert (
    PEDIDOS["TotalEntregado"] + PEDIDOS["Rechazo"]
    <= PEDIDOS["totalPedido"]
).all(), "Hay importes que superan el valor pedido"

assert (
    PEDIDOS["Stick_Entregados"]
    + PEDIDOS["Stick_Rechazados"]
    <= PEDIDOS["Stick_Pedidos"]
).all(), "Hay cantidades de sticks inconsistentes"

# Guardamos el CSV en la carpeta del proyecto.
CARPETA_PROYECTO =  r"D:\Proyectos\Data"

RUTA_SALIDA = os.path.join(
    CARPETA_PROYECTO,
    "Datos_Preventa_Sinteticos.csv"
)

PEDIDOS.to_csv(
    RUTA_SALIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- EXPORTACION COMPLETADA ---")
print("Archivo:", RUTA_SALIDA)
print("Total de registros:", len(PEDIDOS))
print("Total de columnas:", len(PEDIDOS.columns))
print("Fecha inicial:", PEDIDOS["Fecha"].min())
print("Fecha final:", PEDIDOS["Fecha"].max())
print("Duplicados de pedido:", PEDIDOS["NumeroPedido"].duplicated().sum())
print("Valores faltantes por columna:")
print(PEDIDOS.isna().sum())
