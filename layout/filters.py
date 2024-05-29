from dash import html,dcc, callback, Output,Input
import dash_bootstrap_components as dbc
from layout.charts import bar_label_h,line_interval
import plotly.graph_objects as go
from data.data import data
from data.transform import *

from components.components import DashComponent

import pandas as pd
import plotly.express as px

filtro_modal = html.Div(
    [
        dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(data['track_name'].unique(), id='dropdown-track',multi=True,placeholder="Tracks"),
            ),
            dbc.Col(
                dcc.Dropdown(data['artist(s)_name'].unique(), id='dropdown-artist',multi=True,placeholder="Artista"),
            ),
        ],
        style={
            'padding':'5px'
        }
        ),
        dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(data['mode'].unique(), id='dropdown-mode',placeholder="Modo"),
            ),
            dbc.Col(
                dcc.Dropdown(data['key'].unique(), id='dropdown-key',placeholder="Clave"),
            ),
        ],
        style={
            'padding':'5px'
        }
        ),
    ]
    )

def get_callback(app):
    #_________________________________________________________________________________
    @app.callback(
        [
            # Output('graph-content', 'figure'),
            Output('graph-track', 'figure'),
            Output('graph-artist', 'figure'),
            Output('graph-playlist', 'figure'),
            Output('graph-charts', 'figure'),
            Output('graph-period', 'figure'),
            #
            Output('card-value-danceability_%','children'),
            Output('card-value-valence_%','children'),
            Output('card-value-energy_%','children'),
            Output('card-value-acousticness_%','children'),
            Output('card-value-instrumentalness_%','children'),
            Output('card-value-liveness_%','children'),
            Output('card-value-speechiness_%','children'),
            #
            Output('card-progress-danceability_%','value'),
            Output('card-progress-valence_%','value'),
            Output('card-progress-energy_%','value'),
            Output('card-progress-acousticness_%','value'),
            Output('card-progress-instrumentalness_%','value'),
            Output('card-progress-liveness_%','value'),
            Output('card-progress-speechiness_%','value'),
        ],
        [
            # Input('dropdown-selection', 'value'),
            Input('dropdown-track', 'value'),
            Input('dropdown-artist', 'value'),
            Input('dropdown-mode', 'value'),
            Input('dropdown-key', 'value'),
        ]
    )
    # def update_graph(value,track,artist,mode,key):
    def update_graph(track,artist,mode,key):
        
        # value = [value] if type(value) == str else value
        track = [track] if type(track) == str else track
        artist = [artist] if type(artist) == str else artist
        mode = [mode] if type(mode) == str else mode
        key = [key] if type(key) == str else key
        
        data['true'] = True

        track_cond = data['true'] if (track == None) or (track==[]) else data['track_name'].isin(track)
        artist_cond = data['true'] if (artist == None) or (artist==[]) else data['artist(s)_name'].isin(artist)
        mode_cond = data['true'] if (mode == None) or (mode==[]) else data['mode'].isin(mode)
        key_cond = data['true'] if (key == None) or (key==[]) else data['key'].isin(key)

        data_ = data[track_cond & artist_cond & mode_cond & key_cond]
        if len(data_) == 0:
            f_track = go.Figure()
            f_artist = go.Figure()
            f_playlist = go.Figure()
            f_charts = go.Figure()
            f_period = go.Figure()
            r = (
                #Figuras de
                f_track,
                f_artist,
                f_playlist,
                f_charts,
                f_period,
                #Valor de indicadores con formatos
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                #Valor de indicadores para barra de progreso
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                )
        else:
            data_top = update_data_top(data_)
            #artist
            data_artist = update_data_artist(data_)
            #artist_top10
            top_artist_clean = update_top_artist_clean(data_artist)
            #data_period
            data_period = update_data_period(data_)
            #data_charts
            data_charts = update_data_charts(data_)
            #data_playlist
            data_playlist = update_data_playlist(data_)
            #indicadores
            dic_ind = update_indicators(data_)
            #
            color_platform = {
                'spotify':'#1ED760',
                'deezer':'#A238FF',
                'apple':'#BEBEBE',
                'shazam':'#00ADFF',
            }
            color_playlist =  [color_platform[i] for i in list(data_playlist['type'])]
            color_chart =  [color_platform[i] for i in list(data_charts['type'])]
            #
            f_artist = bar_label_h(top_artist_clean['artist_clean'],top_artist_clean['N Popular tracks clean'],color='#CD0D84')
            f_track = bar_label_h(data_top['track_name'],data_top['streams'])
            f_playlist = bar_label_h(data_playlist['type'],data_playlist['value'],color=color_playlist)
            f_charts = bar_label_h(data_charts['type'],data_charts['value'],color=color_chart)
            f_period = line_interval(data_period['released_period'],data_period['top'],'2020-01-01')
            #Indicadores
            danceability_val = format(dic_ind['danceability_%']/100,".2%")
            valence_val = format(dic_ind['valence_%']/100,".2%")
            energy_val = format(dic_ind['energy_%']/100,".2%")
            acousticness_val = format(dic_ind['acousticness_%']/100,".2%")
            instrumentalness_val = format(dic_ind['instrumentalness_%']/100,".2%")
            liveness_val = format(dic_ind['liveness_%']/100,".2%")
            speechiness_val = format(dic_ind['speechiness_%']/100,".2%")
            #
            r = (
                #Figuras de
                f_track,
                f_artist,
                f_playlist,
                f_charts,
                f_period,
                #Valor de indicadores con formatos
                danceability_val,
                valence_val,
                energy_val,
                acousticness_val,
                instrumentalness_val,
                liveness_val,
                speechiness_val,
                #Valor de indicadores para barra de progreso
                dic_ind['danceability_%'],
                dic_ind['valence_%'],
                dic_ind['energy_%'],
                dic_ind['acousticness_%'],
                dic_ind['instrumentalness_%'],
                dic_ind['liveness_%'],
                dic_ind['speechiness_%'],
                )
        return r
    #_________________________________________________________________________________
    return

filtro = DashComponent(
    name='modal_filtro',
    layout=filtro_modal,
    callback=get_callback
)