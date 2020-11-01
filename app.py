import dash
#from dash.dependencies import Input, Output, State
from datetime import date
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.express as px
#from sqlalchemy import create_engine
import psycopg2 as ps
#import pandas as pd
#import pyodbc


# Parameters of database :
colors = {
    #'background': '#111111',
    #'text': '#7FDBFF'
    'background': '#fafafa',
    'text': '#7FDBFF',
    'color': '#333333'
}


# conection to DB
host = '157.230.55.87'
port = 5432
user = 'postgres'
database = 'AMVA'

try:
    #conn = ps.connect(host=host,database=database,user=user,password=password,port=port)
    conn = ps.connect(host=host,database=database,user=user,port=port)
except ps.OperationalError as e:
    raise e
else:
    print('Connected!')

SQL_Query = pd.read_sql('SELECT * FROM eventosmodelo LIMIT 100', conn)
# charts
scatter = px.scatter(SQL_Query, x='longitud', y='latitud')

#### ------------- application

app = dash.Dash(__name__
, external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

# CONTROLS:

 # define visual objects and styles
sidebar = html.Div(
    [
        html.H5('FILTROS AVANZADOS'),
        #controls,
        dcc.DatePickerRange(id='date_picker1', min_date_allowed=date(2019,11,1),
                    max_date_allowed=date(2019,11,30),initial_visible_month =date(2019,11,1),
                    minimum_nights = 0),
        dcc.Input(id='input_hour1',type='text', placeholder='Start hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
        dcc.Input(id='output_hour1',type='text', placeholder='End hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
        html.Button(id= 'date_button1', n_clicks=0, children = 'Process')
    ],
)

# banner object
nav = dbc.Navbar(
         [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # Change App Name here
                        dbc.Col(html.Img(src=app.get_asset_url('logo5.png'), height="120px")),
                        dbc.Col(dbc.NavbarBrand("DASHBOARD AMVA", className = "ml-2" )),
                    ],
                    align="center",
                    no_gutters=True,
            ),
            href="https://plot.ly",
        ),
#        dbc.NavbarToggler(id="navbar-toggler"),
#        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

# intro div
intro = html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("INTRODUCCIÓN", style={
                                        "color": "#15283F"}),

                                    html.P(
                                        "\
                                    El transporte público es un servicio vital para una ciudad, ya que permite a sus ciudadanos desplazarse,  viajar y desarrollar la economía de la ciudad. Además, se ha trabajado mucho en el diseño de un sistema  de transporte inclusivo, eficiente y sostenible. Sin embargo, ha habido una falta de coordinación de las  diferentes partes interesadas y hay una falta de datos confiables para los tomadores de decisiones. Las  partes interesadas del sistema de transporte pueden incluir: gobierno, autoridades de tránsito, empresas    propietarias de autobuses, formuladores de políticas, fabricantes de autobuses, conductores, usuarios,  etc. Pueden tener diferentes intereses y percepciones sobre cómo debería ser un sistema de transporte                                       público y una metodología sistemática para la evaluación de los principales factores de servicio no está                                     disponible, más aún cuando los datos están disponibles, pero son diversos, dispersos y no confiables. El                                     Centro de Operaciones de Transporte Público (GTPC) reconoce que hasta el 40% de los datos capturados                                         para el sistema operativo diario tienen problemas de calidad. Los datos de baja calidad no son adecuados                                     para alimentar el sistema operativo ni utilizarse para el modelado de predicciones, la planificación de                                     rutas óptimas o para la toma de decisiones.",
                                        style={"color": "#15283f"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    )
#id="imagen-intro",
imagen = html.Div([html.A(children=[
                                html.Img(src=app.get_asset_url("banner.jpg"),
                                         style={
                'height': '90%',
                'width': '90%'
            })
                            ],
                         )
], style={'textAlign': 'center'})

#OUR TEAM
# intro div
NOSOTROS = html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("NUESTRO EQUIPO", style={
                                        "color": "#15283F"}),

                                    html.P(
                                        "\
                                    Contamos con el mejor talento de Científicos de Datos certificados con Honores por el Ministerio de Tecnologías de la Información y Comunicaciones (MINTIC). Somos Expertos en la generación de soluciones de Negocio, aplicamos alternativas basadas en Inteligencia Artificial, expertos en bases de datos, integración de herramientas y metodologías tecnologicas para un mejor desarrollo y sostenibilidad del país. Somos tu mejor Opción :)" ,
                                        style={"color": "#15283f"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    )
#id="imagen-intro",
EQUITEAM = html.Div([html.A(children=[
                                html.Img(src=app.get_asset_url("TEAM.png"),
                                         style={
                'height': '100%',
                'width': '100%'
            })
                            ],
                         )
], style={'textAlign': 'center'})









# GRAPHS
graph1 = dcc.Graph(figure=scatter, id='scatter')
graph2 = dash_table.DataTable(id='table',
                     columns =[{'name':i, 'id':i} for i in SQL_Query.columns],
                     data=SQL_Query.head(5).to_dict('records'))
graph3 = dcc.Graph(
        id='example-graph_2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                },
                'title': 'Dash Data Visualization'
            }
        }
    )

content_first_row = dbc.Row(dbc.Col(''))

content_second_row = dbc.Row(dbc.Col(intro,md=12))

content_third_row = dbc.Row([

    dbc.Col(
    dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='TITL', children=['# RUTAS'], className='card-title'),
                        html.P(id='card_text_1', children=[str(SQL_Query['latitud'].mean())]),
                    ]
                )
            ], color="primary", inverse=True
        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('# EMPRESAS', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ] ,color="primary", inverse=True

        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# BACH', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ] ,    color="primary", inverse=True

        ),
        md=2
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# LINEA', className='card-title'),
                        html.P('Sample text.'),
                    ]
                )
            ],    color="primary", inverse=True
        ),
        md=2
    )
])

content_fourth_row = dbc.Row(
    [

        dbc.Col(
            dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)

content_fifth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_sixth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

tabs = dbc.Tabs(
    [
        dbc.Tab([content_second_row, imagen], label="QUIENES SOMOS"),
        dbc.Tab([NOSOTROS, EQUITEAM], label="NUESTRO EQUIPO"),
        dbc.Tab([html.Hr(),
                 sidebar,
                 html.Hr(),
                 content_third_row,
                 html.Hr(),
                 content_fifth_row,
                 html.Hr(),
                 content_sixth_row,
                 html.Hr(),
                 content_fourth_row], label="EDA")
    ]
)

content = html.Div(
    [
        #html.H2('Analytics Dashboard', style=TEXT_STYLE),
        #html.Hr(),
        html.Div(content_first_row), # BANNER
        html.Hr(),
        html.Div(tabs),
        #html.Hr(className="myHr"),
        #html.Div(content_third_row),
        #html.Hr(),
        #html.Div(content_fifth_row),
        #html.Hr(),
        #html.Div(content_sixth_row),
        #html.Hr(),
        #html.Div(content_fourth_row)
    ],
)

#### layout
app.layout = html.Div(children=[nav,
                                content,


#html.Br([]),
html.H5("EXPLORACIÓN DE DATOS"),

#graph1,


#html.Br([]),
#html.H5("RUTAS REPORTADAS"),

#graph2,

#html.Br([]),

#html.H5("MAPEO"),

#graph3,

html.Div(id='output_date')
], id='layout')



#### Interactividad




#### Initiate server where app will work
if __name__ == '__main__':
    app.run_server(debug=True)
