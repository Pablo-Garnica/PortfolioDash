from components.components import DashCard
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from data.data import dic_ind

icon = html.I(className="bi bi-music-note-beamed")
ls_card = []
for key in dic_ind.keys():
    value_indicator=html.Div( 
        children=[
            html.Div(
            id=f'card-value-{key}',
            style={
                'font-weight': 'bolder',
                'font-size':'large',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            }),
            dbc.Progress(
                id=f'card-progress-{key}',
                color ='#0B8316',
                style={
                    'height': '5px',
                    'background': '#D9D9D9 ',
                }
                )
        ],
        style={
            'width':'100%',
            'padding':'0px'
        }
    )
    body_style = {
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
    }

    card_style = {
        'width':'130px',
        "--bs-card-border-color": "black"
    }
    card = DashCard(
        header_layout=[
            icon,
            html.Div(key.split('_')[0].title()),
            ],
        header_style={
            'background-color':'#003086',
            'color':'white'
            },
        body_layout=value_indicator,
        body_style=body_style,
        card_style=card_style,
    )
    ls_card = ls_card + [card]

ls_card_layout = [card.get_layout() for card in ls_card]

card = dbc.Card(
        dbc.CardBody(
            ls_card_layout,
            style={
                'display': 'flex',
                'justify-content': 'space-around',
            }
            ),
        style={
                'margin':'10px',
                'background-color':'#E5ECF6',
            }
)

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    children=dbc.Card(
                            children=[
                                html.Div(
                                    children ='Top 10 Track populares',
                                    style={
                                        'font-weight': 'bolder',
                                        'font-size': '20px',
                                        'text-align': 'center',
                                    }
                                    ),
                                dcc.Graph(id='graph-track'),
                            ],
                        style={'background-color':'#E5ECF6',}
                        ),                        
                    style={
                        'width':'50%',
                        'padding':'12px',
                    }
                ),
                dbc.Col(
                    dbc.Card(
                        children=[
                            html.Div(
                                children ='Top 10 artistas populares',
                                style={
                                    'font-weight': 'bolder',
                                    'font-size': '20px',
                                    'text-align': 'center',
                                }
                                ),    
                            dcc.Graph(id='graph-artist'),
                        ],
                        style={'background-color':'#E5ECF6',}
                    ),
                    style={
                        'width':'50%',
                        'padding':'12px',
                        },
                ),
            ],
            style={'margin':'0px',},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        children = [
                                html.Div(
                                    children ='Comparación playlist',
                                    style={
                                        'font-weight': 'bolder',
                                        'font-size': '20px',
                                        'text-align': 'center',
                                    }
                                    ),
                                dcc.Graph(id='graph-playlist'),
                        ],
                        style={'background-color':'#E5ECF6',}
                    ),
                    style={
                        'width':'50%',
                        'padding':'12px',
                        },
                ),
                dbc.Col(
                    dbc.Card(
                        children=[
                            html.Div(
                                children ='Comparación charts',
                                style={
                                    'font-weight': 'bolder',
                                    'font-size': '20px',
                                    'text-align': 'center',
                                }
                                ),
                            dcc.Graph(id='graph-charts'),
                        ],
                        style={'background-color':'#E5ECF6',}
                    ),
                    style={
                        'width':'50%',
                        'padding':'12px',
                        },
                ),
            ],
            style={'margin':'0px',},
        ),
        dbc.Row(dbc.Col(
            dbc.Card(
                children = [
                    html.Div(
                        children ='Tendencia mes de realización',
                        style={
                            'font-weight': 'bolder',
                            'font-size': '20px',
                            'text-align': 'center',
                        }
                        ),
                    dcc.Graph(id='graph-period'),
                ],
                style={'background-color':'#E5ECF6',}
            ),
                    style={
                        'padding':'12px',
                        },
        ),
        style={'margin':'0px',},
        ),
    ]
)