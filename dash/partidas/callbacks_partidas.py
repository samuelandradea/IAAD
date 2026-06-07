import mysql.connector
import pandas as pd
from dash import Input, Output, State, ctx, html
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
        
        conn.close()
        return df.to_dict('records'), estadios_ativos, times_inscritos
    except Exception as e:
        print(f"Erro ao buscar partidas: {e}")
        return [], 0, 0

def registrar_callbacks(app):
    

    @app.callback(
        [Output('container-lista-partidas', 'style'),
         Output('container-cadastro-partida', 'style'),
         Output('cadastro-feedback', 'children')],
        [Input('btn-cadastrar-partida', 'n_clicks'),
         Input('btn-cancelar-cadastro', 'n_clicks'),
         Input('btn-salvar-partida', 'n_clicks')],
        [State('input-data-partida', 'value'),
         State('dropdown-estadio', 'value'),
         State('dropdown-time1', 'value'),
         State('dropdown-time2', 'value'),
         State('input-gols-time1', 'value'),
         State('input-gols-time2', 'value')],
        prevent_initial_call=True
    )
    def alternar_e_salvar(btn_cad, btn_canc, btn_salvar, data, estadio, t1, t2, g1, g2):
        botao_clicado = ctx.triggered_id
        

        if botao_clicado == 'btn-cadastrar-partida':
            return {'display': 'none'}, {'display': 'block'}, ""
            

        elif botao_clicado == 'btn-cancelar-cadastro':
            return {'display': 'block'}, {'display': 'none'}, ""
            

        elif botao_clicado == 'btn-salvar-partida':

            if not all([data, estadio, t1, t2, g1 is not None, g2 is not None]):
                return {'display': 'none'}, {'display': 'block'}, "Por favor, preencha todos os campos."
            
            try:
                conn = obter_conexao()
                cursor = conn.cursor()
                

                cursor.execute("SELECT COALESCE(MAX(id_partida), 0) + 1 FROM Partidas")
                novo_id = cursor.fetchone()[0]
                

                vencedor = None
                if int(g1) > int(g2):
                    vencedor = int(t1)
                elif int(g2) > int(g1):
                    vencedor = int(t2)
                    
                sql = """
                    INSERT INTO Partidas 
                    (id_partida, data_partida, quantidade_gols_selecao_1, quantidade_gols_selecao_2, id_estadio, id_selecao_1, id_selecao_2, vencedor)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (novo_id, data, g1, g2, estadio, t1, t2, vencedor)
                cursor.execute(sql, valores)
                conn.commit()
                conn.close()
                

                return {'display': 'block'}, {'display': 'none'}, ""
            except Exception as e:
                print(f"Erro ao salvar: {e}")
                return {'display': 'none'}, {'display': 'block'}, f"Erro no banco: {str(e)}"
                
        return {'display': 'block'}, {'display': 'none'}, ""



    @app.callback(
        Output('tabela-partidas-body', 'children'),
        Output('kpi-total-partidas', 'children'),
        Output('kpi-estadios-ativos', 'children'),
        Output('kpi-times-inscritos', 'children'),
        Output('kpi-partida-abertura', 'children'),
        Input('btn-partidas', 'n_clicks'),
        Input('btn-salvar-partida', 'n_clicks') # Recarrega ao salvar
    )
    def renderizar_tabela(btn_partidas, btn_salvar):
        partidas, estadios_ativos, times_inscritos = buscar_partidas()
        total_partidas = len(partidas)
        
        partida_abertura = "-"
        
        if total_partidas == 0:
            linha_vazia = html.Tr([
                html.Td("Nenhuma partida encontrada.", colSpan=6,
                        style={'textAlign': 'center', 'color': '#6b7280', 'padding': '30px'})
            ])
            return [linha_vazia], "0", "0", str(times_inscritos), "-"
            

        primeira = partidas[0]
        partida_abertura = f"{primeira['estadio']}, {primeira['time1']} x {primeira['time2']}"


        linhas = []
        for p in partidas:
            placar = f"{p['gols1']} - {p['gols2']}"
            linhas.append(
                html.Tr([
                    html.Td(f"#{p['id']:02d}", style={"padding": "15px", "color": "#059669", "fontWeight": "bold", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(p['estadio'], style={"padding": "15px", "color": "#111827", "fontWeight": "bold", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(p['time1'], style={"padding": "15px", "color": "#4b5563", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(p['time2'], style={"padding": "15px", "color": "#4b5563", "borderBottom": "1px solid #eaeaea"}),
                    html.Td(placar, style={"padding": "15px", "textAlign": "center", "color": "#111827", "fontWeight": "bold", "borderBottom": "1px solid #eaeaea"}),
                    html.Td([
                        html.Span("✏️", style={"cursor": "pointer", "marginRight": "10px", "color": "#6b7280"}),
                        html.Span("🗑️", style={"cursor": "pointer", "color": "#ef4444"})
                    ], style={"padding": "15px", "textAlign": "right", "borderBottom": "1px solid #eaeaea"}),
                ])
            )

        return linhas, str(total_partidas), str(estadios_ativos), str(times_inscritos), partida_abertura

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
        except Exception as e:
            print(f"Erro ao carregar opções: {e}")
            return [], [], []
