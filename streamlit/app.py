import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="SNIES Analytics 2020–2025",
    page_icon="🎓",
    layout="wide"
)

BASE = Path(__file__).resolve().parent

CLAVES = [
    "CODIGO SNIES DEL PROGRAMA",
    "CODIGO DE LA INSTITUCION",
    "CODIGO DEL MUNICIPIO (PROGRAMA)",
    "ID MODALIDAD"
]

PROGRAMA = "NOMBRE_ESTANDARIZADO"
IES = "INSTITUCION DE EDUCACION SUPERIOR (IES)"
MUNICIPIO = "MUNICIPIO_ESTANDARIZADO"

DUMMIES = [
    "SECTOR IES_Privado",
    "TIPO IES_Seccional"
]

ESCENARIOS = {
    "A": {
        "nombre": "Demanda reciente 2025",
        "n": 124,
        "k": 8,
        "columnas": 24,
        "silueta": 0.5300
    },
    "B": {
        "nombre": "Evolución histórica 2020–2025",
        "n": 115,
        "k": 5,
        "columnas": 28,
        "silueta": 0.4452
    },
    "C": {
        "nombre": "Demanda integral",
        "n": 105,
        "k": 2,
        "columnas": 38,
        "silueta": 0.3973
    }
}

# ============================================================
# 2. NOMBRES DE LOS 15 PERFILES ACADÉMICOS
# ============================================================

PERFILES = {
    "A": {
        0: "Demanda baja con ingreso relativo alto",
        1: "Demanda baja con ingreso relativo moderado",
        2: "Demanda muy baja con ingreso relativo favorable",
        3: "Demanda alta con ingreso relativo bajo",
        4: "Demanda intermedia-alta con ingreso relativo bajo",
        5: "Demanda alta con elevada matrícula de primer curso",
        6: "Demanda baja con ingreso relativo muy alto",
        7: "Demanda intermedia con ingreso relativo alto"
    },
    "B": {
        0: "Demanda intermedia con crecimiento del ingreso efectivo",
        1: "Demanda baja con estabilidad relativa de inscritos",
        2: "Demanda baja con crecimiento moderado",
        3: "Demanda reducida con variaciones históricas pequeñas",
        4: "Demanda alta con crecimiento de inscritos superior al de nuevos matriculados"
    },
    "C": {
        0: "Demanda elevada con crecimiento histórico de inscritos",
        1: "Demanda reducida con relativa estabilidad histórica de inscritos"
    }
}


# ============================================================
# 3. INTERPRETACIÓN ACADÉMICA DE LOS 15 CLÚSTERES
# SIGNIFICADO DE LOS PERFILES OBTENIDOS MEDIANTE K-MEANS
#
# Las denominaciones son comparativas dentro de cada
# escenario; no corresponden a umbrales oficiales del SNIES.
# ============================================================

DESCRIPCIONES = {
    "A": {
        0: (
            "Agrupa ofertas académicas que registran un volumen "
            "relativamente reducido de inscritos, pero presentan "
            "una relación elevada entre los matriculados de "
            "primer curso y los inscritos. Esto significa que, "
            "aunque su demanda es baja, el ingreso relativo "
            "es favorable frente a otros grupos del escenario."
        ),
        1: (
            "Agrupa ofertas con un número relativamente bajo "
            "de inscritos y una relación intermedia entre "
            "matriculados de primer curso e inscritos. "
            "Se caracteriza por una demanda reducida y un "
            "ingreso relativo moderado en comparación con "
            "los demás clústeres."
        ),
        2: (
            "Identifica ofertas con uno de los menores volúmenes "
            "de inscritos del escenario. Sin embargo, presentan "
            "una relación relativamente favorable entre "
            "matriculados de primer curso e inscritos. "
            "El perfil combina una demanda muy reducida con "
            "un ingreso relativo comparativamente favorable."
        ),
        3: (
            "Agrupa ofertas que atraen un volumen elevado de "
            "inscritos, pero registran una relación relativamente "
            "baja entre matriculados de primer curso e inscritos. "
            "Esto indica que una demanda alta no necesariamente "
            "se acompaña de un ingreso relativo igualmente alto."
        ),
        4: (
            "Identifica ofertas con un volumen de inscritos "
            "intermedio-alto respecto a los demás grupos, "
            "pero con una relación reducida entre matriculados "
            "de primer curso e inscritos. El perfil combina "
            "una demanda considerable con un ingreso relativo "
            "comparativamente bajo."
        ),
        5: (
            "Agrupa ofertas con una demanda académica elevada "
            "y un volumen destacado de matriculados de primer "
            "curso. Se diferencia de los demás perfiles porque "
            "presenta simultáneamente numerosos inscritos y "
            "una matrícula de primer curso comparativamente "
            "alta en términos absolutos."
        ),
        6: (
            "Agrupa ofertas académicas con un volumen "
            "relativamente reducido de inscritos, pero con una "
            "relación muy elevada entre matriculados de primer "
            "curso e inscritos. Su característica distintiva "
            "no es atraer muchos inscritos, sino presentar "
            "uno de los ingresos relativos más altos del escenario."
        ),
        7: (
            "Agrupa ofertas con un volumen de inscritos "
            "intermedio y una relación elevada entre "
            "matriculados de primer curso e inscritos. "
            "Representa un perfil que combina una demanda "
            "moderada con un ingreso relativo favorable "
            "frente a otros grupos."
        )
    },

    "B": {
        0: (
            "Agrupa ofertas con un volumen histórico de inscritos "
            "intermedio y una tendencia promedio creciente en "
            "los matriculados de primer curso. El perfil "
            "destaca por el aumento absoluto estimado de nuevos "
            "matriculados, aunque los inscritos también presentan "
            "variaciones positivas de distinta magnitud."
        ),
        1: (
            "Agrupa ofertas con una demanda histórica "
            "relativamente baja y pendientes promedio de "
            "inscritos cercanas a cero, con diferencias entre "
            "semestres. Esto describe variaciones absolutas "
            "reducidas del grupo, sin demostrar que todas las "
            "ofertas mantengan una demanda estable."
        ),
        2: (
            "Identifica ofertas con un volumen histórico "
            "reducido de inscritos y pendientes promedio "
            "positivas, pero de magnitud moderada. El perfil "
            "refleja una tendencia creciente en términos "
            "absolutos sin alcanzar los aumentos observados "
            "en los grupos de mayor demanda."
        ),
        3: (
            "Agrupa ofertas con un volumen histórico de "
            "inscritos reducido y pendientes promedio "
            "de pequeña magnitud tanto en inscritos como "
            "en matriculados de primer curso. Describe "
            "cambios históricos absolutos limitados, "
            "sin implicar ausencia de fluctuaciones "
            "en las ofertas individuales."
        ),
        4: (
            "Agrupa ofertas con demanda histórica elevada "
            "y pendientes positivas de inscritos "
            "considerablemente mayores que las pendientes "
            "de matriculados de primer curso. Esto significa "
            "que el número de inscritos presenta un aumento "
            "absoluto estimado superior al de los nuevos "
            "matriculados, sin establecer por sí mismo "
            "las causas de esa diferencia."
        )
    },

    "C": {
        0: (
            "Agrupa ofertas con un volumen de inscritos "
            "comparativamente elevado, tanto en su comportamiento "
            "histórico como en la situación reciente. "
            "Sus pendientes históricas promedio son positivas "
            "y de mayor magnitud que las del otro grupo. "
            "El perfil combina alta demanda con una tendencia "
            "histórica creciente de inscritos."
        ),
        1: (
            "Agrupa ofertas con un volumen de inscritos "
            "comparativamente reducido y pendientes históricas "
            "promedio de pequeña magnitud, próximas a cero. "
            "El perfil describe una demanda menor con cambios "
            "históricos absolutos limitados en términos "
            "promedio, sin demostrar estabilidad estadística "
            "ni uniformidad entre las ofertas."
        )
    }
}


# ============================================================
# 4. INDICADORES ACADÉMICOS
# ============================================================

INDICADORES = {
    "A": {
        "Inscritos S1 — 2025": "INSCRITOS_2025_S1",
        "Inscritos S2 — 2025": "INSCRITOS_2025_S2",
        "Matrícula primer curso S1 — 2025":
            "MATRICULADOS PRIMER CURSO_2025_S1",
        "Matrícula primer curso S2 — 2025":
            "MATRICULADOS PRIMER CURSO_2025_S2",
        "Admisión S1 — 2025": "PROP_ADMISION_2025_S1",
        "Admisión S2 — 2025": "PROP_ADMISION_2025_S2",
        "Ingreso de admitidos S1 — 2025":
            "PROP_INGRESO_ADMITIDOS_2025_S1",
        "Ingreso de admitidos S2 — 2025":
            "PROP_INGRESO_ADMITIDOS_2025_S2",
        "Ingreso relativo S1 — 2025":
            "PROP_INGRESO_INSCRITOS_2025_S1",
        "Ingreso relativo S2 — 2025":
            "PROP_INGRESO_INSCRITOS_2025_S2"
    },
    "B": {},
    "C": {}
}

for s in (1, 2):

    for variable, etiqueta in [
        ("INSCRITOS", "Inscritos"),
        ("MATRICULADOS PRIMER CURSO", "Matrícula primer curso")
    ]:

        INDICADORES["B"][
            f"Promedio histórico {etiqueta} S{s}"
        ] = f"{variable}_PROM_S{s}"

        INDICADORES["B"][
            f"Pendiente {etiqueta} S{s} (estudiantes/año)"
        ] = f"{variable}_PENDIENTE_S{s}"

        INDICADORES["C"][
            f"Promedio histórico {etiqueta} S{s}"
        ] = f"{variable}_PROM_S{s}"

        INDICADORES["C"][
            f"Pendiente {etiqueta} S{s} (estudiantes/año)"
        ] = f"{variable}_PENDIENTE_S{s}"

        INDICADORES["C"][
            f"{etiqueta} S{s} — 2025"
        ] = f"{variable}_2025_S{s}"

    for sufijo, titulo in [
        ("ADMISION", "Admisión"),
        ("INGRESO_ADMITIDOS", "Ingreso de admitidos"),
        ("INGRESO_INSCRITOS", "Ingreso relativo")
    ]:

        INDICADORES["B"][
            f"{titulo} promedio S{s}"
        ] = f"PROP_{sufijo}_PROM_S{s}"

        INDICADORES["C"][
            f"{titulo} promedio S{s}"
        ] = f"PROP_{sufijo}_PROM_S{s}"

        INDICADORES["C"][
            f"{titulo} S{s} — 2025"
        ] = f"PROP_{sufijo}_2025_S{s}"

# ============================================================
# 5. DISEÑO INSTITUCIONAL UPB BUCARAMANGA
# ============================================================

imagenes = [
    BASE / "fondo_universidad.jpg",
    BASE / "fondo_universidad.jpeg",
    BASE / "fondo_universidad.png"
]

imagen = next(
    (p for p in imagenes if p.is_file()),
    None
)

if imagen:

    tipo = (
        "png" if imagen.suffix.lower() == ".png"
        else "jpeg"
    )

    imagen_b64 = base64.b64encode(
        imagen.read_bytes()
    ).decode("ascii")

    fondo = (
        "background-image:"
        "linear-gradient("
        "rgba(255,255,255,.87),"
        "rgba(255,255,255,.92)"
        "),"
        f"url('data:image/{tipo};base64,{imagen_b64}');"
        "background-size:cover;"
        "background-position:center;"
        "background-attachment:fixed;"
    )

else:
    fondo = "background-color:#f4f7fb;"

st.markdown(
    """
    <style>

    .stApp {
    """ + fondo + """
    }

    section[data-testid="stSidebar"] {
        background-color:#103b70;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color:white !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] * {
        color:#172b46;
    }

    div[data-testid="stMetric"] {
        background:rgba(255,255,255,.96);
        border:1px solid #d7e1ec;
        border-radius:12px;
        padding:14px;
    }

    div[data-testid="stMetric"] *,
    section[data-testid="stSidebar"] [data-testid="stMetric"] * {
        color:#172b46 !important;
        opacity:1 !important;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stPlotlyChart"] {
        background:rgba(255,255,255,.95);
        border-radius:10px;
    }

    h1, h2, h3 {
        color:#143b6c;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 6. CARGA Y VALIDACIÓN DE RESULTADOS
# ============================================================

@st.cache_data(show_spinner=False)
def cargar(escenario):

    config = ESCENARIOS[escenario]

    archivo = (
        BASE / f"resultados_cluster_{escenario}.csv"
    )

    tabla = pd.read_csv(
        archivo,
        encoding="utf-8-sig",
        dtype={c: str for c in CLAVES},
        low_memory=False
    )

    dimensiones = (
        config["n"], config["columnas"]
    )

    if tabla.shape != dimensiones:
        raise ValueError(
            f"Escenario {escenario}: dimensiones "
            f"{tabla.shape}; esperadas {dimensiones}"
        )

    requeridas = set(
        CLAVES
        + [
            PROGRAMA,
            IES,
            MUNICIPIO,
            "MODALIDAD",
            "CLUSTER",
            "ESCENARIO"
        ]
        + DUMMIES
        + list(INDICADORES[escenario].values())
    )

    faltantes = requeridas.difference(tabla.columns)

    if faltantes:
        raise ValueError(
            f"Escenario {escenario}: "
            f"faltan columnas {sorted(faltantes)}"
        )

    if tabla.duplicated(CLAVES).any():
        raise ValueError(
            f"Escenario {escenario}: ofertas duplicadas"
        )

    if not tabla["ESCENARIO"].eq(escenario).all():
        raise ValueError(
            f"Escenario {escenario}: "
            "identificación incorrecta"
        )

    tabla["CLUSTER"] = pd.to_numeric(
        tabla["CLUSTER"],
        errors="raise"
    ).astype(int)

    if set(tabla["CLUSTER"]) != set(
        PERFILES[escenario]
    ):
        raise ValueError(
            f"Escenario {escenario}: "
            "clústeres inesperados"
        )

    for columna in set(
        INDICADORES[escenario].values()
    ):

        tabla[columna] = pd.to_numeric(
            tabla[columna],
            errors="raise"
        )

        if tabla[columna].isna().any():
            raise ValueError(
                f"Escenario {escenario}: "
                f"faltantes en {columna}"
            )

    for columna in DUMMIES:

        tabla[columna] = pd.to_numeric(
            tabla[columna],
            errors="raise"
        )

        if not tabla[columna].isin([0, 1]).all():
            raise ValueError(
                f"Escenario {escenario}: "
                f"variable dummy inválida {columna}"
            )

    tabla["PERFIL"] = tabla["CLUSTER"].map(
        PERFILES[escenario]
    )

    return tabla


try:

    tablas = {
        e: cargar(e)
        for e in ESCENARIOS
    }

except Exception as error:

    st.error(
        f"No fue posible cargar los resultados: {error}"
    )

    st.stop()

# ============================================================
# 7. ENCABEZADO Y NAVEGACIÓN
# ============================================================

st.title("🎓 SNIES Analytics")

st.subheader(
    "Segmentación de la demanda académica 2020–2025"
)

st.caption(
    "Minería de Datos · K-means · Metodología CRISP-DM"
)

with st.sidebar:

    st.header("Panel de navegación")

    escenario = st.selectbox(
        "Escenario",
        list(ESCENARIOS),
        key="escenario",
        format_func=lambda e: (
            f"{e} · {ESCENARIOS[e]['nombre']}"
        )
    )

    st.metric(
        "Ofertas del escenario",
        ESCENARIOS[escenario]["n"]
    )

    st.metric(
        "Coeficiente de silueta",
        f"{ESCENARIOS[escenario]['silueta']:.4f}"
    )

    st.info(
        "Análisis descriptivo. "
        "No predice matrícula futura."
    )

# ============================================================
# 8. FILTROS
# ============================================================

original = tablas[escenario]

st.markdown("### Filtros de consulta")

c1, c2, c3 = st.columns(3)

with c1:

    instituciones = st.multiselect(
        "Institución",
        sorted(original[IES].dropna().unique()),
        key=f"institucion_{escenario}"
    )

with c2:

    municipios = st.multiselect(
        "Municipio",
        sorted(original[MUNICIPIO].dropna().unique()),
        key=f"municipio_{escenario}"
    )

with c3:

    programas = st.multiselect(
        "Programa académico",
        sorted(original[PROGRAMA].dropna().unique()),
        key=f"programa_{escenario}"
    )

clusters = st.multiselect(
    "Clúster",
    sorted(PERFILES[escenario]),
    key=f"cluster_{escenario}",
    format_func=lambda k: (
        f"{k} · {PERFILES[escenario][k]}"
    )
)

datos = original.copy()

for campo, seleccion in [
    (IES, instituciones),
    (MUNICIPIO, municipios),
    (PROGRAMA, programas),
    ("CLUSTER", clusters)
]:

    if seleccion:
        datos = datos.loc[
            datos[campo].isin(seleccion)
        ]

# ============================================================
# 9. INDICADORES GENERALES
# ============================================================

a, b, c, d = st.columns(4)

a.metric(
    "Ofertas seleccionadas",
    len(datos)
)

b.metric(
    "Clústeres",
    datos["CLUSTER"].nunique()
)

c.metric(
    "Instituciones",
    datos[IES].nunique()
)

d.metric(
    "Municipios",
    datos[MUNICIPIO].nunique()
)

st.divider()

# ============================================================
# 10. PESTAÑAS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Distribución de clústeres",
    "Consulta de ofertas",
    "Indicadores académicos",
    "Metodología"
])

# ============================================================
# PESTAÑA 1. DISTRIBUCIÓN E INTERPRETACIÓN
# ============================================================

with tab1:

    st.header(
        f"Escenario {escenario} · "
        f"{ESCENARIOS[escenario]['nombre']}"
    )

    if datos.empty:

        st.warning(
            "No hay ofertas para los filtros seleccionados."
        )

    else:

        distribucion = (
            datos.groupby(["CLUSTER", "PERFIL"])
            .size()
            .reset_index(name="OFERTAS")
            .sort_values("CLUSTER")
        )

        distribucion["GRUPO"] = (
            "Clúster "
            + distribucion["CLUSTER"].astype(str)
        )

        fig = px.bar(
            distribucion,
            x="GRUPO",
            y="OFERTAS",
            color="PERFIL",
            text="OFERTAS",
            title="Ofertas académicas por clúster"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            distribucion[
                ["CLUSTER", "PERFIL", "OFERTAS"]
            ],
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            "Las cantidades reflejan los filtros activos."
        )

    # --------------------------------------------------------
    # AYUDA | INTERPRETACIÓN DE LOS PERFILES ACADÉMICOS
    # --------------------------------------------------------

    with st.expander(
        "📘 Ayuda | ¿Cómo interpretar los perfiles académicos?",
        expanded=False
    ):

        st.markdown(
            "Cada perfil combina características de la demanda "
            "académica y, según el escenario, del ingreso relativo "
            "o de su evolución histórica. Las denominaciones "
            "son comparativas entre los clústeres de un mismo "
            "escenario y no representan categorías ni umbrales "
            "oficiales establecidos por el SNIES."
        )

        st.markdown("#### Conceptos para interpretar los perfiles")

        st.markdown(
            "**Demanda académica:** corresponde al volumen de "
            "personas inscritas en las ofertas académicas. "
            "Los términos *muy baja, baja, intermedia y alta* "
            "expresan diferencias relativas entre los grupos "
            "del escenario analizado."
        )

        st.markdown(
            "**Ingreso relativo:** corresponde al cociente entre "
            "el número de matriculados de primer curso y el "
            "número de inscritos. Un ingreso relativo alto "
            "significa que esta relación es comparativamente "
            "elevada, aunque el volumen total de inscritos "
            "pueda ser reducido."
        )

        st.markdown(
            "**Crecimiento histórico:** describe una pendiente "
            "positiva en la evolución de un indicador durante "
            "el periodo analizado. La pendiente representa "
            "el cambio estimado en estudiantes por año."
        )

        st.markdown(
            "**Estabilidad histórica relativa:** describe "
            "pendientes promedio de pequeña magnitud, cercanas "
            "a cero. No implica necesariamente ausencia de "
            "fluctuaciones ni estabilidad estadística."
        )

        st.divider()

        st.markdown("#### Significado de los perfiles identificados")

        for numero, descripcion in DESCRIPCIONES[escenario].items():

            st.markdown(
                f"**Clúster {numero} — "
                f"{PERFILES[escenario][numero]}**"
            )

            st.write(descripcion)

        st.divider()

        st.caption(
            "Nota metodológica: las interpretaciones describen "
            "características promedio de los grupos obtenidos "
            "mediante K-means. No representan evaluaciones "
            "de calidad académica, relaciones causales ni "
            "predicciones. Los cocientes no deben interpretarse "
            "como probabilidades individuales."
        )

# ============================================================
# PESTAÑA 2. CONSULTA DE OFERTAS
# ============================================================

with tab2:

    st.header("Ofertas académicas clasificadas")

    columnas = [
        PROGRAMA,
        IES,
        MUNICIPIO,
        "MODALIDAD",
        "CLUSTER",
        "PERFIL"
    ] + CLAVES

    st.dataframe(
        datos[columnas],
        hide_index=True,
        use_container_width=True
    )

    st.download_button(
        "Descargar resultados filtrados",
        data=datos.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name=f"SNIES_escenario_{escenario}.csv",
        mime="text/csv"
    )

    if not datos.empty:

        consulta = datos.reset_index(drop=True)

        elegido = st.selectbox(
            "Consultar una oferta académica",
            range(len(consulta)),
            key=f"oferta_{escenario}",
            format_func=lambda i: (
                f"{consulta.at[i, PROGRAMA]} | "
                f"{consulta.at[i, IES]} | "
                f"{consulta.at[i, MUNICIPIO]} | "
                f"SNIES {consulta.at[i, CLAVES[0]]} | "
                f"IES {consulta.at[i, CLAVES[1]]} | "
                f"Municipio {consulta.at[i, CLAVES[2]]} | "
                f"Modalidad {consulta.at[i, CLAVES[3]]}"
            )
        )

        oferta = consulta.iloc[elegido]

        st.success(
            f"Clúster {oferta['CLUSTER']}: "
            f"{oferta['PERFIL']}"
        )

        st.write("**Programa:**", oferta[PROGRAMA])
        st.write("**Institución:**", oferta[IES])
        st.write("**Municipio:**", oferta[MUNICIPIO])
        st.write("**Modalidad:**", oferta["MODALIDAD"])
        st.write("**Código SNIES:**", oferta[CLAVES[0]])

# ============================================================
# PESTAÑA 3. INDICADORES ACADÉMICOS
# ============================================================

with tab3:

    st.header("Indicadores académicos")

    if datos.empty:

        st.warning("No hay ofertas para analizar.")

    else:

        opciones = INDICADORES[escenario]

        titulo = st.selectbox(
            "Indicador",
            list(opciones),
            key=f"indicador_{escenario}"
        )

        columna = opciones[titulo]

        grafico = datos.copy()

        grafico["GRUPO"] = (
            "Clúster "
            + grafico["CLUSTER"].astype(str)
        )

        fig = px.box(
            grafico,
            x="GRUPO",
            y=columna,
            color="GRUPO",
            points="outliers",
            title=titulo,
            hover_data=[PROGRAMA, IES]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if "Pendiente" in titulo:

            st.caption(
                "Variación estimada en estudiantes/año; "
                "no es una tasa porcentual."
            )

        if "Ingreso relativo" in titulo:

            st.caption(
                "Cociente entre matriculados de primer "
                "curso e inscritos; no es una "
                "probabilidad individual."
            )

        # ----------------------------------------------------
        # COMPARACIÓN HISTÓRICA DEL ESCENARIO C
        # ----------------------------------------------------

        if escenario == "C":

            st.markdown(
                "### Comparación histórica frente a 2025"
            )

            variable = st.radio(
                "Variable",
                [
                    "INSCRITOS",
                    "MATRICULADOS PRIMER CURSO"
                ],
                horizontal=True,
                key="variable_comparacion_C"
            )

            semestre = st.radio(
                "Semestre",
                [1, 2],
                horizontal=True,
                key="semestre_comparacion_C"
            )

            historica = (
                f"{variable}_PROM_S{semestre}"
            )

            reciente = (
                f"{variable}_2025_S{semestre}"
            )

            comparacion = (
                datos.groupby("CLUSTER")[
                    [historica, reciente]
                ]
                .mean()
                .reset_index()
                .melt(
                    id_vars="CLUSTER",
                    var_name="PERIODO",
                    value_name="PROMEDIO"
                )
            )

            comparacion["PERIODO"] = (
                comparacion["PERIODO"].replace({
                    historica: "Promedio histórico",
                    reciente: "Valor de 2025"
                })
            )

            comparacion["GRUPO"] = (
                "Clúster "
                + comparacion["CLUSTER"].astype(str)
            )

            fig_c = px.bar(
                comparacion,
                x="GRUPO",
                y="PROMEDIO",
                color="PERIODO",
                barmode="group",
                text_auto=".1f",
                title=(
                    f"{variable} · Semestre {semestre}: "
                    "histórico frente a 2025"
                )
            )

            st.plotly_chart(
                fig_c,
                use_container_width=True
            )

            st.caption(
                "Comparación descriptiva del promedio "
                "histórico con el registro de 2025."
            )

# ============================================================
# PESTAÑA 4. METODOLOGÍA
# ============================================================

with tab4:

    st.header("Metodología CRISP-DM")

    st.markdown("""
**Objetivo:** caracterizar la demanda académica mediante
agrupamiento no supervisado K-means.

**Unidad de análisis:** oferta académica identificada
mediante código SNIES, institución, municipio y modalidad.

**Escenario A:** comportamiento de los dos semestres
de 2025 (124 ofertas, 8 clústeres).

**Escenario B:** evolución de 2020 a 2025, con un mínimo
de cuatro años completos (115 ofertas, 5 clústeres).

**Escenario C:** integración de características históricas
y recientes (105 ofertas, 2 clústeres).

**Preparación:** selección de registros Masculino y Femenino
para construir los indicadores académicos; normalización
MinMax de variables cuantitativas y codificación dummy
del sector y tipo de institución.

La modalidad se conserva como variable contextual
y no interviene en el cálculo de distancias de K-means.

**Centroides:** se recuperan de `cluster_centers_` y no
se recalculan durante el perfilamiento. Las variables
cuantitativas se desnormalizan mediante `inverse_transform()`.

Las variables `SECTOR IES_Privado` y `TIPO IES_Seccional`
expresan la proporción de ofertas de esas categorías
dentro del clúster y no requieren desnormalización.

**Evaluación:** coeficiente de silueta, distribución de
ofertas y caracterización académica de los centroides.

**Limitaciones:** los centroides representan promedios
y no describen necesariamente cada oferta individual.
Los cocientes pueden superar 1 y no deben interpretarse
como probabilidades individuales. Las pendientes representan
cambios absolutos estimados en estudiantes/año, no pruebas
de significancia estadística.

Los escenarios utilizan poblaciones y características
distintas; sus coeficientes de silueta no constituyen
una comparación directa de desempeño.

Los resultados son exploratorios, no predictivos ni causales.
    """)

    resumen = pd.DataFrame([
        {
            "Escenario": e,
            "Ofertas": config["n"],
            "Clústeres": config["k"],
            "Silueta": config["silueta"]
        }
        for e, config in ESCENARIOS.items()
    ])

    st.dataframe(
        resumen,
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.caption(
    "Proyecto de Minería de Datos · "
    "SNIES 2020–2025 · Streamlit"
)
