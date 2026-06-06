import dash
from dash import dcc, html, Input, Output, ctx

from home.home import tela_home
from jogadores.tela_jogadores import  tela_jogadores
from jogadores.callbacks_jogadores import registrar_callbacks as registrar_callbacks_jogadores
import dash_bootstrap_components as dbc
from partidas.layout_partidas import layout_partidas_container
from partidas.callbacks_partidas import registrar_callbacks as registrar_callbacks_partidas

#dash define que só irá procurar imagens em folders img
app = dash.Dash(__name__, title="Copa SQL", assets_folder='img', assets_url_path='/img/',external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)



estilo_botao_padrao = {
    'background': 'none', 'border': 'none', 'cursor': 'pointer',
    'color': '#4b5563', 'fontWeight': 'bold', 'fontSize': '14px'
}


estilo_botao_ativo = estilo_botao_padrao.copy()
estilo_botao_ativo.update({'color': '#15803d', 'borderBottom': '3px solid #15803d'})


app.layout = html.Div([
    
    dcc.Store(id='filtered-data-store'),

    # HEADER 
    html.Div([
        html.Div([
            
            
            html.Img(src='/img/logo.svg', style={'height': '50px', 'width': 'auto'}),
            html.H1("Copa SQL", style={'margin': '0', 'color': "#064e3b", 'fontWeight': '1000'}), 
        ], style={'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            
            html.Button('Home', id='btn-home', n_clicks=0, style=estilo_botao_ativo),
            html.Button('Dashboards', id='btn-dashboards', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Documentation', id='btn-docs', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Seleções', id='btn-selecoes', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Estádios', id='btn-estadios', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Jogadores', id='btn-jogadores', n_clicks=0, style=estilo_botao_padrao),
            html.Button('Partidas', id='btn-partidas', n_clicks=0, style=estilo_botao_padrao),
        ], style={'display': 'flex', 'gap': '20px'}) 

    ], className="header", style={
        'display': 'flex', 
        'justifyContent': 'space-between', 
        'alignItems': 'center', 
        
        'padding': '20px 5%',
        'backgroundColor': '#ffffff',
        'borderBottom': '1px solid #eaeaea'
    }),
    
    
    # Recipiente onde as páginas serão renderizadas
    html.Div(id='page-content', style={'margin': '0', 'padding': '50px', 'width': '100%', 'textAlign': 'center'})
    
], style={'margin': '0', 'padding': '0', 'backgroundColor': '#f9fafb', 'minHeight': '100vh'}) 


# --- INÍCIO DO CALLBACK DE ROTEAMENTO ---
@app.callback(
    Output('page-content', 'children'), 
    [
        
        Input('btn-home', 'n_clicks'),
        Input('btn-dashboards', 'n_clicks'),
        Input('btn-docs', 'n_clicks'),
        Input('btn-selecoes', 'n_clicks'),
        Input('btn-estadios', 'n_clicks'),
        Input('btn-jogadores', 'n_clicks'),
        Input('btn-partidas', 'n_clicks')
    ]
)
def mudar_pagina(b1, b2, b3, b4, b5, b6, b7):
    
    botao_clicado = ctx.triggered_id
    
   
    if botao_clicado == 'btn-dashboards':
        return html.H1("2", style={'color': '#111827', 'fontSize': '100px'})
        
    elif botao_clicado == 'btn-docs':
        return html.H1("3", style={'color': '#111827', 'fontSize': '100px'})

    elif botao_clicado == 'btn-selecoes':
        return html.H1("4", style={'color': '#111827', 'fontSize': '100px'})

    elif botao_clicado == 'btn-estadios':
        return html.H1("5", style={'color': '#111827', 'fontSize': '100px'})
        
    elif botao_clicado == 'btn-jogadores':
        return html.H1(tela_jogadores, style={'color': '#111827', 'fontSize': '100px'})

    elif botao_clicado == 'btn-partidas':
        return layout_partidas_container
        
    else:
        
        return tela_home


registrar_callbacks_jogadores(app)
registrar_callbacks_partidas(app)

if __name__ == '__main__':
    app.run(debug=True)