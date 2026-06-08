import mysql.connector
from dash import Input, Output, State, ctx, html, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from datetime import datetime


def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Matheus",
        database="Copa do Mundo de Futebol"
    )


def buscar_opcoes_selecoes():
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT id_selecoes, nome_selecao FROM `Copa do Mundo de Futebol`.`Selecoes` ORDER BY nome_selecao")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{'label': r[1], 'value': r[0]} for r in rows]
    except:
        return []


def registrar_callbacks(app):

    @app.callback(
        Output('jogador-editando-id', 'data'),
        Output('pagina-atual-store',  'data', allow_duplicate=True),
        Output('page-content',        'children', allow_duplicate=True),
        Input({'type': 'btn-editar-jogador', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def abrir_edicao(n_clicks):
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
            cursor.execute("""
                SELECT nome_jogador, Selecoes_id_selecoes, numero_camisa, posicao, data_nascimento
                FROM `Copa do Mundo de Futebol`.`Jogadores`
                WHERE id_jogador = %s
            """, (id_jogador,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Erro ao buscar jogador: {e}")
            raise PreventUpdate

        if not row:
            raise PreventUpdate

        nome, id_selecao, numero, posicao, data_nasc = row
        data_str = data_nasc.strftime('%d/%m/%Y') if data_nasc else ''
        opcoes_selecao = buscar_opcoes_selecoes()

        from jogadores.tela_UPDATE_jogadores import build_tela_editar
        tela = build_tela_editar(nome, id_selecao, opcoes_selecao, numero, posicao, data_str)

        # escreve 'editar-jogador' no store para o renderizar_pagina ignorar
        return id_jogador, 'editar-jogador', tela

    @app.callback(
        Output('edit-jogador-feedback', 'children'),
        Input('btn-confirmar-edicao', 'n_clicks'),
        State('jogador-editando-id',  'data'),
        State('edit-nome',            'value'),
        State('edit-selecao',         'value'),
        State('edit-numero',          'value'),
        State('edit-posicao',         'value'),
        State('edit-data-nascimento', 'value'),
        prevent_initial_call=True
    )
    def atualizar_jogador(_, id_jogador, nome, id_selecao, numero, posicao, data_str):
        if not all([id_jogador, nome, id_selecao, numero, posicao, data_str]):
            return dbc.Alert("⚠️ Preencha todos os campos antes de salvar.", color="warning")
        try:
            data_nasc = datetime.strptime(data_str, '%d/%m/%Y').date()
        except ValueError:
            return dbc.Alert("❌ Data inválida. Use o formato DD/MM/AAAA.", color="danger")
        try:
            conn = obter_conexao()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE `Copa do Mundo de Futebol`.`Jogadores`
                SET nome_jogador         = %s,
                    Selecoes_id_selecoes = %s,
                    numero_camisa        = %s,
                    posicao              = %s,
                    data_nascimento      = %s
                WHERE id_jogador = %s
            """, (nome, id_selecao, numero, posicao, data_nasc, id_jogador))
            conn.commit()
            cursor.close()
            conn.close()
            return dbc.Alert("✅ Jogador atualizado com sucesso!", color="success")
        except mysql.connector.Error as err:
            return dbc.Alert(f"❌ Erro MySQL: {err.msg}", color="danger")

    @app.callback(
        Output('page-content',        'children', allow_duplicate=True),
        Output('jogador-editando-id', 'data',     allow_duplicate=True),
        Output('pagina-atual-store',  'data',     allow_duplicate=True),
        Input('btn-cancelar-edicao',  'n_clicks'),
        prevent_initial_call=True
    )
    def cancelar_edicao(_):
        from jogadores.tela_jogadores import tela_jogadores
        return tela_jogadores, None, 'jogadores'