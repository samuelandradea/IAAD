import math
import mysql.connector
import pandas as pd
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
        password=os.getenv("DB_PASSWORD", "1234"),
        database="Copa do Mundo de Futebol"
    )


def buscar_jogadores():
    try:
        conn = obter_conexao()
        query = """
            SELECT 
                j.nome_jogador AS nome,
                j.posicao      AS posicao,
                j.numero_camisa AS numero,
                s.nome_selecao  AS selecao,
                TIMESTAMPDIFF(YEAR, j.data_nascimento, CURDATE()) AS idade
            FROM `Copa do Mundo de Futebol`.`Jogadores` j
            JOIN `Copa do Mundo de Futebol`.`Selecoes` s
              ON j.Selecoes_id_selecoes = s.id_selecoes
            ORDER BY j.nome_jogador
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        print(f"Erro ao buscar jogadores: {e}")
        return []


def registrar_callbacks(app):
    """Chamada uma vez no app.py para registrar todos os callbacks desta tela."""

    # CALLBACK 1 — atualiza o Store com a página clicada
    @app.callback(
        Output('jogadores-pagina-atual', 'data'),
        Input({'type': 'btn-pagina-jogador', 'index': ALL}, 'n_clicks'),
        State('jogadores-pagina-atual', 'data'),
        prevent_initial_call=True
    )
    def atualizar_pagina(_, pagina_atual):
        triggered = ctx.triggered_id
        if triggered is None:
            return pagina_atual
        return triggered['index']

    # CALLBACK 2 — renderiza tbody + info + botões de paginação
    @app.callback(
        Output('tabela-jogadores-body',   'children'),
        Output('jogadores-info-texto',    'children'),
        Output('jogadores-botoes-pagina', 'children'),
        Input('jogadores-pagina-atual',   'data'),
        Input('btn-jogadores',            'n_clicks'),
    )
    def renderizar_tabela(pagina_atual, _):
        jogadores     = buscar_jogadores()
        total         = len(jogadores)

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
                    html.Span("✏️", style={'cursor': 'pointer', 'marginRight': '15px'}),
                    html.Span("🗑️", style={'cursor': 'pointer', 'color': '#ef4444'})
                ], style={'textAlign': 'right', 'padding': '14px 16px', 'fontSize': '14px'})
            ], style={'borderBottom': '1px solid #f3f4f6', 'verticalAlign': 'middle'})
            for j in slice_
        ]

        # ── Texto informativo ─────────────────────────────────────────────
        info = f"Showing {inicio + 1}–{min(fim, total)} of {total:,} players"

        # ── Botões de paginação ───────────────────────────────────────────
        s_ativo  = {'marginRight': '5px', 'backgroundColor': '#047857', 'border': 'none'}
        s_normal = {'marginRight': '5px', 'color': '#4b5563', 'border': '1px solid #e5e7eb'}
        s_nav    = {'border': '1px solid #e5e7eb', 'color': '#4b5563', 'marginRight': '5px'}

        botoes = [
            dbc.Button("<",
                       id={'type': 'btn-pagina-jogador', 'index': max(1, pagina_atual - 1)},
                       color="light", size="sm", style=s_nav,
                       disabled=(pagina_atual == 1)),
        ]

        # janela deslizante de páginas visíveis
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
                           id={'type': 'btn-pagina-jogador', 'index': p},
                           color="success" if p == pagina_atual else "light",
                           size="sm",
                           style=s_ativo if p == pagina_atual else s_normal)
            )
            ultima = p

        botoes.append(
            dbc.Button(">",
                       id={'type': 'btn-pagina-jogador', 'index': min(total_paginas, pagina_atual + 1)},
                       color="light", size="sm", style={'border': '1px solid #e5e7eb', 'color': '#4b5563'},
                       disabled=(pagina_atual == total_paginas))
        )

        return linhas, info, botoes