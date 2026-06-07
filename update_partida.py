import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import mysql.connector
import pandas as pd
from datetime import datetime  # <-- Importação necessária para conversão de datas
import os
from dotenv import load_dotenv

load_dotenv()

# 1. CONFIGURAÇÃO DE CONEXÃO
def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",                  
        password=os.getenv("DB_PASSWORD", "1234"),
        database="Copa do Mundo de Futebol"
    )

# Funções auxiliares para alimentar a interface
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


# 2. INICIALIZAÇÃO
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


# 3. LAYOUT
app.layout = dbc.Container([
    # Topbar igual ao seu protótipo
    dbc.NavbarSimple(
        brand="Copa SQL", brand_href="#", color="#ffffff", dark=False, className="mb-4 shadow-sm",
        children=[dbc.NavLink("Partidas", href="#", active=True, style={'color': '#10b981', 'fontWeight': 'bold'})]
    ),

    # Título
    html.Div([
        html.H2("Atualização de Partida", style={'fontWeight': 'bold', 'color': '#1e1b4b'}),
        html.P("Selecione uma partida existente para modificar seus dados no banco central.", style={'color': '#6b7280'})
    ], className="mb-4"),

    # Formulário
    dbc.Card([
        dbc.CardBody([
            
            # Seleção da partida que será editada
            dbc.Row([
                dbc.Col([
                    html.Label("Selecione a Partida para Editar", style={'fontWeight': 'bold', 'color': '#1e1b4b'}),
                    dcc.Dropdown(
                        id='dropdown-partida-selecionada',
                        placeholder='Escolha o confronto que deseja alterar...',
                        options=buscar_opcoes_partidas()
                    )
                ], width=12, className="mb-4")
            ]),

            html.Hr(),

            # Dados que serão atualizados
            dbc.Row([
                dbc.Col([
                    html.Label("Data da Partida", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dcc.DatePickerSingle(
                        id='data-partida', 
                        placeholder='DD/MM/AAAA',
                        className='w-100', 
                        display_format='DD/MM/YYYY'
                    )
                ], width=6, className="mb-3"),
                
                dbc.Col([
                    html.Label("Estádio", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dcc.Dropdown(id='dropdown-estadio', placeholder='Selecione o local', options=buscar_opcoes_estadios())
                ], width=6, className="mb-3"),
            ]),

            dbc.Row([
                dbc.Col([
                    html.Label("Time 1 (Mandante)", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dcc.Dropdown(id='dropdown-time1', placeholder='Selecione o país', options=buscar_opcoes_selecoes())
                ], width=6, className="mb-3"),
                
                dbc.Col([
                    html.Label("Time 2 (Visitante)", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dcc.Dropdown(id='dropdown-time2', placeholder='Selecione o país', options=buscar_opcoes_selecoes())
                ], width=6, className="mb-3"),
            ]),

            dbc.Row([
                dbc.Col([
                    html.Label("Quantidade de gols Time 1", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dbc.Input(id='gols-time1', type='number', value=0)
                ], width=6, className="mb-3"),
                
                dbc.Col([
                    html.Label("Quantidade de gols Time 2", style={'fontFamily': 'monospace', 'fontSize': '12px'}),
                    dbc.Input(id='gols-time2', type='number', value=0)
                ], width=6, className="mb-3"),
            ]),

            html.Hr(className="my-4"),

            html.Div([
                dbc.Button("Cancelar", color="light", className="me-2"),
                dbc.Button("Salvar Alterações", id="btn-atualizar", color="success", style={'backgroundColor': '#00c853', 'border': 'none'})
            ], style={'textAlign': 'right'})

        ])
    ], style={'borderRadius': '12px', 'backgroundColor': '#fcfcfd'}, className="p-3 shadow-sm"),
    
    html.Div(id='notificacao-banco', className="mt-3"),
    
    html.Hr(className="my-5"),
    html.H4("📋 Confrontos Atualizados", style={'fontWeight': 'bold'}),
    html.Div(id='tabela-historico-partidas')

], fluid=False, style={'maxWidth': '900px'})


# 4. CALLBACK 1: CARREGAR DADOS DO JOGO SELECIONADO NOS CAMPOS
@app.callback(
    [Output('data-partida', 'date'),
     Output('dropdown-estadio', 'value'),
     Output('dropdown-time1', 'value'),
     Output('dropdown-time2', 'value'),
     Output('gols-time1', 'value'),
     Output('gols-time2', 'value')],
    Input('dropdown-partida-selecionada', 'value'),
    prevent_initial_call=True
)
def carregar_dados_no_formulario(id_partida):
    if id_partida is None:
        return None, None, None, None, 0, 0
    
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT data_partida, id_estadio, id_selecao_1, id_selecao_2, quantidade_gols_selecao_1, quantidade_gols_selecao_2 FROM `Copa do Mundo de Futebol`.`Partidas` WHERE id_partida = %s", (id_partida,))
    dados = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if dados:
        return str(dados[0]), dados[1], dados[2], dados[3], dados[4], dados[5]
    return None, None, None, None, 0, 0


# 5. CALLBACK 2: EXECUTAR O COMANDO UPDATE NO BANCO
@app.callback(
    [Output('notificacao-banco', 'children'),
     Output('dropdown-partida-selecionada', 'options')],
    Input('btn-atualizar', 'n_clicks'),
    [State('dropdown-partida-selecionada', 'value'),
     State('data-partida', 'date'),
     State('dropdown-estadio', 'value'),
     State('dropdown-time1', 'value'),
     State('dropdown-time2', 'value'),
     State('gols-time1', 'value'),
     State('gols-time2', 'value')],
    prevent_initial_call=True
)
def atualizar_partida(n_clicks, id_partida, data, id_estadio, id_time1, id_time2, gols_t1, gols_t2):
    if not id_partida:
        return dbc.Alert("⚠️ Selecione uma partida no topo antes de tentar salvar.", color="warning"), buscar_opcoes_partidas()
    if not data or id_estadio is None or id_time1 is None or id_time2 is None:
        return dbc.Alert("⚠️ Preencha todos os campos.", color="warning"), buscar_opcoes_partidas()
    if id_time1 == id_time2:
        return dbc.Alert("❌ Regra de Negócio: O Time 1 não pode jogar contra si mesmo.", color="danger"), buscar_opcoes_partidas()

    try:
        # Lógica do Vencedor
        if int(gols_t1) > int(gols_t2): vencedor = id_time1
        elif int(gols_t2) > int(gols_t1): vencedor = id_time2
        else: vencedor = None

        conn = obter_conexao()
        cursor = conn.cursor()
        
        # COMANDO SQL UPDATE
        sql = """
            UPDATE `Copa do Mundo de Futebol`.`Partidas`
            SET data_partida = %s, id_estadio = %s, id_selecao_1 = %s, id_selecao_2 = %s, 
                quantidade_gols_selecao_1 = %s, quantidade_gols_selecao_2 = %s, vencedor = %s
            WHERE id_partida = %s
        """
        valores = (data, id_estadio, id_time1, id_time2, gols_t1, gols_t2, vencedor, id_partida)
        
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()

        alerta = dbc.Alert(f"🔄 Partida {id_partida} atualizada com sucesso no MySQL!", color="success")
        return alerta, buscar_opcoes_partidas()

    except mysql.connector.Error as err:
        return dbc.Alert(f"❌ Erro MySQL: {err.msg}", color="danger"), buscar_opcoes_partidas()


# CALLBACK 3: RENDERIZAR A TABELA ATUALIZADA
@app.callback(
    Output('tabela-historico-partidas', 'children'),
    Input('notificacao-banco', 'children')
)
def atualizar_tabela_historico(notificacao):
    try:
        conn = obter_conexao()
        query = """
            SELECT p.id_partida AS 'ID', 
                   DATE_FORMAT(p.data_partida, '%d/%m/%Y') AS 'Data', 
                   est.nome_estadio AS 'Estádio',
                   sel1.nome_selecao AS 'Mandante', p.quantidade_gols_selecao_1 AS 'Gols T1',
                   p.quantidade_gols_selecao_2 AS 'Gols T2', sel2.nome_selecao AS 'Visitante',
                   COALESCE(sel_venc.nome_selecao, 'Empate') AS 'Vencedor'
            FROM `Copa do Mundo de Futebol`.`Partidas` p
            JOIN `Copa do Mundo de Futebol`.`Estadios` est ON p.id_estadio = est.id_estadios
            JOIN `Copa do Mundo de Futebol`.`Selecoes` sel1 ON p.id_selecao_1 = sel1.id_selecoes
            JOIN `Copa do Mundo de Futebol`.`Selecoes` sel2 ON p.id_selecao_2 = sel2.id_selecoes
            LEFT JOIN `Copa do Mundo de Futebol`.`Selecoes` sel_venc ON p.vencedor = sel_venc.id_selecoes
            ORDER BY p.id_partida DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, className="text-center shadow-sm bg-white")
    except:
        return html.P("Erro ao carregar dados.")


if __name__ == '__main__':
    app.run(debug=True)