# ============================================================
# IMPORTAR LIBRERÍAS
# ============================================================

import pandas as pd
import numpy as np
import streamlit as st


# ============================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Análisis de Datos Preventa",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# UBICACIÓN DEL ARCHIVO ORIGINAL
# ============================================================

DP = r"D:\Proyectos\Data\Datos Preventa.xlsx"


# ============================================================
# CARGAR DATOS
# ============================================================

@st.cache_data
def get_data():

    df = pd.read_excel(
        DP,
        sheet_name="Ordenado"
    )

    return df


# ============================================================
# CARGAR DATAFRAME
# ============================================================

DN = get_data()


# ============================================================
# VALIDAR DATOS
# ============================================================

if DN.empty:

    st.error("El archivo no contiene registros.")

    st.stop()


# ============================================================
# PREPARACIÓN DE DATOS
# ============================================================

DN["Fecha"] = pd.to_datetime(
    DN["Fecha"],
    errors="coerce"
)

DN = DN.dropna(
    subset=["Fecha"]
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Análisis de Datos Preventa")

st.markdown(
    """
    ### Dashboard de análisis de visitas de preventa

    Esta aplicación permite explorar los registros de preventa,
    analizar su comportamiento por fecha y conocer la distribución
    de los diferentes tipos de visita.
    """
)


# ============================================================
# INFORMACIÓN GENERAL
# ============================================================

st.header("📌 Información general")
#  Filtros de fecha y ciudad disponibles en la barra lateral.
st.sidebar.header("📅 Filtro de fecha")
fecha_minima = DN["Fecha"].min().date()
fecha_maxima = DN["Fecha"].max().date()
Fecha_Filtro= st.sidebar.date_input(
    "Seleccione un rango de fechas:",
    value=(fecha_minima, fecha_maxima),
    min_value=fecha_minima,
    max_value=fecha_maxima
)
st.sidebar.header("📌 Ciudad")
Ciudades=sorted(DN["Ciudad"].dropna().unique())
Ciudad_seleccionado = st.sidebar.multiselect(
    "Seleccione una Ciudad:",
    options=Ciudades,
    default=Ciudades
)
st.sidebar.header("📌 Lideres")
Lideres=sorted(DN["Lider PMI"].dropna().unique())
lider_seleccionado = st.sidebar.multiselect(
    "Seleccione un Líder:",
    options=Lideres,
    default=Lideres
)
fecha_inicio, fecha_fin = Fecha_Filtro
DN_filtrado = DN[
    (DN["Fecha"].dt.date >= fecha_inicio) &
    (DN["Fecha"].dt.date <= fecha_fin)&
    (DN["Ciudad"].isin(Ciudad_seleccionado)) &
    (DN["Lider PMI"].isin(lider_seleccionado))
]

Cantidad_Rechazo= DN_filtrado["Estado Pws"].value_counts().get("Rechazado", 0)
cantidad_registros = len(DN_filtrado)
cantidad_tipos_visita = DN_filtrado["Tipo Visita"].nunique()


# ============================================================
# KPIs
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        label="📋 Total registros",
        value=f"{cantidad_registros:,}"
    )


with col2:

    st.metric(
        label="📅 Fecha mínima",
        value=fecha_inicio.strftime("%d/%m/%Y")
    )


with col3:

    st.metric(
        label="📅 Fecha máxima",
        value=fecha_fin.strftime("%d/%m/%Y")
    )


with col4:

    st.metric(
        label="🏷️ Tipos de visita",
        value=cantidad_tipos_visita
    )


with col5:

    st.metric(
        label="❌ Registros rechazados",
        value=f"{Cantidad_Rechazo:,}"
    )


# ============================================================
# ESTRUCTURA DE LOS DATOS
# ============================================================

st.header("🔎 Estructura de los datos")


col1, col2 = st.columns(2)


with col1:

    st.write("**Cantidad de filas:**")

    st.write(
        len(DN_filtrado)
    )


with col2:

    st.write("**Cantidad de columnas:**")

    st.write(
        len(DN_filtrado.columns)
    )


st.write("**Columnas disponibles:**")

st.write(
    list(DN.columns)
)


# ============================================================
# REGISTROS POR FECHA
# ============================================================

st.header("📅 Registros por fecha")

# Registros por fecha y ciudad
CF = (
    DN_filtrado
    .groupby(["Fecha","Lider PMI"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

# Registros por fecha y estado
CR = (
    DN_filtrado
    .groupby(["Fecha", "Estado Pws"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

st.subheader("🏙️ Registros por Lider")

st.line_chart(
    CF,
    use_container_width=True
)

st.subheader("📊 Estado PWS por fecha")

st.bar_chart(
    CR,
    use_container_width=True
)


# ============================================================
# DÍA CON MÁS REGISTROS
# ============================================================

dia_mas_registros = CF.idxmax()

mayor_cantidad_registros = CF.max()


# ============================================================
# DÍA CON MENOS REGISTROS
# ============================================================

dia_menos_registros = CF.idxmin()

menor_cantidad_registros = CF.min()


# ============================================================
# KPIs DE REGISTROS POR FECHA
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📈 Mayor cantidad de registros")

    st.metric(
        label="Registros",
        value=f"{mayor_cantidad_registros:,}"
    )

    st.write(
        f"Fecha: **{dia_mas_registros.strftime('%d/%m/%Y')}**"
    )


with col2:

    st.subheader("📉 Menor cantidad de registros")

    st.metric(
        label="Registros",
        value=f"{menor_cantidad_registros:,}"
    )

    st.write(
        f"Fecha: **{dia_menos_registros.strftime('%d/%m/%Y')}**"
    )


# ============================================================
# TABLA DE REGISTROS POR FECHA
# ============================================================

st.subheader("📋 Detalle de registros por fecha")


tabla_fechas = (
    CF
    .reset_index()
)


tabla_fechas.columns = [
    "Fecha",
    "Cantidad de registros"
]


st.dataframe(
    tabla_fechas,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ANÁLISIS POR TIPO DE VISITA
# ============================================================

st.header("🏷️ Análisis por tipo de visita")


Categorias = (
    DN["Tipo Visita"]
    .value_counts()
)


# ============================================================
# GRÁFICO
# ============================================================

st.bar_chart(
    Categorias,
    use_container_width=True
)


# ============================================================
# TABLA DE TIPOS DE VISITA
# ============================================================

tabla_categorias = (
    Categorias
    .reset_index()
)


tabla_categorias.columns = [
    "Tipo de visita",
    "Cantidad de registros"
]


st.dataframe(
    tabla_categorias,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# TIPO DE VISITA MÁS FRECUENTE
# ============================================================

tipo_visita_mas_frecuente = (
    Categorias.idxmax()
)

cantidad_tipo_mas_frecuente = (
    Categorias.max()
)


st.subheader("🏆 Tipo de visita más frecuente")


st.metric(
    label=tipo_visita_mas_frecuente,
    value=f"{cantidad_tipo_mas_frecuente:,} registros"
)


# ============================================================
# EXPLORADOR DE DATOS
# ============================================================

st.header("🔍 Explorador de datos")


tipos_disponibles = sorted(
    DN["Tipo Visita"]
    .dropna()
    .unique()
)


tipo_seleccionado = st.selectbox(
    "Seleccione un tipo de visita:",
    ["Todos"] + tipos_disponibles
)


# ============================================================
# FILTRAR DATOS
# ============================================================

if tipo_seleccionado == "Todos":

    DN_filtrado = DN

else:

    DN_filtrado = DN[
        DN["Tipo Visita"] == tipo_seleccionado
    ]


# ============================================================
# CANTIDAD DE REGISTROS FILTRADOS
# ============================================================

st.metric(
    "📋 Registros encontrados",
    f"{len(DN_filtrado):,}"
)


# ============================================================
# MOSTRAR DATOS
# ============================================================

st.subheader("📄 Registros")


st.dataframe(
    DN_filtrado,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INFORMACIÓN TÉCNICA
# ============================================================

with st.expander("🛠️ Información técnica del DataFrame"):

    st.write("### Tipos de datos")

    st.dataframe(
        DN.dtypes.astype(str).to_frame("Tipo de dato"),
        use_container_width=True
    )


    st.write("### Valores nulos")

    nulos = (
        DN.isnull()
        .sum()
        .to_frame("Valores nulos")
    )

    st.dataframe(
        nulos,
        use_container_width=True
    )


# ============================================================
# FINAL
# ============================================================

st.divider()

st.caption(
    "Dashboard desarrollado en Python, Pandas y Streamlit."
)