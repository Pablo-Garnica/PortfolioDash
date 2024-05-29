import dash_treeview_antd
from dash import html, Output, Input, State, callback

from components.components import DashComponent

rute = {'title': 'Dash','key': 'Dash'}
tree = html.Div([
    dash_treeview_antd.TreeView(
        id='nav-input',
        multiple=False,
        checkable=False,
        checked=['0-0-1'],
        selected=[],
        expanded=['0'],
        data=rute
    ),
    html.Div(id='output-selected'),
])
def get_callback(app):
  #_________________________________________________________________________________
  @app.callback(Output('output-selected', 'children'),
                [Input('nav-input', 'selected')])
  def _display_selected(selected):
      sel = '' if len(selected) ==0 else selected[0]
      return f'You have checked {sel}'
  #_________________________________________________________________________________
  return


nav = DashComponent(
   name='modal_nav',
   layout=tree,
   callback=get_callback
)
