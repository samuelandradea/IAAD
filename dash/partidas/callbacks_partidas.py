import mysql.connector
import pandas as pd
from dash import Input, Output, State, ctx, html, dcc, ALL, no_update
import os
from dotenv import load_dotenv

load_dotenv()

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="Copa do Mundo de Futebol"
    )

def buscar_partidas():
    try:
        conn = obter_conexao()

        query = """
            SELECT 
                p.id_partida as id,
                p.data_partida as data,
                e.nome_estadio as estadio,
                s1.nome_selecao as time1,
                s2.nome_selecao as time2,
                p.quantidade_gols_selecao_1 as gols1,
                p.quantidade_gols_selecao_2 as gols2
            FROM Partidas p
            JOIN Estadios e ON p.id_estadio = e.id_estadios
            JOIN Selecoes s1 ON p.id_selecao_1 = s1.id_selecoes
            JOIN Selecoes s2 ON p.id_selecao_2 = s2.id_selecoes
            ORDER BY p.id_partida ASC
        """
        df = pd.read_sql(query, conn)
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT id_estadio) FROM Partidas;")
        estadios_ativos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Selecoes;")
        times_inscritos = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT CONCAT(s1.nome_selecao, ' x ', s2.nome_selecao) 
            FROM Partidas p
            JOIN Selecoes s1 ON p.id_selecao_1 = s1.id_selecoes
            JOIN Selecoes s2 ON p.id_selecao_2 = s2.id_selecoes
            ORDER BY p.data_partida ASC LIMIT 1;
        """)
        resultado_abertura = cursor.fetchone()
        partida_abertura = resultado_abertura[0] if resultado_abertura else "Não definida"

        conn.close()

        total_partidas = len(df)

        linhas = []
        for row in df.itertuples():
            linhas.append(
                html.Tr([
                    html.Td(str(row.id), style={"padding": "15px", "color": "#111827", "fontWeight": "500", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(pd.to_datetime(row.data).strftime('%d/%m/%Y'), style={"padding": "15px", "color": "#4b5563", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(row.estadio, style={"padding": "15px", "color": "#4b5563", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(row.time1, style={"padding": "15px", "color": "#111827", "fontWeight": "500", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(row.time2, style={"padding": "15px", "color": "#111827", "fontWeight": "500", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(f"{row.gols1} - {row.gols2}", style={"padding": "15px", "textAlign": "center", "color": "#111827", "fontWeight": "bold", "borderBottom": "1px solid #eaeaea"}),
                    html.Td([
                        # Botão Editar (Lápis)
                        html.Button("✏️", id={'type': 'btn-editar-partida', 'index': row.id}, style={
                            "background": "none", "border": "none", "cursor": "pointer", "marginRight": "10px", "fontSize": "16px"
                        }),
                        # Botão Deletar (Lixeira)
                        html.Button("🗑️", id={'type': 'btn-deletar-partida', 'index': row.id}, style={
                            "background": "none", "border": "none", "cursor": "pointer", "fontSize": "16px"
                        })
                    ], style={"padding": "15px", "textAlign": "right", "borderBottom": "1px solid #eaeaea"}),
                ])
            )

        return linhas, str(total_partidas), str(estadios_ativos), str(times_inscritos), partida_abertura
    except Exception as e:
        print(f"Erro ao buscar partidas: {e}")
        return [], "0", "0", "0", "Erro"

def registrar_callbacks(app):
    # Callback de renderização da tabela principal
    @app.callback(
        Output('tabela-partidas-body', 'children'),
        Output('kpi-total-partidas', 'children'),
        Output('kpi-estadios-ativos', 'children'),
        Output('kpi-times-inscritos', 'children'),
        Output('kpi-partida-abertura', 'children'),
        Input('nav-store', 'data'),
        Input('cadastro-feedback', 'children'),
        Input('btn-atualizar', 'n_clicks'),
        Input('excluir-trigger-store', 'data'), 
        prevent_initial_call=False
    )
    def carregar_dados_tela_principal(pagina, n_salvar, n_atualizar, trigger_excluir):
        return buscar_partidas()

    # Dropdowns do cadastro
    @app.callback(
        Output('dropdown-estadio', 'options'),
        Output('dropdown-time1', 'options'),
        Output('dropdown-time2', 'options'),
        Input('btn-cadastrar-partida', 'n_clicks')
    )
    def carregar_opcoes_dropdown(_):
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("SELECT id_estadios, nome_estadio FROM Estadios")
            estadios = [{"label": row[1], "value": row[0]} for row in cursor.fetchall()]
            cursor.execute("SELECT id_selecoes, nome_selecao FROM Selecoes")
            selecoes = [{"label": row[1], "value": row[0]} for row in cursor.fetchall()]
            conn.close()
            return estadios, selecoes, selecoes
        except Exception as e:
            print(f"Erro ao carregar dropdowns: {e}")
            return [], [], []

    # Ir para tela de edição (Lápis)
    @app.callback(
        Output('dropdown-partida-selecionada', 'value'),
        Input({'type': 'btn-editar-partida', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def ir_para_edicao_partida(botoes_clicks):
        triggered = ctx.triggered_id
        if triggered is None or not any(x for x in botoes_clicks if x is not None):
            return no_update
        
        id_partida = triggered['index']
        return id_partida

    # ETAPA 1 DA EXCLUSÃO: Quando clica no lixo, abre a janela e guarda o ID que foi clicado no Store
    @app.callback(
        Output('confirmacao-exclusao-partida', 'displayed'),
        Output('confirmacao-exclusao-partida', 'message'),
        Output('id-partida-para-excluir-store', 'data'),
        Input({'type': 'btn-deletar-partida', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def disparar_confirmacao(clicks):
        triggered = ctx.triggered_id
        if triggered is None or not any(x for x in clicks if x is not None):
            return False, no_update, no_update
            
        id_partida = triggered['index']
        mensagem = f"Deseja realmente deletar permanentemente a partida de ID {id_partida}?"
        return True, mensagem, id_partida

    # ETAPA 2 DA EXCLUSÃO: Se o usuário confirmar no botão "OK", efetua o DELETE usando o ID salvo
    @app.callback(
        Output('excluir-trigger-store', 'data'),
        Input('confirmacao-exclusao-partida', 'submit_n_clicks'),
        State('id-partida-para-excluir-store', 'data'),
        State('excluir-trigger-store', 'data'),
        prevent_initial_call=True
    )
    def deletar_partida_confirmada(submit_clicks, id_partida_para_deletar, valor_atual):
        if not submit_clicks or id_partida_para_deletar is None:
            return no_update
        
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Partidas WHERE id_partida = %s", (id_partida_para_deletar,))
            conn.commit()
            conn.close()
            return valor_atual + 1
        except Exception as e:
            print(f"Erro ao deletar partida: {e}")
            return no_update

    # Callback para SALVAR nova partida e LIMPAR os campos (também limpa ao Cancelar) e controlar o Modal
    @app.callback(
        Output('modal-cadastro', 'is_open'),
        Output('modal-cadastro-title', 'children'),
        Output('modal-cadastro-title', 'style'),
        Output('modal-cadastro-body', 'children'),
        Output('cadastro-feedback', 'children'),
        Output('input-data-partida', 'value'),
        Output('dropdown-estadio', 'value'),
        Output('dropdown-time1', 'value'),
        Output('dropdown-time2', 'value'),
        Output('input-gols-time1', 'value'),
        Output('input-gols-time2', 'value'),
        Input('btn-salvar-partida', 'n_clicks'),
        Input('btn-cancelar-cadastro', 'n_clicks'),
        Input('btn-fechar-modal-cadastro', 'n_clicks'),
        State('input-data-partida', 'value'),
        State('dropdown-estadio', 'value'),
        State('dropdown-time1', 'value'),
        State('dropdown-time2', 'value'),
        State('input-gols-time1', 'value'),
        State('input-gols-time2', 'value'),
        prevent_initial_call=True
    )
    def salvar_nova_partida(n_salvar, n_cancelar, n_fechar, data, id_estadio, id_time1, id_time2, gols1, gols2):
        triggered = ctx.triggered_id
        
        if triggered == 'btn-fechar-modal-cadastro':
            return False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        
        if triggered == 'btn-cancelar-cadastro':
            return False, no_update, no_update, no_update, no_update, "", None, None, None, 0, 0
            
        if triggered == 'btn-salvar-partida':
            if not data or not id_estadio or not id_time1 or not id_time2:
                return True, "⚠️ Atenção", {"color": "#d97706"}, "Preencha todos os campos obrigatórios.", no_update, no_update, no_update, no_update, no_update, no_update, no_update
                
            if id_time1 == id_time2:
                return True, "❌ Erro", {"color": "#dc2626"}, "O Time 1 não pode jogar contra si mesmo.", no_update, no_update, no_update, no_update, no_update, no_update, no_update
                
            try:
                conn = obter_conexao()
                cursor = conn.cursor()
                
                if gols1 is None: gols1 = 0
                if gols2 is None: gols2 = 0
                
                if int(gols1) > int(gols2): vencedor = id_time1
                elif int(gols2) > int(gols1): vencedor = id_time2
                else: vencedor = None
                
                cursor.execute("SELECT IFNULL(MAX(id_partida), 0) + 1 FROM Partidas")
                novo_id = cursor.fetchone()[0]
                
                sql = "INSERT INTO Partidas (id_partida, data_partida, quantidade_gols_selecao_1, quantidade_gols_selecao_2, id_estadio, id_selecao_1, id_selecao_2, vencedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (novo_id, data, gols1, gols2, id_estadio, id_time1, id_time2, vencedor)
                cursor.execute(sql, val)
                conn.commit()
                cursor.close()
                conn.close()
                
                return True, "✅ Sucesso", {"color": "#059669"}, "A partida foi cadastrada com sucesso!", "refresh", "", None, None, None, 0, 0
            except Exception as e:
                return True, "❌ Erro", {"color": "#dc2626"}, f"Ocorreu um erro ao cadastrar no banco: {e}", no_update, no_update, no_update, no_update, no_update, no_update, no_update
            
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
