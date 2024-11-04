from dash import Dash, callback, dcc, html, Output, Input
import pandas as pd 
import plotly.express as px 
import plotly.io as pio
import dash_bootstrap_components as dbc
from urllib.request import urlopen
import json
import requests


app = Dash(
    __name__,    
    title="Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
#llamado de json
with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json') as response:
    counties = json.load(response)

# dataset
#reading the dataset in a variable df
df1 = pd.read_excel('Anexo4.Covid-19_CE_15-03-23.xlsx')

df1.info()

#app.layout = [html.Div(children='Hello World')]

app.layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    "Mortalidad en Colombia de los casos de covid-19 para el año 2020 y 2021",  # title
                    className="title",
                ),
                html.H3(
                    "Aplicación de datos con una web interactiva con informes gráficos utilizando Python y librería plotly y dash.",  # title
                    className="subtitle-small",
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                dcc.Graph(
                                    id="gender-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "280px"},
                                ),
                                type="circle",
                                color="#f79500",
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Loading(
                                dcc.Graph(
                                    id="age-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "280px"},
                                ),
                                type="circle",
                                color="#f79500",
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            dcc.Loading(
                                dcc.Graph(
                                    id="education-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "280px"},
                                ),
                                type="circle",
                                color="#f79500",
                            ),
                            width=4,
                        ),
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                dcc.Graph(
                                    id="state-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "337px"},
                                ),
                                type="circle",
                                color="#f79500",
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "337px"},
                                ),
                                type="circle",
                                color="#f79500",
                            ),
                            width=6,
                        ),
                    ],
                ),
            ],
            className="page-content",
        )
    ],
    fluid=True,
)
# callback cards and graphs
@callback(
    [
        Output("gender-chart", "figure"),
        Output("age-chart", "figure"),
        Output("education-chart", "figure"),
        Output("state-chart", "figure"),
        Output("income-chart", "figure"),
        Input("gender-chart", "id"),
        Input("age-chart", "id"),
        Input("education-chart", "id"),
        Input("state-chart", "id"),
        Input("income-chart", "id"),
    ],
)
def update_chart(gender, age, education, state, income):

    # gender
    # -----------------------
    # Gráfico circular de tipos de casos
    # -----------------------
    # Convertir las fechas a formato datetime
    df1['FECHA DEFUNCIÓN'] = pd.to_datetime(df1['FECHA DEFUNCIÓN'], errors='coerce')

    # Filtrar para el año 2021
    df_2021 = df1[df1['FECHA DEFUNCIÓN'].dt.year == 2021]

    # Filtrar muertes confirmadas de COVID-19 en ambos años
    df_confirmados = df1[df1['COVID-19'] == 'CONFIRMADO']

    # Contar los casos por tipo (confirmado, sospechoso, descartado)
    tipos_casos_2021 = df_2021['COVID-19'].value_counts().reset_index()
    tipos_casos_2021.columns = ['TIPO_CASO', 'TOTAL']

    # Crear el gráfico circular
    gender_chart = px.pie(
        tipos_casos_2021,
        values='TOTAL',
        names='TIPO_CASO',
        title='Distribución de casos de COVID-19 reportados en 2021',
        labels={'TOTAL': 'Total de casos', 'TIPO_CASO': 'Tipo de caso'}
    )

    # age
    # -----------------------
    # Gráfico de barras horizontal para ciudades (2021)
    # -----------------------

    # Agrupar por ciudad y contar las muertes confirmadas
    muertes_por_ciudad = df_2021[df_2021['COVID-19'] == 'CONFIRMADO'].groupby('MUNICIPIO').size().reset_index(name='MUERTES_2021')

    # Ordenar y seleccionar las 5 ciudades con más muertes
    top_5_ciudades = muertes_por_ciudad.nlargest(5, 'MUERTES_2021')

    # Crear el gráfico de barras horizontal
    age_chart = px.bar(
        top_5_ciudades,
        x='MUERTES_2021',
        y='MUNICIPIO',
        orientation='h',
        title='Top 5 ciudades con mayor índice de muertes confirmadas en 2021',
        labels={'MUERTES_2021': 'Número de muertes', 'MUNICIPIO': 'Ciudad'}
    )

    # education
    # -----------------------
    # Gráfico de línea: muertes confirmadas por mes (2020 y 2021)
    # -----------------------

    # Agrupar por año y mes, contando las muertes confirmadas
    df_confirmados['AÑO_MES'] = df_confirmados['FECHA DEFUNCIÓN'].dt.to_period('M')
    muertes_mensuales = df_confirmados.groupby('AÑO_MES').size().reset_index(name='MUERTES_MENSUALES')

    # Convertir la columna de año y mes a formato datetime para el gráfico de línea
    muertes_mensuales['AÑO_MES'] = muertes_mensuales['AÑO_MES'].dt.to_timestamp()

    # Crear el gráfico de líneas
    education_chart = px.line(
        muertes_mensuales,
        x='AÑO_MES',
        y='MUERTES_MENSUALES',
        title='Muertes confirmadas por COVID-19 por mes (2020-2021)',
        labels={'AÑO_MES': 'Fecha', 'MUERTES_MENSUALES': 'Número de muertes'}
    )

    # state

    # Agrupar por departamento y contar las muertes confirmadas en 2021
    muertes_por_departamento = df_2021[df_2021['COVID-19'] == 'CONFIRMADO'].groupby('DEPARTAMENTO').size().reset_index(name='MUERTES_2021')

    # Descargar el archivo GeoJSON con las fronteras de Colombia
    url = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json'
    geojson = requests.get(url).json()

    # Mapa interactivo de las muertes confirmadas por departamento
    state_chart = px.choropleth(
        muertes_por_departamento,
        geojson=geojson,
        locations='DEPARTAMENTO',  # Columna de departamentos
        featureidkey='properties.NOMBRE_DPT',  # Nombre de los departamentos en el GeoJSON
        color='MUERTES_2021',  # Columna de valores (muertes)
        hover_name='DEPARTAMENTO',  # Mostrar el nombre del departamento al pasar el mouse
        title='Muertes confirmadas por COVID-19 en 2021 por departamento'
    )

    # Ajustar el zoom y la posición del mapa en Colombia
    state_chart.update_geos(fitbounds="locations", visible=False)

    # income
    # -----------------------
    # Histograma de frecuencias de muertes por edad (2020)
    # -----------------------

    # Filtrar los datos para 2020 y casos confirmados
    df_2020_confirmados = df1[(df1['FECHA DEFUNCIÓN'].dt.year == 2020) & (df1['COVID-19'] == 'CONFIRMADO')]

    # Definir los rangos quinquenales de edad
    bins = list(range(0, 91, 5)) + [float('inf')]  # Intervalos hasta "90 o más"
    labels = [f"{i}-{i+4}" for i in range(0, 90, 5)] + ["90 o más"]

    # Función para convertir cada valor a float
    def convertir_a_float(valor):
        if isinstance(valor, int) or isinstance(valor, float):
            return float(valor)
        elif isinstance(valor, str):
            # Quitar espacios en blanco
            valor = valor.strip()
            # Verificar si la cadena está vacía
            if valor == "":
                return float('nan')  # Usar NaN para representar valores vacíos
            elif '(' in valor:
                return float(valor.split('(')[0])
            else:
                return float(valor)
        else:
            return float('nan')  # Usar NaN si el valor no es ni int ni str
        
    # Aplicar la función a la columna "EDAD FALLECIDO"
    df1['EDAD FALLECIDO'] = df1['EDAD FALLECIDO'].apply(convertir_a_float)    

    # Crear una columna de edades en intervalos quinquenales
    df_2020_confirmados['EDAD_QUINQUENAL'] = pd.cut(df1['EDAD FALLECIDO'], bins=bins, labels=labels, right=False)

    # Contar las muertes en cada intervalo de edad
    muertes_por_edad = df_2020_confirmados['EDAD_QUINQUENAL'].value_counts().sort_index().reset_index()
    muertes_por_edad.columns = ['EDAD_QUINQUENAL', 'FRECUENCIA']

    # Crear el histograma
    income_chart = px.bar(
        muertes_por_edad,
        x='EDAD_QUINQUENAL',
        y='FRECUENCIA',
        title='Frecuencia de muertes confirmadas por COVID-19 por edades quinquenales (2020)',
        labels={'EDAD_QUINQUENAL': 'Rango de edad', 'FRECUENCIA': 'Número de muertes'}
    )

    return (
        gender_chart,
        age_chart,
        education_chart,
        state_chart,
        income_chart,
    )

if __name__ == '__main__':
    app.run(debug=True)
