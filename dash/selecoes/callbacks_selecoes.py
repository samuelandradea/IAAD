import math
import mysql.connector
import pandas as pd
from dash import Input, Output, State, ctx, ALL, html
import dash_bootstrap_components as dbc


SELECOES_POR_PAGINA = 10


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="Copa do Mundo de Futebol"
    )


def buscar_selecoes():
    try:
        conn = obter_conexao()
        query = """
            SELECT
                nome_selecao  AS nome,
                continente    AS confederacao,
                titulos       AS titulos
            FROM `Copa do Mundo de Futebol`.`Selecoes`
            ORDER BY nome_selecao
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        print(f"Erro ao buscar seleções: {e}")
        return []


def registrar_callbacks(app):

    @app.callback(
        Output('selecoes-pagina-atual', 'data'),
        Input({'type': 'btn-pagina-selecao', 'index': ALL}, 'n_clicks'),
        State('selecoes-pagina-atual', 'data'),
        prevent_initial_call=True
    )
    def atualizar_pagina(_, pagina_atual):
        triggered = ctx.triggered_id
        if triggered is None:
            return pagina_atual
        return triggered['index']

    @app.callback(
        Output('tabela-selecoes-body',   'children'),
        Output('selecoes-info-texto',    'children'),
        Output('selecoes-botoes-pagina', 'children'),
        Input('selecoes-pagina-atual',   'data'),
        Input('btn-selecoes',            'n_clicks'),
    )
    def renderizar_tabela(pagina_atual, _):
        selecoes      = buscar_selecoes()
        total         = len(selecoes)

        if total == 0:
            linha_vazia = html.Tr([
                html.Td("Nenhuma seleção encontrada.", colSpan=4,
                        style={'textAlign': 'center', 'color': '#6b7280', 'padding': '30px'})
            ])
            return [linha_vazia], "0 seleções", []

        total_paginas = math.ceil(total / SELECOES_POR_PAGINA)
        pagina_atual  = max(1, min(pagina_atual or 1, total_paginas))

        inicio = (pagina_atual - 1) * SELECOES_POR_PAGINA
        fim    = inicio + SELECOES_POR_PAGINA
        slice_ = selecoes[inicio:fim]

        linhas = [
            html.Tr([
                html.Td(s['nome'],           style={'fontSize': '15px', 'fontWeight': '600', 'color': '#131b2e', 'padding': '14px 24px'}),
                html.Td(s['confederacao'],   style={'fontSize': '13px', 'fontFamily': 'monospace', 'color': '#3c4b3b', 'padding': '14px 24px'}),
                html.Td(str(s['titulos']),   style={'fontSize': '13px', 'fontFamily': 'monospace', 'color': '#131b2e', 'padding': '14px 24px'}),
                html.Td([
                    html.Span("✏️", style={'cursor': 'pointer', 'marginRight': '12px', 'fontSize': '16px'}),
                    html.Span("🗑️", style={'cursor': 'pointer', 'fontSize': '16px'})
                ], style={'textAlign': 'center', 'padding': '14px 24px'})
            ], style={'borderBottom': '1px solid #f1f5f9', 'verticalAlign': 'middle',
                      'backgroundColor': '#f1f5f9' if idx % 2 == 1 else 'transparent'})
            for idx, s in enumerate(slice_)
        ]

        info = f"Showing {inicio + 1}-{min(fim, total)} of {total} teams"

        s_ativo  = {'marginRight': '4px', 'backgroundColor': '#006e28', 'border': 'none'}
        s_normal = {'marginRight': '4px', 'color': '#131b2e', 'border': '1px solid #e5e7eb'}
        s_nav    = {'border': '1px solid #e5e7eb', 'color': '#4b5563', 'marginRight': '4px'}

        botoes = [
            dbc.Button("<",
                       id={'type': 'btn-pagina-selecao', 'index': max(1, pagina_atual - 1)},
                       color="light", size="sm", style=s_nav,
                       disabled=(pagina_atual == 1)),
        ]

        visiveis = sorted(set(
            [1] +
            list(range(max(2, pagina_atual - 1), min(total_paginas, pagina_atual + 2))) +
            [total_paginas]
        ))

        ultima = 0
        for p in visiveis:
            if ultima and p - ultima > 1:
                botoes.append(html.Span("...", style={'margin': '0 8px', 'color': '#9ca3af'}))
            botoes.append(
                dbc.Button(str(p),
                           id={'type': 'btn-pagina-selecao', 'index': p},
                           color="success" if p == pagina_atual else "light",
                           size="sm",
                           style=s_ativo if p == pagina_atual else s_normal)
            )
            ultima = p

        botoes.append(
            dbc.Button(">",
                       id={'type': 'btn-pagina-selecao', 'index': min(total_paginas, pagina_atual + 1)},
                       color="light", size="sm", style={'border': '1px solid #e5e7eb', 'color': '#4b5563'},
                       disabled=(pagina_atual == total_paginas))
        )

        return linhas, info, botoes
