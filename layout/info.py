from dash import html
from components.components import DashComponent
info_message ='''
    Para construir este dashboard se tiene como fuende de información Popular_Spotify_Songs, la cual fue descargada del siguiente link de kaggle:
'''
info_component = html.Div(
    children=[
        html.Br(),
        html.Div(
            [
                info_message,
                html.A('https://www.kaggle.com/datasets/zeesolver/spotfy',href='https://www.kaggle.com/datasets/zeesolver/spotfy'),
             ]),
        html.Br(),
        html.Ol(
            children=[
                html.Li('El componente Avatar esta pensado para que en un futuro se agreguen opciones de seión que aun no se tienen'),
                html.Li('La componente Navegación en el modal se tiene pensada para poder navegar entre paginas, en esta versión es una aplicación de solo una pagina'),
                html.Li('Proximamente se buscará una forma para hacer un filtro cruzado con los graficos de plotly'),
                html.Li('Proximamente se buscará una forma para hacer la interactividad y el centro de datos de forma organizada (Con una POO)'),
                html.Li('Proximamente se buscará una forma para la construccion de graficos de forma organizada (Con una POO)'),
                html.Li('Proximamente se modularizara los indicadores'),
            ]
        )
    ],
    )

info = DashComponent(
    name='modal_info',
    layout=info_component,
)
