import math
import mysql.connector
import pandas as pd
import dash
from dash import Input, Output, State, ctx, ALL, html, no_update
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv

load_dotenv()

ESTADIOS_POR_PAGINA = 6

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="Copa do Mundo de Futebol"
    )

def buscar_estadios():
    try:
        conn = obter_conexao()
        query = """
            SELECT id_estadios AS id, nome_estadio AS nome,
                   cidade, pais, capacidade
            FROM `Copa do Mundo de Futebol`.`Estadios`
            ORDER BY nome_estadio
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        print(f"Erro ao buscar estádios: {e}")
        return []

def inserir_estadio(nome, cidade, pais, capacidade):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(id_estadios), 0) + 1 FROM `Copa do Mundo de Futebol`.`Estadios`")
    novo_id = cursor.fetchone()[0]
    cursor.execute(
        """INSERT INTO `Copa do Mundo de Futebol`.`Estadios`
           (id_estadios, nome_estadio, cidade, pais, capacidade)
           VALUES (%s, %s, %s, %s, %s)""",
        (novo_id, nome.strip(), cidade.strip(), pais.strip(), int(capacidade))
    )
    conn.commit()
    cursor.close()
    conn.close()

def deletar_estadio(id_estadio):
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM `Copa do Mundo de Futebol`.`Estadios` WHERE id_estadios = %s",
        (int(id_estadio),)
    )
    conn.commit()
    cursor.close()
    conn.close()

def registrar_callbacks(app):

    @app.callback(
        Output('estadios-pagina-atual', 'data'),
        Input({'type': 'btn-pagina-estadio', 'index': ALL}, 'n_clicks'),
        State('estadios-pagina-atual', 'data'),
        prevent_initial_call=True
    )
    def atualizar_pagina(_, pagina_atual):
        triggered = ctx.triggered_id
        if triggered is None:
            return pagina_atual
        return triggered['index']

    @app.callback(
        Output('tabela-estadios-body',   'children'),
        Output('estadios-info-texto',    'children'),
        Output('estadios-botoes-pagina', 'children'),
        Input('estadios-pagina-atual',   'data'),
        Input('btn-estadios',            'n_clicks'),
        Input('estadios-reload-trigger', 'data'),
    )
    def renderizar_tabela(pagina_atual, _, reload_trigger):
        estadios = buscar_estadios()
        total    = len(estadios)

        if total == 0:
            return ([html.Tr([html.Td("Nenhum estádio encontrado.", colSpan=5,
                    style={'textAlign': 'center', 'color': '#6b7280', 'padding': '30px'})])],
                    "0 estádios", [])

        total_paginas = math.ceil(total / ESTADIOS_POR_PAGINA)
        pagina_atual  = max(1, min(pagina_atual or 1, total_paginas))
        inicio = (pagina_atual - 1) * ESTADIOS_POR_PAGINA
        fim    = inicio + ESTADIOS_POR_PAGINA
        slice_ = estadios[inicio:fim]

        linhas = [
            html.Tr([
                html.Td(e['nome'], style={'fontSize': '14px', 'fontWeight': '600',
                                          'color': '#111827', 'padding': '14px 16px'}),
                html.Td(e['cidade'], style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td(e['pais'],   style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td(f"{int(e['capacidade']):,}".replace(',', '.'),
                        style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td([
                    html.Button(html.I(className="fa fa-pen"),
                                disabled=True, title="Editar (outro membro da equipe)",
                                style={'background': 'none', 'border': 'none',
                                       'cursor': 'not-allowed', 'color': '#d1d5db',
                                       'marginRight': '10px', 'fontSize': '14px'}),
                    html.Button(html.I(className="fa fa-trash"),
                                id={'type': 'btn-delete-estadio', 'index': e['id']},
                                n_clicks=0, title="Excluir estádio",
                                style={'background': 'none', 'border': 'none',
                                       'cursor': 'pointer', 'color': '#ef4444',
                                       'fontSize': '14px'}),
                ], style={'textAlign': 'right', 'padding': '14px 16px'})
            ], style={'borderBottom': '1px solid #f3f4f6', 'verticalAlign': 'middle'})
            for e in slice_
        ]

        info = f"Exibindo {inicio + 1}–{min(fim, total)} de {total} estádios"

        s_ativo  = {'marginRight': '5px', 'backgroundColor': '#047857', 'border': 'none'}
        s_normal = {'marginRight': '5px', 'color': '#4b5563', 'border': '1px solid #e5e7eb'}
        s_nav    = {'border': '1px solid #e5e7eb', 'color': '#4b5563', 'marginRight': '5px'}

        botoes = [dbc.Button("<", id={'type': 'btn-pagina-estadio', 'index': max(1, pagina_atual - 1)},
                             color="light", size="sm", style=s_nav, disabled=(pagina_atual == 1))]

        visiveis = sorted(set([1] +
            list(range(max(2, pagina_atual - 1), min(total_paginas, pagina_atual + 2))) +
            [total_paginas]))

        ultima = 0
        for p in visiveis:
            if ultima and p - ultima > 1:
                botoes.append(html.Span("...", style={'margin': '0 8px', 'color': '#9ca3af'}))
            botoes.append(dbc.Button(str(p), id={'type': 'btn-pagina-estadio', 'index': p},
                                     color="success" if p == pagina_atual else "light",
                                     size="sm", style=s_ativo if p == pagina_atual else s_normal))
            ultima = p

        botoes.append(dbc.Button(">", id={'type': 'btn-pagina-estadio',
                                          'index': min(total_paginas, pagina_atual + 1)},
                                 color="light", size="sm",
                                 style={'border': '1px solid #e5e7eb', 'color': '#4b5563'},
                                 disabled=(pagina_atual == total_paginas)))

        return linhas, info, botoes

    @app.callback(
        Output('nav-estadios', 'data'),
        Input('btn-ir-cadastro-estadio', 'n_clicks'),
        prevent_initial_call=True
    )
    def ir_para_cadastro(n):
        return 'cadastro'

    @app.callback(
        Output('cadastro-estadio-feedback', 'children'),
        Output('nav-estadios',              'data', allow_duplicate=True),
        Output('estadios-reload-trigger',   'data', allow_duplicate=True),
        Input('cadastro-estadio-salvar',    'n_clicks'),
        Input('cadastro-estadio-cancelar',  'n_clicks'),
        State('cadastro-estadio-nome',      'value'),
        State('cadastro-estadio-cidade',    'value'),
        State('cadastro-estadio-pais',      'value'),
        State('cadastro-estadio-capacidade','value'),
        State('estadios-reload-trigger',    'data'),
        prevent_initial_call=True
    )
    def salvar_estadio(salvar, cancelar, nome, cidade, pais, capacidade, trigger):
        triggered = ctx.triggered_id

        if triggered == 'cadastro-estadio-cancelar':
            return '', 'lista', trigger

        if triggered == 'cadastro-estadio-salvar':
            if not nome or not cidade or not pais or not capacidade:
                return (dbc.Alert("Todos os campos são obrigatórios.",
                                  color="warning", className="mt-2"),
                        no_update, trigger)
            try:
                inserir_estadio(nome, cidade, pais, capacidade)
                return '', 'lista', (trigger or 0) + 1
            except mysql.connector.Error as err:
                return (dbc.Alert(f"Erro MySQL: {err.msg}",
                                  color="danger", className="mt-2"),
                        no_update, trigger)

        return '', no_update, trigger

    @app.callback(
        Output('modal-confirmar-delete-estadio', 'is_open'),
        Output('estadio-delete-id',              'data'),
        Input({'type': 'btn-delete-estadio', 'index': ALL}, 'n_clicks'),
        Input('btn-cancelar-delete-estadio',     'n_clicks'),
        Input('btn-confirmar-delete-estadio',    'n_clicks'),
        State('estadio-delete-id',               'data'),
        prevent_initial_call=True
    )
    def gerenciar_modal_delete(cliques_lixeira, cancelar, confirmar, id_atual):
        triggered = ctx.triggered_id

        if triggered == 'btn-cancelar-delete-estadio':
            return False, None
        if triggered == 'btn-confirmar-delete-estadio':
            return False, id_atual
        if isinstance(triggered, dict) and triggered.get('type') == 'btn-delete-estadio':
            for n in cliques_lixeira:
                if n and n > 0:
                    return True, triggered['index']

        return False, id_atual

    @app.callback(
        Output('estadios-reload-trigger', 'data', allow_duplicate=True),
        Output('modal-confirmar-delete-estadio', 'is_open', allow_duplicate=True),
        Input('btn-confirmar-delete-estadio', 'n_clicks'),
        State('estadio-delete-id',            'data'),
        State('estadios-reload-trigger',      'data'),
        prevent_initial_call=True
    )
    def executar_delete(n_clicks, id_estadio, trigger):
        if n_clicks and id_estadio is not None:
            try:
                deletar_estadio(id_estadio)
                return (trigger or 0) + 1, False
            except mysql.connector.Error as err:
                print(f"Erro ao deletar: {err}")
        return trigger, False