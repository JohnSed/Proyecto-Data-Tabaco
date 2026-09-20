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
st.set_page_config(page_title="Análisis de Datos Preventa", page_icon="📊", layout="wide")
@st.cache_data
def get_data():
    return DN