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
        Output("output-estadio", "children"),
        Output("input-estadio-nome", "value"),
        Output("input-estadio-cidade", "value"),
        Output("dropdown-estadio-pais", "value"),
        Output("input-estadio-capacidade", "value"),
        Input("btn-estadio-cadastrar", "n_clicks"),
        Input("btn-estadio-cancelar", "n_clicks"),
        State("input-estadio-nome", "value"),
        State("input-estadio-cidade", "value"),
        State("dropdown-estadio-pais", "value"),
        State("input-estadio-capacidade", "value"),
        prevent_initial_call=True
    )
    def gerenciar_estadio(n_cadastrar, n_cancelar, nome, cidade, pais, capacidade):
        if ctx.triggered_id == "btn-estadio-cancelar":
            return "", "", "", None, None

        if not all([nome, cidade, pais, capacidade is not None]):
            return "⚠️ Preencha todos os campos.", nome, cidade, pais, capacidade

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Estadios
                SET cidade = %s, pais = %s, capacidade = %s
                WHERE nome_estadio = %s
            """, (cidade, pais, capacidade, nome))
            conn.commit()
            cursor.close()
            conn.close()
            return f"✅ Estádio '{nome}' atualizado! Cidade: {cidade} | País: {pais} | Capacidade: {capacidade} assentos", nome, cidade, pais, capacidade
        except Exception as e:
            return f"❌ Erro: {str(e)}", nome, cidade, pais, capacidade