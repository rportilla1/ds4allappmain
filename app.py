import dash
from dash.dependencies import Input, Output, State
from datetime import date
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import plotly.express as px
from sqlalchemy import create_engine
import psycopg2 as ps
import pandas as pd 
import pyodbc


# Parameters of database :
colors = {
    #'background': '#111111',
    #'text': '#7FDBFF'
    'background': '#fafafa',
    'text': '#7FDBFF',
    'color': '#333333'
}

# the style arguments for the sidebar.
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#1E90FF'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#FFFFFF'
}

CARD_TEXT_STYLE = {
    'textAlign': 'justify',
    'color': '#000000'
    'width: 120rem',
}

 


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
scatter = px.scatter(SQL_Query, x='longitud', y='latitud')

#### ------------- application

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# CONTROLS:

     
 # define visual objects and styles
sidebar = html.Div(
    [   
        html.H2('FILTROS AVANZADOS', style=TEXT_STYLE),
        html.Hr(),
        #controls,
        dcc.DatePickerRange(id='date_picker', min_date_allowed=date(2019,11,1),
                    max_date_allowed=date(2019,11,30),initial_visible_month =date(2019,11,1),
                    minimum_nights = 0),
dcc.Input(id='input_hour',type='text', placeholder='Start hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
dcc.Input(id='output_hour',type='text', placeholder='End hour', debounce=True,
          pattern= u'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'),
html.Button(id= 'date_button', n_clicks=0, children = 'Process')
    ],
    style=SIDEBAR_STYLE,
)

# banner object
banner = html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                                                                               
                            id="banner-title",
                            children=[
                                html.A(
                                    "DASHBOARD AMVA",
                                     style={
                                        "text-decoration": "none",
                                        "color": "#FFFFFF",
                                        
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("logo5.png"))
                            ],
                         ),
                    ],
                )
            ],
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

content_first_row = dbc.Row(dbc.Col(banner,md=12))

content_second_row = dbc.Row(dbc.Col(intro,md=12))

content_third_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='TITL', children=['# RUTAS'], className='card-title',
                                style='width: 22rem;'),
                        html.P(id='card_text_1', children=[str(SQL_Query['latitud'].mean())], style=CARD_TEXT_STYLE),
                    ]
                )
            ], color="primary", inverse=True
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('# EMPRESAS', className='card-title', style='width: 22rem;'),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                )
            ] ,color="primary", inverse=True

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# BACH', className='card-title', style='width: 22rem;'),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                )
            ] ,    color="primary", inverse=True

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4('# LINEA', className='card-title', style='width: 22rem;'),
                        html.P('Sample text.', style=CARD_TEXT_STYLE, ),
                    ]
                )
            ],    color="primary", inverse=True
        ),
        md=3
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

content = html.Div(
    [
        #html.H2('Analytics Dashboard', style=TEXT_STYLE),
        #html.Hr(),
        html.Div(content_first_row),
        html.Div(content_second_row),
        html.Hr(className="myHr"),
        html.Div(content_third_row),
        html.Hr(),
        html.Div(content_fifth_row),
        html.Hr(),
        html.Div(content_sixth_row),
        html.Hr(),
        html.Div(content_fourth_row)
    ],
    style=CONTENT_STYLE
)

#### layout
app.layout = html.Div(children=[sidebar,
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
