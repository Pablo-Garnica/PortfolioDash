from components.components import DashNavBar,DashAvatar,DashModal
import dash_bootstrap_components as dbc
from layout.nav import nav
from layout.info import info
from layout.filters import filtro
# #______________________________________________________________________________
#Modal
modal = DashModal(
    filter=filtro,
    info=info,
    nav=nav
    )
#_____________________________________________________________________________________
#Avatar 
name = "Usuario Prueba"
ls=[
    [
    dbc.Button("Prueba 1",style={'border-radius':'0px','border': '0'},color="light"),
    dbc.Button("Prueba 2",style={'border-radius':'0px','border': '0'},color="light"),
    dbc.Button("Prueba 3",style={'border-radius':'0px','border': '0'},color="light"),
    ],
]
avatar = DashAvatar(name_user=name,ls_button=ls)
#_____________________________________________________________________________________
#NavBar
nombre_app = "Popular Spotify Songs"
logo_app = "https://m.media-amazon.com/images/I/51rttY7a+9L.png"
#
navbar = DashNavBar(nombre_app,logo_app,modal,avatar)
#_____________________________________________________________________________________