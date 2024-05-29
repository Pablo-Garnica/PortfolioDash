import plotly.graph_objects as go
from datetime import date

def bar_label_h(df_col_label,df_col_value,color= '#48937E'):
    fig = go.Figure(
        data=go.Bar(
                x=df_col_value,
                marker_color = color,
            ),
        layout={
            'bargroupgap':0.4, 
            'yaxis':{'visible': False,},
            'xaxis':{'visible': False},
            'barcornerradius':5,
            'margin' : {'l':0,'r':0,'t':0,'b':0},
        })
    df_col_value = df_col_value.map('{:,.0f}'.format)
    label = df_col_label + ": " + df_col_value

    for idx, name in enumerate(label):
        fig.add_annotation(
            x=0,
            y=idx + 0.45,
            text=name,
            xanchor='left',
            showarrow=False,
            yshift=0
        )
    return fig

def line_interval(x,y,min_x=None,max_x=None):
    r_min = x.min() if min_x==None else date.fromisoformat(min_x)
    r_max = x.max() if max_x==None else date.fromisoformat(max_x)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        text= y,
        textposition='top center',
        textfont=dict(color='#000000'),
        line_color='rgb(0,100,80)',
    ))
    fig.update_layout(
        xaxis = {'range':[r_min,r_max]},
        yaxis = {'visible': False,},
        margin = {'l':0,'r':0,'t':0,'b':0},
        paper_bgcolor='#E5ECF6',
        plot_bgcolor='#E5ECF6'
    )
    fig.update_traces(mode='lines+text')
    return fig