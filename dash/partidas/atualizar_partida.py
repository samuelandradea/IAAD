from dash import html, dcc
import dash_bootstrap_components as dbc
import mysql.connector
import pandas as pd
import os

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",                  
        password=os.getenv("DB_PASSWORD"),
        database="Copa do Mundo de Futebol"
    )

def buscar_opcoes_partidas():
    try:
        conn = obter_conexao()
        query = """
            SELECT p.id_partida, s1.nome_selecao AS m, s2.nome_selecao AS v 
            FROM `Copa do Mundo de Futebol`.`Partidas` p
            JOIN `Copa do Mundo de Futebol`.`Selecoes` s1 ON p.id_selecao_1 = s1.id_selecoes
            JOIN `Copa do Mundo de Futebol`.`Selecoes` s2 ON p.id_selecao_2 = s2.id_selecoes
            ORDER BY p.id_partida DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return [{'label': f"Partida {row['id_partida']} - {row['m']} x {row['v']}", 'value': row['id_partida']} for _, row in df.iterrows()]
    except:
        return []

def buscar_opcoes_selecoes():
    try:
        conn = obter_conexao()
        df = pd.read_sql("SELECT id_selecoes, nome_selecao FROM `Copa do Mundo de Futebol`.`Selecoes` ORDER BY nome_selecao", conn)
        conn.close()
        return [{'label': row['nome_selecao'], 'value': row['id_selecoes']} for _, row in df.iterrows()]
    except:
        return []

def buscar_opcoes_estadios():
    try:
        conn = obter_conexao()
        df = pd.read_sql("SELECT id_estadios, nome_estadio FROM `Copa do Mundo de Futebol`.`Estadios` ORDER BY nome_estadio", conn)
        conn.close()
        return [{'label': row['nome_estadio'], 'value': row['id_estadios']} for _, row in df.iterrows()]
    except:
        return []

# Layout adaptado fielmente ao visual de "tela_partidas.py"
tela_atualizar_partida = html.Div([
    html.Div([
        html.Div([
            html.H2("Atualização de Partida", style={"fontWeight": "bold", "color": "#111827", "margin": "0 0 5px 0", "textAlign": "left"}),
            html.P("Selecione e modifique os confrontos oficiais da Copa do Mundo FIFA 2026.", style={"color": "#6b7280", "margin": "0", "textAlign": "left"}),
        ]),
        html.Button("← Voltar para Lista", id="btn-voltar-partidas", style={
            "backgroundColor": "#4b5563", "color": "white", "border": "none", 
            "padding": "10px 20px", "borderRadius": "5px", "fontWeight": "bold", "cursor": "pointer"
        })
    ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "30px"}),

    # Card Principal seguindo as cores, bordas e sombras do grupo (#fcfcfd)
    html.Div([
        html.Div([
            html.Label("Selecione a Partida para Editar", style={'fontWeight': 'bold', 'color': '#111827', 'fontSize': '14px'}),
            dcc.Dropdown(
                id='dropdown-partida-selecionada',
                placeholder='Escolha o confronto que deseja alterar...',
                options=buscar_opcoes_partidas(),
                style={"marginTop": "5px"}
            )
        ], style={"marginBottom": "25px"}),

        html.Hr(style={"borderColor": "#eaeaea", "marginBottom": "25px"}),

        dbc.Row([
            dbc.Col([
                html.Label("Data da Partida", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dcc.DatePickerSingle(id='data-partida', placeholder='DD/MM/AAAA', className='w-100', display_format='DD/MM/YYYY')
            ], width=6, style={"marginBottom": "20px"}),
            
            dbc.Col([
                html.Label("Estádio", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dcc.Dropdown(id='atualizar-dropdown-estadio', placeholder='Selecione o local', options=buscar_opcoes_estadios())
            ], width=6, style={"marginBottom": "20px"}),
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Time 1 (Mandante)", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dcc.Dropdown(id='atualizar-dropdown-time1', placeholder='Selecione o país', options=buscar_opcoes_selecoes())
            ], width=6, style={"marginBottom": "20px"}),
            
            dbc.Col([
                html.Label("Time 2 (Visitante)", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dcc.Dropdown(id='atualizar-dropdown-time2', placeholder='Selecione o país', options=buscar_opcoes_selecoes())
            ], width=6, style={"marginBottom": "20px"}),
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Quantidade de gols Time 1", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dbc.Input(id='gols-time1', type='number', value=0, style={"borderRadius": "6px"})
            ], width=6, style={"marginBottom": "20px"}),
            
            dbc.Col([
                html.Label("Quantidade de gols Time 2", style={'color': '#4b5563', 'fontSize': '13px', 'fontWeight': '500'}),
                dbc.Input(id='gols-time2', type='number', value=0, style={"borderRadius": "6px"})
            ], width=6, style={"marginBottom": "20px"}),
        ]),

        html.Hr(style={"borderColor": "#eaeaea", "marginTop": "20px", "marginBottom": "25px"}),

        html.Div([
            html.Button("Salvar Alterações", id="btn-atualizar", style={
                "backgroundColor": "#059669", "color": "white", "border": "none", 
                "padding": "12px 25px", "borderRadius": "5px", "fontWeight": "bold", "cursor": "pointer"
            })
        ], style={'textAlign': 'right'})

    ], style={
        "padding": "30px", "borderRadius": "8px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
        "backgroundColor": "#fcfcfd", "border": "1px solid #eaeaea"
    }),
    
    html.Div(id='notificacao-banco', className="mt-3"),
    
    html.Hr(style={"borderColor": "#eaeaea", "marginTop": "40px", "marginBottom": "25px"}),
    html.H4("📋 Confrontos Atualizados", style={'fontWeight': 'bold', 'color': '#111827', 'textAlign': 'left', 'marginBottom': '15px'}),
    html.Div(id='tabela-historico-partidas')
])