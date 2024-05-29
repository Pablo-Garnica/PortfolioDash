import pandas as pd
#_____________________________________________________________
#Errores
def error_str_to_int(df_column,flg_print=True):    
    ls_error = []
    for i in df_column.unique():
        try:
            int(i)
        except:
            if len(ls_error) <6:
                if flg_print:
                    print(i)
            ls_error = ls_error + [i]
    if flg_print:
        print(f'EL numero de errores es {len(ls_error)}')
    return ls_error
#_____________________________________________________________
def group_agg(df,ls):
    df = df[ls].mean()
    df = pd.DataFrame(data=df).reset_index()
    df.columns = ['type','value']
    return df
#_____________________________________________________________
#_______________________data__________________________________
def import_transform_data():
    data = pd.read_csv('data\Popular_Spotify_Songs.csv',encoding='latin1')
    #Errores
    dic_error = {}
    ls_val = [
        'streams',
        'in_deezer_playlists',
        'in_shazam_charts',
    ]
    for col_name in ls_val:
        ls_error = error_str_to_int(data[col_name],flg_print=False)
        dic_error.update({col_name:ls_error})
    #Alinear tipos
    #Streams
    data = data[~data['streams'].isin(dic_error['streams'])]
    data['streams'] = data['streams'].fillna(0).astype(float)
    #in_shazam_charts
    data['in_shazam_charts'] = data['in_shazam_charts'].str.replace(',','').fillna(0).astype(int)
    #in_deezer_playlists
    data['in_deezer_playlists'] = data['in_deezer_playlists'].str.replace(',','').astype(int)
    #_____________________________________
    #Crear id registro (top)
    data = data.sort_values('streams',ascending=False).reset_index(drop=True)
    data = data.reset_index()
    #Crear el top de canciones
    data = data.rename(columns={'index':'top'})
    data['top'] = data['top'] + 1
    return data
#_____________________________________________________________
#________________________top__________________________________
def update_data_top(data):
    data = data.sort_values('streams',ascending=False).reset_index(drop=True)
    data = data.reset_index()
    data = data.drop(['top'], axis=1)
    # #Crear el top de canciones
    data = data.rename(columns={'index':'top'})
    data['top'] = data['top'] + 1
    data_top = data[data['top']<=10][['streams','track_name']]
    data_top = data_top.sort_values('streams')
    return data_top
#_____________________________________________________________
#________________________artist_______________________________
def update_data_artist(data):
    data_artist = data[['top', 'artist(s)_name']]
    data_artist['artist'] = data_artist['artist(s)_name'].apply(lambda x : x.split(', '))
    data_artist = (
        data_artist[['top', 'artist']]
        .set_index(['top'])['artist']
        .apply(pd.Series)
        .stack()
        .reset_index(level=1, drop=True)
        .reset_index()
        .rename(columns={0:'artist'})
    )
    return data_artist
#_____________________________________________________________
#___________________artist_top10______________________________
def update_top_artist_clean(data_artist):
    top_artist_clean = (
        data_artist
            .groupby('artist',as_index=False)['top'].count()
            .sort_values('top',ascending=False)
            .reset_index(drop=True)
            .head(10)
    )
    top_artist_clean.columns = ['artist_clean','N Popular tracks clean']
    top_artist_clean = top_artist_clean.sort_values('N Popular tracks clean',ascending=True)
    return top_artist_clean
#_____________________________________________________________
#______________________data_period____________________________
def update_data_period(data):
    data['released_period'] = data['released_year'].astype(str) + '/' + data['released_month'].astype(str) + '/01'
    data['released_period'] = pd.to_datetime(data['released_period'],yearfirst=True)
    data_period =data.groupby(['released_period'],as_index=False)['top'].count()
    return data_period
#_____________________________________________________________
#______________________data_charts____________________________
def update_data_charts(data):
    charts = [
        'in_spotify_charts',
        'in_apple_charts',
        'in_deezer_charts',
    ]
    data_charts = group_agg(data,charts)
    data_charts['type'] = data_charts['type'].apply(lambda x : x.split('_')[1])
    data_charts = data_charts.sort_values('value')
    return data_charts
#_____________________________________________________________
#_____________________data_playlist___________________________
def update_data_playlist(data):
    playlist = [
        'in_spotify_playlists',
        'in_apple_playlists',
        'in_deezer_playlists',
        'in_shazam_charts',
    ]
    data_playlist = group_agg(data,playlist)
    data_playlist['type'] = data_playlist['type'].apply(lambda x : x.split('_')[1])
    data_playlist = data_playlist.sort_values('value')
    return data_playlist
#_____________________________________________________________
#________________________indicator____________________________
def update_indicators(data):
    ls_indicator = [
        'danceability_%',
        'valence_%',
        'energy_%',
        'acousticness_%',
        'instrumentalness_%',
        'liveness_%',
        'speechiness_%',
    ]
    dic_ind ={}
    for i in ls_indicator:
        dic_ind.update({i:data[i].mean()})
    return dic_ind