import math
from dash.exceptions import PreventUpdate
import mysql.connector
from dash import Input, Output, State, ctx, ALL, html
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv

load_dotenv()

JOGADORES_POR_PAGINA = 5


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="Copa do Mundo de Futebol"
    )


def buscar_jogadores():
    try:
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                j.nome_jogador  AS nome,
                j.posicao       AS posicao,
                j.numero_camisa AS numero,
                s.nome_selecao  AS selecao,
                j.id_jogador    AS id_jogador,
                TIMESTAMPDIFF(YEAR, j.data_nascimento, CURDATE()) AS idade
            FROM `Copa do Mundo de Futebol`.`Jogadores` j
            JOIN `Copa do Mundo de Futebol`.`Selecoes` s
              ON j.Selecoes_id_selecoes = s.id_selecoes
            ORDER BY j.nome_jogador
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erro ao buscar jogadores: {e}")
        return []


def registrar_callbacks(app):

    # CALLBACK 1 — atualiza página via botões de paginação
    @app.callback(
        Output('jogadores-pagina-atual', 'data'),
        Input({'type': 'btn-pagina-jogador', 'index': ALL}, 'n_clicks'),
        State('jogadores-pagina-atual', 'data'),
        prevent_initial_call=True
    )
    def atualizar_pagina(_, pagina_atual):
        triggered = ctx.triggered_id
        if triggered is None:
            raise PreventUpdate

        idx = triggered['index']
        if idx == 0:   return max(1, pagina_atual - 1)
        if idx == -1:  return pagina_atual + 1
        return idx

    # CALLBACK 2 — DELETE
    @app.callback(
        Output('jogadores-pagina-atual', 'data', allow_duplicate=True),
        Input({'type': 'btn-deletar-jogador', 'index': ALL}, 'n_clicks'),
        State('jogadores-pagina-atual', 'data'),
        prevent_initial_call=True
    )
    def deletar_jogador(n_clicks, pagina_atual):
        triggered = ctx.triggered_id
        if not triggered:
            raise PreventUpdate

        botoes = ctx.inputs_list[0]
        clicado = next((b for b in botoes if b['id']['index'] == triggered['index']), None)
        if not clicado or not clicado.get('value'):
            raise PreventUpdate

        id_jogador = triggered['index']

        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM `Copa do Mundo de Futebol`.`Jogadores` WHERE id_jogador = %s",
                (id_jogador,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f">>> Jogador {id_jogador} deletado com sucesso")
        except Exception as e:
            print(f"Erro ao deletar jogador: {e}")

        return pagina_atual

    # CALLBACK 3 — renderiza tabela + paginação
    @app.callback(
        Output('tabela-jogadores-body',   'children'),
        Output('jogadores-info-texto',    'children'),
        Output('jogadores-botoes-pagina', 'children'),
        Input('jogadores-pagina-atual',   'data'),
        Input('btn-jogadores',            'n_clicks'),
    )
    def renderizar_tabela(pagina_atual, _):
        jogadores = buscar_jogadores()
        total     = len(jogadores)

        if total == 0:
            linha_vazia = html.Tr([
                html.Td("Nenhum jogador encontrado.", colSpan=6,
                        style={'textAlign': 'center', 'color': '#6b7280', 'padding': '30px'})
            ])
            return [linha_vazia], "0 players", []

        total_paginas = math.ceil(total / JOGADORES_POR_PAGINA)
        pagina_atual  = max(1, min(pagina_atual or 1, total_paginas))

        inicio = (pagina_atual - 1) * JOGADORES_POR_PAGINA
        fim    = inicio + JOGADORES_POR_PAGINA
        slice_ = jogadores[inicio:fim]

        # ── Linhas ───────────────────────────────────────────────────────
        linhas = [
            html.Tr([
                html.Td(j['nome'],        style={'fontSize': '14px', 'fontWeight': '600', 'color': '#111827', 'padding': '14px 16px'}),
                html.Td(j['posicao'],     style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td(str(j['numero']), style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td(j['selecao'],     style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td(str(j['idade']),  style={'fontSize': '14px', 'color': '#4b5563', 'padding': '14px 16px'}),
                html.Td([
                    html.Span(
                        "✏️",
                        id={'type': 'btn-editar-jogador', 'index': j['id_jogador']},
                        n_clicks=0,
                        style={'cursor': 'pointer', 'marginRight': '10px', 'fontSize': '16px'}
                    ),
                    html.Span(
                        "🗑️",
                        id={'type': 'btn-deletar-jogador', 'index': j['id_jogador']},
                        n_clicks=0,
                        style={'cursor': 'pointer', 'color': '#ef4444', 'fontSize': '16px'}
                    )
                ], style={'textAlign': 'right', 'padding': '14px 16px'}),
            ], style={'borderBottom': '1px solid #f3f4f6', 'verticalAlign': 'middle'})
            for j in slice_
        ]

        # ── Texto informativo ─────────────────────────────────────────────
        info = f"Showing {inicio + 1}–{min(fim, total)} of {total:,} players"

        # ── Botões de paginação ───────────────────────────────────────────
        s_ativo  = {'marginRight': '5px', 'backgroundColor': '#047857', 'border': 'none'}
        s_normal = {'marginRight': '5px', 'color': '#4b5563', 'border': '1px solid #e5e7eb'}
        s_nav    = {'border': '1px solid #e5e7eb', 'color': '#4b5563', 'marginRight': '5px'}

        def paginas_visiveis(atual, total):
            if total <= 7:
                return list(range(1, total + 1))
            if atual <= 4:
                return [1, 2, 3, 4, 5, '...', total]
            if atual >= total - 3:
                return [1, '...', total-4, total-3, total-2, total-1, total]
            return [1, '...', atual-1, atual, atual+1, '...', total]

        botoes = [
            dbc.Button("<",
                       id={'type': 'btn-pagina-jogador', 'index': 0},
                       color="light", size="sm", style=s_nav,
                       disabled=(pagina_atual == 1))
        ]

        for p in paginas_visiveis(pagina_atual, total_paginas):
            if p == '...':
                botoes.append(html.Span("...", style={'margin': '0 8px', 'color': '#9ca3af', 'lineHeight': '32px'}))
            else:
                botoes.append(
                    dbc.Button(str(p),
                               id={'type': 'btn-pagina-jogador', 'index': p},
                               color="success" if p == pagina_atual else "light",
                               size="sm",
                               style=s_ativo if p == pagina_atual else s_normal)
                )

        botoes.append(
            dbc.Button(">",
                       id={'type': 'btn-pagina-jogador', 'index': -1},
                       color="light", size="sm",
                       style={'border': '1px solid #e5e7eb', 'color': '#4b5563'},
                       disabled=(pagina_atual == total_paginas))
        )

        return linhas, info, botoes