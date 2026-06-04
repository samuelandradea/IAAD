from dash import html
from partidas.tela_partidas import tela_partidas
from partidas.tela_cadastro import tela_cadastro


layout_partidas_container = html.Div([
    html.Div(id='container-lista-partidas', children=tela_partidas, style={'display': 'block'}),
    html.Div(id='container-cadastro-partida', children=tela_cadastro, style={'display': 'none'})
])
