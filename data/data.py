from data.transform import *
import dash_bootstrap_components as dbc
from layout.charts import *
from dash import html,dcc, callback, Output,Input
pd.options.mode.copy_on_write = True 

#_____________________________________________________________
# #data
data = import_transform_data()
#
dic_ind = update_indicators(data)
