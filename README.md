# SNIES Analytics 2020–2025

## Información académica

**Universidad:** Universidad Pontificia Bolivariana (UPB)  
**Programa:** Maestría en Ciencia de Datos  
**Asignatura:** Minería de Datos  
**Docente:** Ana Oviedo  
**Elaborado por:** Maryory Patricia Villamizar León  
**Año:** 2026

## Descripción del proyecto

SNIES Analytics 2020–2025 es una solución de minería
de datos orientada a caracterizar y segmentar la demanda
académica de programas de educación superior en Colombia.

El proyecto utiliza información del Sistema Nacional
de Información de la Educación Superior (SNIES),
técnicas de preparación de datos y aprendizaje
no supervisado mediante el algoritmo K-means.

Los resultados se presentan mediante una aplicación
interactiva desarrollada con Streamlit.

## Objetivo general

Caracterizar y segmentar la demanda académica de
programas de educación superior en Colombia mediante
técnicas de minería de datos, con el fin de identificar
perfiles de comportamiento reciente e histórico.

## Metodología CRISP-DM

El desarrollo considera las seis etapas:

1. Comprensión del negocio.
2. Comprensión de los datos.
3. Preparación de los datos.
4. Modelado.
5. Evaluación.
6. Despliegue.

## Escenarios de agrupamiento

| Escenario | Enfoque | Ofertas | Clústeres | Silueta |
|---|---|---:|---:|---:|
| A | Demanda reciente de 2025 | 124 | 8 | 0.5300 |
| B | Evolución histórica 2020–2025 | 115 | 5 | 0.4452 |
| C | Demanda integral | 105 | 2 | 0.3973 |

Los escenarios utilizan diferentes conjuntos de ofertas
y características, por lo que sus coeficientes de silueta
no deben utilizarse como una comparación directa
de desempeño entre escenarios.

## Estructura del repositorio

- `README.md`: descripción general del proyecto.
- `notebooks/Clustering_T_F_Maryory.ipynb`:
  desarrollo analítico y metodológico.
- `streamlit/app.py`: aplicación interactiva.
- `streamlit/requirements.txt`: dependencias.
- `streamlit/fondo_universidad.jpg`:
  imagen de fondo de la aplicación.
- `streamlit/resultados_cluster_A.csv`:
  clasificación del escenario A.
- `streamlit/resultados_cluster_B.csv`:
  clasificación del escenario B.
- `streamlit/resultados_cluster_C.csv`:
  clasificación del escenario C.
- `streamlit/resultados_cluster_consolidados.csv`:
  resultados integrados.

## Ejecución de la aplicación

Instalar las dependencias desde la carpeta `streamlit`:

    pip install -r requirements.txt

Iniciar la aplicación:

    streamlit run app.py

La aplicación presenta cuatro secciones:

1. Distribución de clústeres.
2. Consulta de ofertas académicas.
3. Indicadores académicos.
4. Metodología CRISP-DM.

## Interpretación de los resultados

Los clústeres identifican perfiles relativos de demanda
académica, ingreso relativo y evolución histórica.

Las interpretaciones son descriptivas y exploratorias.
No representan predicciones, relaciones causales
ni categorías oficiales establecidas por el SNIES.

## Fuente de datos

Sistema Nacional de Información de la Educación
Superior (SNIES), Colombia.

Período de análisis: 2020–2025.

## Autoría académica

**Maryory Patricia Villamizar León**

Maestría en Ciencia de Datos  
Universidad Pontificia Bolivariana – UPB  
2026
