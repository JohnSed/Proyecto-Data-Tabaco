#IMPORTAR LIBRERÍAS
import pandas as pd
import numpy as np
import streamlit as st
#UBICACIÓN DEL ARCHIVO ORIGINAL
DP = r"D:\Proyectos\Data\Datos Preventa.xlsx"
DN = pd.read_excel(DP,sheet_name="Ordenado")
#VER LAS PRIMERAS FILAS
print(DN.head())
#CONOCER LA ESTRUCTURA DEL DATAFRAME
print(DN.info())
#CONOCER EL RANGO DE FECHAS Minimo y Máximo
print("Fecha mínima:", DN["Fecha"].min())
print("Fecha máxima:", DN["Fecha"].max())
#CONOCER LA CANTIDAD DE FILAS
print("Cantidad de filas del archivo:", len(DN))
#CONTAR REGISTROS POR FECHA
print(DN["Fecha"].value_counts().sort_index())
#Dia Con Más Registros
CF = DN["Fecha"].value_counts().sort_index()
print("Cantidad de registros por fecha:", CF)
print("Día con más registros:", CF.idxmax())
#Mayor cantidad de registros por fecha
print("Mayor cantidad de registros por fecha:", CF.max())
#Dia Con Menos Registros
print("Día con menos registros:", CF.idxmin())
#Menor cantidad de registros por fecha
print("Menor cantidad de registros por fecha:", CF.min())
Categorias=DN["Tipo Visita"].value_counts()
print("Cantidad de registros por tipo de Visita:", Categorias)
Estado=DN["Estado"].value_counts()
print("Cantidad de registros por Estado:", Estado)
Motivos=DN["MotivoRechazo"].value_counts()
print("Cantidad de registros por Motivo:", Motivos)
Ruta=DN["CodPrevendedor"].value_counts()
print("Cantidad de registros por Ruta:", Ruta)
Clientes=DN["CodigoCliente"].value_counts()
print("Cantidad de registros por Cliente:", Clientes)
Entregador=DN["CodRepartidor"].value_counts()
print("Cantidad de registros por Entregador:", Entregador)  
#Registros Duplicados
print("Cantidad de registros duplicados:", DN.duplicated().sum())

# ==========================================
# PREPARACIÓN PARA LA GENERACIÓN SINTÉTICA
# ==========================================

# 1. Trabajar solamente con solicitudes de pedido
DPED = DN[
    DN["Tipo Visita"].eq("Solicitud De Pedido")
].copy()

print("\n--- SOLICITUDES DE PEDIDO ---")
print("Registros:", len(DPED))

# 2. Comprobar identificadores de pedido
for columna in ["NumeroPedido", "Orden Id", "NumeroDocumento"]:
    if columna in DPED.columns:
        print(f"\n{columna}")
        print("Valores únicos:", DPED[columna].nunique())
        print("Valores faltantes:", DPED[columna].isna().sum())

# 3. Distribución de estados
print("\n--- DISTRIBUCIÓN DE ESTADOS ---")
print(
    DPED["Estado"]
    .value_counts(normalize=True, dropna=False)
    .mul(100)
    .round(2)
)

# 4. Distribución por prevendedor
print("\n--- PREVENDEDORES ---")
print(
    DPED["CodPrevendedor"]
    .value_counts()
    .head(15)
)

# 5. Distribución por ciudad
print("\n--- CIUDADES ---")
print(DPED["Ciudad"].value_counts(dropna=False))

# 6. Cantidades y valores comerciales
print("\n--- RESUMEN DE PEDIDOS ---")
print(
    DPED[
        [
            "totalPedido",
            "TotalEntregado",
            "Rechazo",
            "Stick_Pedidos",
            "Stick_Entregados",
            "Stick_Rechazados",
        ]
    ].describe().round(2)
)


# ==========================================
# INVESTIGAR NUMEROPEDIDO REPETIDOS
# ==========================================

# Resumir los registros agrupados por pedido
RP = DPED.groupby("NumeroPedido").agg(
    CantidadRegistros=("Orden Id", "size"),
    OrdenesId=("Orden Id", "nunique"),
    Estados=("Estado", "nunique"),
    Clientes=("CodigoCliente", "nunique"),
    Fechas=("Fecha", "nunique"),
    Documentos=("NumeroDocumento", "nunique"),
)

print("\n--- RESUMEN DE NUMEROPEDIDO ---")
print("Pedidos únicos:", len(RP))
print("Pedidos con varios registros:",
      (RP["CantidadRegistros"] > 1).sum())
print("Pedidos con varios estados:",
      (RP["Estados"] > 1).sum())
print("Pedidos asociados a varios clientes:",
      (RP["Clientes"] > 1).sum())
print("Pedidos registrados en varias fechas:",
      (RP["Fechas"] > 1).sum())

# Mostrar ejemplos para investigar
RE = DPED[
    DPED.duplicated("NumeroPedido", keep=False)
].sort_values("NumeroPedido")

COLUMNAS_REVISION = [
    "Fecha",
    "NumeroPedido",
    "Orden Id",
    "NumeroDocumento",
    "CodigoCliente",
    "Estado",
    "MotivoRechazo",
    "totalPedido",
    "TotalEntregado",
    "Stick_Pedidos",
    "Stick_Entregados",
    "Stick_Rechazados",
]

print("\n--- EJEMPLOS DE PEDIDOS REPETIDOS ---")
print(RE[COLUMNAS_REVISION].head(20).to_string(index=False))




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
