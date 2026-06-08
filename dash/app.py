import dash
from dash import State, dcc, html, Input, Output, ctx
from dash.exceptions import PreventUpdate

from home.home import tela_home
from jogadores.tela_jogadores import tela_jogadores
from jogadores.callbacks_jogadores import registrar_callbacks as registrar_callbacks_jogadores
from jogadores.callbacks_UPDATE_jogadores import registrar_callbacks as registrar_callbacks_editar_jogador
import dash_bootstrap_components as dbc
from partidas.layout_partidas import layout_partidas_container
from partidas.callbacks_partidas import registrar_callbacks as registrar_callbacks_partidas


from jogadores.main_jogadores import tela_principal_jogadores
#dash define que só irá procurar imagens em folders img
app = dash.Dash(__name__, title="Copa SQL", assets_folder='img', assets_url_path='/img/',external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


app = dash.Dash(
    __name__, title="Copa SQL",
    assets_folder='img', assets_url_path='/img/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

estilo_botao_padrao = {
    'background': 'none', 'border': 'none', 'cursor': 'pointer',
    'color': '#4b5563', 'fontWeight': 'bold', 'fontSize': '14px'
}
estilo_botao_ativo = {**estilo_botao_padrao, 'color': '#15803d', 'borderBottom': '3px solid #15803d'}

app.layout = html.Div([

    dcc.Store(id='pagina-atual-store', data='home'),
    dcc.Store(id='filtered-data-store'),
    dcc.Store(id='jogador-editando-id', data=None),
    dcc.Store(id='jogadores-pagina-atual', data=1),

    # HEADER
    html.Div([
        html.Div([
            html.Img(src='/img/logo.svg', style={'height': '50px', 'width': 'auto'}),
            html.H1("Copa SQL", style={'margin': '0', 'color': "#064e3b", 'fontWeight': '1000'}),
        ], style={'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.Button('Home',          id='btn-home',       n_clicks=0, style=estilo_botao_ativo),
            html.Button('Dashboards',    id='btn-dashboards', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Documentation', id='btn-docs',       n_clicks=0, style=estilo_botao_padrao),
            html.Button('Seleções',      id='btn-selecoes',   n_clicks=0, style=estilo_botao_padrao),
            html.Button('Estádios',      id='btn-estadios',   n_clicks=0, style=estilo_botao_padrao),
            html.Button('Jogadores',     id='btn-jogadores',  n_clicks=0, style=estilo_botao_padrao),
            html.Button('Partidas',      id='btn-partidas',   n_clicks=0, style=estilo_botao_padrao),
        ], style={'display': 'flex', 'gap': '20px'})

    ], style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '20px 5%', 'backgroundColor': '#ffffff', 'borderBottom': '1px solid #eaeaea'
    }),

    html.Div(id='page-content', style={'margin': '0', 'padding': '0', 'width': '100%'})

], style={'margin': '0', 'padding': '0', 'backgroundColor': '#f9fafb', 'minHeight': '100vh'})


BOTOES_MENU = ['btn-home', 'btn-dashboards', 'btn-docs',
               'btn-selecoes', 'btn-estadios', 'btn-jogadores', 'btn-partidas']

@app.callback(
    Output('pagina-atual-store', 'data'),
    Input('btn-home',       'n_clicks'),
    Input('btn-dashboards', 'n_clicks'),
    Input('btn-docs',       'n_clicks'),
    Input('btn-selecoes',   'n_clicks'),
    Input('btn-estadios',   'n_clicks'),
    Input('btn-jogadores',  'n_clicks'),
    Input('btn-partidas',   'n_clicks'),
    prevent_initial_call=True
)
def atualizar_rota(b1, b2, b3, b4, b5, b6, b7):
    mapa = {
        'btn-home': 'home', 'btn-dashboards': 'dashboards',
        'btn-docs': 'docs', 'btn-selecoes': 'selecoes',
        'btn-estadios': 'estadios', 'btn-jogadores': 'jogadores',
        'btn-partidas': 'partidas',
    }
    return mapa.get(ctx.triggered_id, 'home')


@app.callback(
    Output('page-content', 'children'),
    Input('pagina-atual-store', 'data'),
    prevent_initial_call=False
)
def renderizar_pagina(pagina):
    if pagina == 'jogadores':  return tela_principal_jogadores
    if pagina == 'dashboards': return html.H1("2")
    if pagina == 'docs':       return html.H1("3")
    if pagina == 'selecoes':   return html.H1("4")
    if pagina == 'estadios':   return html.H1("5")
    if pagina == 'partidas':   return html.H1("7")
    return tela_home


registrar_callbacks_jogadores(app)
registrar_callbacks_editar_jogador(app)

if __name__ == '__main__':
    app.run(debug=True)