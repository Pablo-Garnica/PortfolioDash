from dash import Dash, html
import dash_bootstrap_components as dbc
#Boton de herramientas
from layout.navBar import navbar
from layout.layout import card,graphs

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],)
app.title = 'Popular Spotify Songs'
server = app.server
#_________________________________________________________________________________________
#Modal
navbar.get_callback()(app)
#_________________________________________________________________________________________
# Layout
app.layout = html.Div([
    html.Div([
        card,
        graphs,
    ],
    style={'margin-top': '65px',}
        ),
    navbar.get_layout(),
    ],
)
#Iniciar la aplicacion
if __name__ == '__main__':
    app.config.suppress_callback_exceptions=True
    app.run(debug=True)

