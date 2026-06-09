import mysql.connector
import os
from dotenv import load_dotenv
from dash import Input, Output, State, ctx

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
        Input("btn-atualizar", "n_clicks"),
        Input("btn-cancelar", "n_clicks"),
        State("input-team", "value"),
        State("dropdown-continent", "value"),
        State("input-coach", "value"),
        State("input-titles", "value"),
        prevent_initial_call=True
    )
    def gerenciar_selecao(n_atualizar, n_cancelar, nome, continente, tecnico, titulos):
        if ctx.triggered_id == "btn-cancelar":
            return "", "", None, "", None

        if not all([nome, continente, tecnico, titulos is not None]):
            return "⚠️ Preencha todos os campos.", nome, continente, tecnico, titulos

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
            return f"✅ Seleção '{nome}' atualizada! Continente: {continente} | Técnico: {tecnico} | Títulos: {titulos}", nome, continente, tecnico, titulos
        except Exception as e:
            return f"❌ Erro: {str(e)}", nome, continente, tecnico, titulos