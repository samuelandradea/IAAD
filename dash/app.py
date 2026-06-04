import dash
from dash import dcc, html, Input, Output, ctx

from home.home import tela_home
from jogadores.tela_jogadores import tela_jogadores
from jogadores.callbacks_jogadores import registrar_callbacks as registrar_callbacks_jogadores
from selecoes.tela_selecoes import tela_selecoes
from selecoes.tela_cadastro_selecao import tela_cadastro_selecao
from selecoes.callbacks_selecoes import registrar_callbacks as registrar_callbacks_selecoes
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, title="Copa SQL", assets_folder='img', assets_url_path='/img/',
                external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

estilo_botao_padrao = {
    'background': 'none', 'border': 'none', 'cursor': 'pointer',
    'color': '#4b5563', 'fontWeight': 'bold', 'fontSize': '14px'
}

estilo_botao_ativo = estilo_botao_padrao.copy()
estilo_botao_ativo.update({'color': '#15803d', 'borderBottom': '3px solid #15803d'})

PAGINAS = {
    'home':             tela_home,
    'selecoes':         tela_selecoes,
    'cadastro-selecao': tela_cadastro_selecao,
    'jogadores':        tela_jogadores,
}

app.layout = html.Div([

    dcc.Store(id='filtered-data-store'),
    dcc.Store(id='nav-store', data='home'),  # controla qual página exibir

    # HEADER
    html.Div([
        html.Div([
            html.Img(src='/img/logo.svg', style={'height': '50px', 'width': 'auto'}),
            html.H1("Copa SQL", style={'margin': '0', 'color': "#064e3b", 'fontWeight': '1000'}),
        ], style={'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.Button('Home',          id='btn-home',        n_clicks=0, style=estilo_botao_ativo),
            html.Button('Dashboards',    id='btn-dashboards',  n_clicks=0, style=estilo_botao_padrao),
            html.Button('Documentation', id='btn-docs',        n_clicks=0, style=estilo_botao_padrao),
            html.Button('Seleções',      id='btn-selecoes',    n_clicks=0, style=estilo_botao_padrao),
            html.Button('Estádios',      id='btn-estadios',    n_clicks=0, style=estilo_botao_padrao),
            html.Button('Jogadores',     id='btn-jogadores',   n_clicks=0, style=estilo_botao_padrao),
            html.Button('Partidas',      id='btn-partidas',    n_clicks=0, style=estilo_botao_padrao),
        ], style={'display': 'flex', 'gap': '20px'})

    ], className="header", style={
        'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
        'padding': '20px 5%', 'backgroundColor': '#ffffff', 'borderBottom': '1px solid #eaeaea'
    }),

    html.Div(id='page-content', style={'margin': '0', 'padding': '50px', 'width': '100%', 'textAlign': 'center'})

], style={'margin': '0', 'padding': '0', 'backgroundColor': '#f9fafb', 'minHeight': '100vh'})


# Botões do header atualizam o nav-store
@app.callback(
    Output('nav-store', 'data'),
    [
        Input('btn-home',       'n_clicks'),
        Input('btn-dashboards', 'n_clicks'),
        Input('btn-docs',       'n_clicks'),
        Input('btn-selecoes',   'n_clicks'),
        Input('btn-estadios',   'n_clicks'),
        Input('btn-jogadores',  'n_clicks'),
        Input('btn-partidas',   'n_clicks'),
    ],
    prevent_initial_call=True
)
def nav_header(b1, b2, b3, b4, b5, b6, b7):
    mapa = {
        'btn-home':       'home',
        'btn-dashboards': 'dashboards',
        'btn-docs':       'docs',
        'btn-selecoes':   'selecoes',
        'btn-estadios':   'estadios',
        'btn-jogadores':  'jogadores',
        'btn-partidas':   'partidas',
    }
    return mapa.get(ctx.triggered_id or '', 'home')


# nav-store renderiza a página
@app.callback(
    Output('page-content', 'children'),
    Input('nav-store', 'data'),
)
def renderizar_pagina(pagina):
    if pagina == 'dashboards':
        return html.H1("2", style={'color': '#111827', 'fontSize': '100px'})
    elif pagina == 'docs':
        return html.H1("3", style={'color': '#111827', 'fontSize': '100px'})
    elif pagina == 'estadios':
        return html.H1("5", style={'color': '#111827', 'fontSize': '100px'})
    elif pagina == 'partidas':
        return html.H1("7", style={'color': '#111827', 'fontSize': '100px'})
    return PAGINAS.get(pagina, tela_home)


registrar_callbacks_jogadores(app)
registrar_callbacks_selecoes(app)

if __name__ == '__main__':
    app.run(debug=True)
