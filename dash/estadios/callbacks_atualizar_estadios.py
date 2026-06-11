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
        Output("output-estadio", "children"),
        Output("input-estadio-nome", "value"),
        Output("input-estadio-cidade", "value"),
        Output("dropdown-estadio-pais", "value"),
        Output("input-estadio-capacidade", "value"),
        Output("nav-estadios", "data", allow_duplicate=True),
        Output("estadios-reload-trigger", "data", allow_duplicate=True),
        Input("btn-estadio-cadastrar", "n_clicks"),
        Input("btn-estadio-cancelar", "n_clicks"),
        State("input-estadio-nome", "value"),
        State("input-estadio-cidade", "value"),
        State("dropdown-estadio-pais", "value"),
        State("input-estadio-capacidade", "value"),
        State("estadio-editando-id", "data"),
        State("estadios-reload-trigger", "data"),
        prevent_initial_call=True
    )
    def gerenciar_estadio(n_cadastrar, n_cancelar, nome, cidade, pais, capacidade, id_estadio, reload_trigger):

        if not n_cadastrar and not n_cancelar:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update
    
        if ctx.triggered_id == "btn-estadio-cancelar":
            return "", "", "", None, None, "lista", no_update
        
        if not id_estadio:
            return "Nenhum estádio selecionado para edição", no_update, no_update, no_update, no_update, no_update, no_update

        if not all([nome, cidade, pais, capacidade is not None]):
            return "⚠️ Preencha todos os campos.", nome, cidade, pais, capacidade, no_update, no_update

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Estadios
                SET nome_estadio = %s, cidade = %s, pais = %s, capacidade = %s
                WHERE id_estadios = %s
            """, (nome, cidade, pais, capacidade, id_estadio))
            conn.commit()
            cursor.close()
            conn.close()
            return f"✅ Estádio '{nome}' atualizado! Cidade: {cidade} | País: {pais} | Capacidade: {capacidade} assentos", nome, cidade, pais, capacidade, "lista", (reload_trigger or 0) + 1
        except Exception as e:
            return f"❌ Erro: {str(e)}", nome, cidade, pais, capacidade, no_update, no_update