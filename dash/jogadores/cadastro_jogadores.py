import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, callback
import random
import mysql.connector

import mysql.connector
import random

# Arquivo: backend.py (ou onde está sua lógica de banco)

import mysql.connector
import random

# Importando o seu "middleware" do outro arquivo
from jogadores.validators import tratar_dados_jogador

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Matheusdev#2026",
        database="Copa do Mundo de Futebol"
    )

def cadastrar_jogador_db(nome, posicao, camisa, data_nascimento, nome_selecao):
    conn = obter_conexao()
    cursor = conn.cursor()
    
    try:
        #trigger de tratamento
        nome_formatado, selecao_limpa, camisa_formatada = tratar_dados_jogador(nome, nome_selecao, camisa)

        #mudar o nome da seleção para o ID
        cursor.execute("SELECT id_selecoes FROM Selecoes WHERE LOWER(nome_selecao) = LOWER(%s)", (selecao_limpa,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            return False, f"A seleção '{selecao_limpa}' não foi encontrada! Verifique a ortografia ou cadastre-a primeiro."

        id_selecao_encontrado = resultado[0]

       
        id_aleatorio = random.randint(10000, 999999)
        sql = """
            INSERT INTO Jogadores 
            (id_jogador, nome_jogador, posicao, numero_camisa, data_nascimento, Selecoes_id_selecoes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_aleatorio, nome_formatado, posicao, camisa_formatada, data_nascimento, id_selecao_encontrado)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        return True, f"Sucesso! Atleta '{nome_formatado}' vinculado à seleção '{selecao_limpa}' (ID: {id_aleatorio})."
        
    except mysql.connector.Error as err:
        return False, f"Erro interno no banco de dados: {err.msg}"
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()




estilo_label = {
    'fontFamily': 'monospace', 
    'fontWeight': '600', 
    'color': '#4b5563', 
    'marginBottom': '5px',
    'fontSize': '13px'
}


tela_cadastro_jogadores = html.Div([
    dbc.Container([
        
        
        html.Div([
            html.H2("Cadastro de Jogador", style={'color': '#111827', 'fontWeight': 'bold', 'margin': '0'}),
            html.P("Insira os dados do atleta para indexação no banco de dados oficial da FIFA World Cup 2026.", 
                   style={'color': '#6b7280', 'marginTop': '5px', 'fontSize': '15px'})
        ], style={'marginBottom': '30px'}),
        
        
        dbc.Card([
            dbc.CardBody([
                
                #Nome Completo
                dbc.Row([
                    dbc.Col([
                        html.Label("Nome Completo", style=estilo_label),
                        dbc.Input(id="cadastro-nome", type="text", placeholder="Ex: Vinícius José Paixão de Oliveira Júnior", className="mb-4")
                    ], width=12)
                ]),
                
                # LINHSeleção Nacional e Número da Camisa
                dbc.Row([
                    dbc.Col([
                        html.Label("Seleção Nacional", style=estilo_label),
                        dbc.Input(id="cadastro-selecao", type="text", placeholder="Ex: Brasil", className="mb-4")
                    ], md=6),
                    
                    dbc.Col([
                        html.Label("Número da Camisa", style=estilo_label),
                        dbc.Input(id="cadastro-camisa", type="number", min=1, max=99, placeholder="7", className="mb-4")
                    ], md=6)
                ]),
                
                #Posição e Data de Nascimento
                dbc.Row([
                    dbc.Col([
                        html.Label("Posição", style=estilo_label),
                        dbc.Select(
                            id="cadastro-posicao",
                            options=[
                                {'label': 'Goleiro', 'value': 'Goleiro'},
                                {'label': 'Zagueiro', 'value': 'Zagueiro'},
                                {'label': 'Lateral', 'value': 'Lateral'},
                                {'label': 'Meia', 'value': 'Meia'},
                                {'label': 'Atacante', 'value': 'Atacante'}
                            ],
                            value=None,
                            placeholder="Escolha a posição...",
                            className="mb-4"
                        )
                    ], md=6),
                    
                    dbc.Col([
                        html.Label("Data de Nascimento", style=estilo_label),
                        # O type="date" já cria o calendário automático no formato mm/dd/yyyy
                        dbc.Input(id="cadastro-nascimento", type="date", className="mb-4") 
                    ], md=6)
                ]),
                
               
                html.Hr(style={'margin': '20px 0', 'color': '#d1d5db'}),
                
                # Onde aparecerá a mensagem de sucesso ou erro
                html.Div(id="mensagem-alerta-cadastro"),
                
               
                html.Div([
                    dbc.Button("Cancelar", id="btn-cancelar", color="link", style={'color': '#4b5563', 'textDecoration': 'none', 'fontWeight': '600'}),
                    dbc.Button("👤 Cadastrar Jogador", id="btn-cadastrar-jogador", color="success", 
                               style={'backgroundColor': '#00d26a', 'border': 'none', 'fontWeight': 'bold', 'padding': '8px 20px', 'borderRadius': '6px'})
                ], style={'display': 'flex', 'justifyContent': 'flex-end', 'gap': '15px', 'alignItems': 'center'})
                
            ], style={'padding': '40px'})
            
        ], style={'borderRadius': '12px', 'border': '1px solid #e5e7eb', 'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.05)'})
        
    ], style={'maxWidth': '900px', 'marginTop': '40px'})
])



@callback(
    [Output("mensagem-alerta-cadastro", "children"),
     Output("cadastro-nome", "value"),
     Output("cadastro-selecao", "value"),
     Output("cadastro-camisa", "value"),
     Output("cadastro-posicao", "value"),
     Output("cadastro-nascimento", "value")],
    Input("btn-cadastrar-jogador", "n_clicks"),
    [State("cadastro-nome", "value"),
     State("cadastro-selecao", "value"),
     State("cadastro-camisa", "value"),
     State("cadastro-posicao", "value"),
     State("cadastro-nascimento", "value")],
    prevent_initial_call=True
)
def realizar_cadastro(n_clicks, nome, selecao, camisa, posicao, nascimento):

    #varifica se existe dados vazios
    if not all([nome, selecao, camisa, posicao, nascimento]):
        alerta = dbc.Alert("Atenção: Preencha todos os campos antes de cadastrar.", color="warning", duration=4000)
        
        return alerta, nome, selecao, camisa, posicao, nascimento
    
    #Envia para o MySQL
    sucesso, mensagem = cadastrar_jogador_db(nome, posicao, camisa, nascimento, selecao)
    
    
    if sucesso:
        # DEU CERTO: Alerta Verde e limpa os campos 
        alerta = dbc.Alert(mensagem, color="success", duration=5000)
        return alerta, None, None, None, None, None
    else:
        # DEU ERRO NO BANCO: Alerta Vermelho e mantém os dados na tela
        alerta = dbc.Alert(mensagem, color="danger", duration=5000)
        return alerta, nome, selecao, camisa, posicao, nascimento