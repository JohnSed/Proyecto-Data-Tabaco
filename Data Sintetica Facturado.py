import pandas as pd
import numpy as np

# ==========================================
# 1. RUTAS DE LOS ARCHIVOS EXISTENTES
# ==========================================

RUTA_ORDENADO = (
    r"D:\Proyectos\Data\Datos_Preventa_Sinteticos.csv"
)

RUTA_FACTURACION_ORIGINAL = (
    r"D:\Proyectos\Data\Datos Preventa.xlsx"
)

# ==========================================
# 2. LEER LOS DATOS
# ==========================================

# Data sintética ya generada
ORDENADO = pd.read_csv(RUTA_ORDENADO)

# Data original para analizar las facturas y Autoventa
ENTREGADO = pd.read_excel(
    RUTA_FACTURACION_ORIGINAL,
    sheet_name="Entregado"
)

# ==========================================
# 3. VALIDAR LA LECTURA
# ==========================================

print("Pedidos sintéticos:", len(ORDENADO))
print("Facturas originales:", len(ENTREGADO))

print("\nColumnas de Ordenado:")
print(ORDENADO.columns.tolist())

print("\nColumnas de Entregado:")
print(ENTREGADO.columns.tolist())