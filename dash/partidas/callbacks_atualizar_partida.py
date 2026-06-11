from dash import Input, Output, State
import mysql.connector
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
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

def registrar_callbacks_atualizar_partida(app):
    # Callback 1: Preencher formulário ao selecionar partida
    @app.callback(
        [Output('data-partida', 'date'),
         Output('atualizar-dropdown-estadio', 'value'),
         Output('atualizar-dropdown-time1', 'value'),
         Output('atualizar-dropdown-time2', 'value'),
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

    # Callback 2: Executar o UPDATE
    @app.callback(
        [Output('notificacao-banco', 'children'),
         Output('dropdown-partida-selecionada', 'options')],
        Input('btn-atualizar', 'n_clicks'),
        [State('dropdown-partida-selecionada', 'value'),
         State('data-partida', 'date'),
         State('atualizar-dropdown-estadio', 'value'),
         State('atualizar-dropdown-time1', 'value'),
         State('atualizar-dropdown-time2', 'value'),
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
            if int(gols_t1) > int(gols_t2): vencedor = id_time1
            elif int(gols_t2) > int(gols_t1): vencedor = id_time2
            else: vencedor = None

            conn = obter_conexao()
            cursor = conn.cursor()
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
            return dbc.Alert(f"🔄 Partida {id_partida} atualizada com sucesso!", color="success"), buscar_opcoes_partidas()
        except mysql.connector.Error as err:
            return dbc.Alert(f"❌ Erro MySQL: {err.msg}", color="danger"), buscar_opcoes_partidas()

    # Callback 3: Renderizar Tabela do Histórico
    @app.callback(
        Output('tabela-historico-partidas', 'children'),
        Input('notificacao-banco', 'children')
    )
    def atualizar_tabela_historico(notificacao):
        try:
            conn = obter_conexao()
            query = """
                SELECT p.id_partida AS 'ID', DATE_FORMAT(p.data_partida, '%d/%m/%Y') AS 'Data', est.nome_estadio AS 'Estádio',
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
            return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, className="text-center bg-white shadow-sm rounded")
        except:
            return html.P("Erro ao carregar histórico.")