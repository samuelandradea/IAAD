import mysql.connector
import pandas as pd
from dash import Input, Output, State, ctx, html, ALL, no_update
import os
from datetime import datetime
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

def cadastrar_partida_db(data, id_estadio, id_time1, id_time2, gols1, gols2):
    """Insere uma nova partida no banco. Retorna (sucesso: bool, mensagem: str)."""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()

        gols1, gols2 = int(gols1), int(gols2)
        if gols1 > gols2:
            vencedor = id_time1
        elif gols2 > gols1:
            vencedor = id_time2
        else:
            vencedor = None

        cursor.execute("SELECT COALESCE(MAX(id_partida), 0) + 1 FROM Partidas")
        novo_id = cursor.fetchone()[0]

        sql = """
            INSERT INTO Partidas
            (id_partida, data_partida, quantidade_gols_selecao_1, quantidade_gols_selecao_2,
             id_estadio, id_selecao_1, id_selecao_2, vencedor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (novo_id, data, gols1, gols2, id_estadio, id_time1, id_time2, vencedor)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return True, f"Partida {novo_id} cadastrada com sucesso!"
    except mysql.connector.Error as err:
        return False, f"Erro MySQL: {err.msg}"
    except Exception as e:
        return False, f"Erro inesperado: {e}"

def registrar_callbacks(app):
    # Callback principal da tabela
    @app.callback(
        Output('tabela-partidas-body', 'children'),
        Output('kpi-total-partidas', 'children'),
        Output('kpi-estadios-ativos', 'children'),
        Output('kpi-times-inscritos', 'children'),
        Output('kpi-partida-abertura', 'children'),
        Input('nav-store', 'data'),
        Input('btn-salvar-partida', 'n_clicks'),
        Input('btn-atualizar', 'n_clicks'),  # <-- ESCUTA O CLIQUE DE ATUALIZAR DA OUTRA TELA!
        Input('excluir-trigger-store', 'data'), 
        prevent_initial_call=False
    )
    def carregar_dados_tela_principal(pagina, n_salvar, n_atualizar, trigger_excluir):
        # Sempre que houver qualquer uma das ações acima, ele busca os dados fresquinhos do MySQL
        return buscar_partidas()

    # Dropdowns do cadastro
    @app.callback(
        Output('dropdown-estadio', 'options'),
        Output('dropdown-time1', 'options'),
        Output('dropdown-time2', 'options'),
        Input('btn-cadastrar-partida', 'n_clicks'),
        prevent_initial_call=True
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
        except:
            return [], [], []

    # Salvar nova partida (Create)
    @app.callback(
        Output('modal-cadastro', 'is_open'),
        Output('modal-cadastro-title', 'children'),
        Output('modal-cadastro-body', 'children'),
        Output('input-data-partida', 'value'),
        Output('dropdown-estadio', 'value'),
        Output('dropdown-time1', 'value'),
        Output('dropdown-time2', 'value'),
        Output('input-gols-time1', 'value'),
        Output('input-gols-time2', 'value'),
        Output('partida-salva-sucesso', 'data'),
        Input('btn-salvar-partida', 'n_clicks'),
        State('input-data-partida', 'value'),
        State('dropdown-estadio', 'value'),
        State('dropdown-time1', 'value'),
        State('dropdown-time2', 'value'),
        State('input-gols-time1', 'value'),
        State('input-gols-time2', 'value'),
        prevent_initial_call=True
    )
    def salvar_nova_partida(n_clicks, data, id_estadio, id_time1, id_time2, gols1, gols2):
        if not data or id_estadio is None or id_time1 is None or id_time2 is None \
                or gols1 is None or gols2 is None:
            return (True, "Atenção", "Preencha todos os campos antes de cadastrar a partida.",
                    data, id_estadio, id_time1, id_time2, gols1, gols2, False)

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            return (True, "Atenção", "Data inválida. Use o formato AAAA-MM-DD (ex: 2026-06-15).",
                    data, id_estadio, id_time1, id_time2, gols1, gols2, False)

        if id_time1 == id_time2:
            return (True, "Regra de negócio", "O Time 1 não pode jogar contra si mesmo.",
                    data, id_estadio, id_time1, id_time2, gols1, gols2, False)

        sucesso, mensagem = cadastrar_partida_db(data, id_estadio, id_time1, id_time2, gols1, gols2)

        if sucesso:
            return (True, "Sucesso", mensagem, None, None, None, None, 0, 0, True)

        return (True, "Erro", mensagem, data, id_estadio, id_time1, id_time2, gols1, gols2, False)

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

    # ETAPA 1 DA EXCLUSÃO: Quando clica no lixo
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

    # ETAPA 2 DA EXCLUSÃO: Confirmação do "OK"
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
