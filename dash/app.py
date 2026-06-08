import dash
from dash import dcc, html, Input, Output, ctx

from home.home import tela_home
from jogadores.callbacks_UPDATE_jogadores import registrar_callbacks as registrar_callbacks_editar_jogador
from jogadores.callbacks_jogadores import registrar_callbacks as registrar_callbacks_jogadores
from jogadores.main_jogadores import tela_principal_jogadores
from partidas.callbacks_partidas import registrar_callbacks as registrar_callbacks_partidas
from partidas.layout_partidas import layout_partidas_container
from selecoes.callbacks_atualizar_selecoes import registrar_callbacks as registrar_callbacks_atualizar_selecoes
from selecoes.callbacks_selecoes import registrar_callbacks as registrar_callbacks_selecoes
from selecoes.tela_atualizar_selecoes import tela_selecoes as tela_atualizar_selecoes
from selecoes.tela_cadastro_selecao import tela_cadastro_selecao
from selecoes.tela_selecoes import tela_selecoes
import dash_bootstrap_components as dbc
from estadios.tela_atualizar_estadios import tela_estadios as tela_atualizar_estadios
from estadios.callbacks_atualizar_estadios import registrar_callbacks as registrar_callbacks_atualizar_estadios

app = dash.Dash(
    __name__, title="Copa SQL",
    assets_folder='img', assets_url_path='/img/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

estilo_botao_padrao = {
    'background': 'none', 'border': 'none', 'cursor': 'pointer',
    'color': '#4b5563', 'fontWeight': 'bold', 'fontSize': '14px'
}
estilo_botao_ativo = {**estilo_botao_padrao, 'color': '#15803d', 'borderBottom': '3px solid #15803d'}

PAGINAS = {
    'home': tela_home,
    'selecoes': tela_selecoes,
    'atualizar-selecoes': tela_atualizar_selecoes,
    'cadastro-selecao': tela_cadastro_selecao,
    'estadios': tela_atualizar_estadios,
    'jogadores': tela_principal_jogadores,
    'partidas': layout_partidas_container,
}

app.layout = html.Div([

    dcc.Store(id='filtered-data-store'),
    dcc.Store(id='nav-store', data='home'),
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


@app.callback(
    Output('nav-store', 'data'),
    Input('btn-home', 'n_clicks'),
    Input('btn-dashboards', 'n_clicks'),
    Input('btn-docs', 'n_clicks'),
    Input('btn-selecoes', 'n_clicks'),
    Input('btn-estadios', 'n_clicks'),
    Input('btn-jogadores', 'n_clicks'),
    Input('btn-partidas', 'n_clicks'),
    prevent_initial_call=True,
)
def atualizar_rota(b1, b2, b3, b4, b5, b6, b7):
    mapa = {
        'btn-home': 'home',
        'btn-dashboards': 'dashboards',
        'btn-docs': 'docs',
        'btn-selecoes': 'selecoes',
        'btn-estadios': 'estadios',
        'btn-jogadores': 'jogadores',
        'btn-partidas': 'partidas',
    }
    return mapa.get(ctx.triggered_id, 'home')

@app.callback(
    Output('page-content', 'children'),
    Input('nav-store', 'data'),
    prevent_initial_call=False,
)
def renderizar_pagina(pagina):
    if pagina == 'dashboards':
        return html.H1("2")
    if pagina == 'docs':
        return html.H1("3")
    return PAGINAS.get(pagina, tela_home)


registrar_callbacks_jogadores(app)
registrar_callbacks_atualizar_selecoes(app)
registrar_callbacks_atualizar_estadios(app)
registrar_callbacks_editar_jogador(app)
registrar_callbacks_selecoes(app)
registrar_callbacks_partidas(app)

if __name__ == '__main__':
    app.run(debug=True)
