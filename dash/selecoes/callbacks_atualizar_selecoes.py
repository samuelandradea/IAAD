import mysql.connector
import os
from dotenv import load_dotenv
from dash import Input, Output, State, ctx, no_update

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="Copa do Mundo de Futebol"
    )

def registrar_callbacks(app):
    @app.callback(
        Output("output-selecao", "children"),
        Output("input-team", "value"),
        Output("dropdown-continent", "value"),
        Output("input-coach", "value"),
        Output("input-titles", "value"),
        Output("nav-store", "data", allow_duplicate=True),
        Output("selecoes-reload-trigger", "data", allow_duplicate=True),
        Input("btn-atualizar", "n_clicks"),
        Input("btn-cancelar", "n_clicks"),
        Input('populate-trigger', 'n_intervals'),                    
        State('selecao-editando-nome', 'data'),         
        State("input-team", "value"),
        State("dropdown-continent", "value"),
        State("input-coach", "value"),
        State("input-titles", "value"),
        State("selecoes-reload-trigger", "data"),
        prevent_initial_call=True
    )
    def gerenciar_selecao(n_atualizar, n_cancelar, n_populate, selecao_nome, nome, continente, tecnico, titulos, reload_trigger):
        triggered = ctx.triggered_id

        # Quando usuário clica em cancelar
        if triggered == "btn-cancelar":
            return "", "", None, "", None, "selecoes", no_update

        # Quando usuário seleciona uma seleção para editar (preencher formulário)
        if triggered == 'populate-trigger':
            if not selecao_nome:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT nome_selecao, continente, tecnico, titulos FROM Selecoes WHERE nome_selecao = %s", (selecao_nome,))
                row = cursor.fetchone()
                cursor.close()
                conn.close()
                if not row:
                    return no_update, selecao_nome, None, "", None, no_update, no_update
                nome_db, continente_db, tecnico_db, titulos_db = row
                return "", nome_db, continente_db, tecnico_db, titulos_db, no_update, no_update
            except Exception as e:
                print(f"Erro ao buscar seleção para editar: {e}")
                return "", no_update, no_update, no_update, no_update, no_update, no_update

        # Quando usuário clica em atualizar
        if triggered == "btn-atualizar":
            if not all([nome, continente, tecnico, titulos is not None]):
                return "⚠️ Preencha todos os campos.", nome, continente, tecnico, titulos, no_update, no_update
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Selecoes
                    SET continente = %s, tecnico = %s, titulos = %s
                    WHERE nome_selecao = %s
                """, (continente, tecnico, titulos, nome))
                conn.commit()
                cursor.close()
                conn.close()
                return f"✅ Seleção '{nome}' atualizada! Continente: {continente} | Técnico: {tecnico} | Títulos: {titulos}", nome, continente, tecnico, titulos, "selecoes", (reload_trigger or 0) + 1
            except Exception as e:
                return f"❌ Erro: {str(e)}", nome, continente, tecnico, titulos, no_update, no_update

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update