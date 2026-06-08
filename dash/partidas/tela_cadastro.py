from dash import html, dcc
import dash_bootstrap_components as dbc

input_style = {
    "width": "100%",
    "height": "40px",
    "padding": "8px 12px", 
    "borderRadius": "5px", 
    "border": "1px solid #d1d5db", 
    "marginTop": "5px", 
    "marginBottom": "20px",
    "boxSizing": "border-box",
    "color": "#4b5563"
}

label_style = {"fontWeight": "bold", "color": "#4b5563", "fontSize": "14px"}

tela_cadastro = html.Div([

    html.Div([
        html.H2("Cadastro de Partida", style={"fontWeight": "bold", "color": "#111827", "margin": "0 0 5px 0", "textAlign": "left"}),
        html.P("Registre um novo confronto da Copa do Mundo FIFA 2026 no banco de dados central.", style={"color": "#6b7280", "margin": "0", "textAlign": "left"}),
    ], style={"marginBottom": "30px"}),


    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Data da Partida (YYYY-MM-DD)", style=label_style),

                dcc.Input(id="input-data-partida", type="text", placeholder="Ex: 2026-06-15", style=input_style)
            ], width=6),
            dbc.Col([
                html.Label("Estádio", style=label_style),
                dcc.Dropdown(
                    id="dropdown-estadio",
                    options=[],
                    placeholder="Selecione o local",
                    style={"marginTop": "5px", "marginBottom": "20px"}
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Time 1 (Mandante)", style=label_style),
                dcc.Dropdown(
                    id="dropdown-time1",
                    options=[],
                    placeholder="Selecione o país",
                    style={"marginTop": "5px", "marginBottom": "20px"}
                )
            ], width=6),
            dbc.Col([
                html.Label("Time 2 (Visitante)", style=label_style),
                dcc.Dropdown(
                    id="dropdown-time2",
                    options=[],
                    placeholder="Selecione o país",
                    style={"marginTop": "5px", "marginBottom": "20px"}
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Quantidade de gols Time 1", style=label_style),
                dcc.Input(id="input-gols-time1", type="number", value=0, min=0, style=input_style)
            ], width=6),
            dbc.Col([
                html.Label("Quantidade de gols Time 2", style=label_style),
                dcc.Input(id="input-gols-time2", type="number", value=0, min=0, style=input_style)
            ], width=6)
        ]),

        html.Hr(style={"borderColor": "#eaeaea", "marginTop": "10px", "marginBottom": "20px"}),


        html.Div(id="cadastro-feedback", style={"marginBottom": "15px", "color": "#059669", "fontWeight": "bold"}),


        html.Div([
            html.Button("Cancelar", id="btn-cancelar-cadastro", style={
                "backgroundColor": "transparent", "color": "#4b5563", "border": "none", 
                "padding": "10px 20px", "fontWeight": "bold", "cursor": "pointer", "marginRight": "10px"
            }),
            html.Button("Cadastrar Partida", id="btn-salvar-partida", style={
                "backgroundColor": "#059669", "color": "white", "border": "none", 
                "padding": "10px 20px", "borderRadius": "5px", "fontWeight": "bold", "cursor": "pointer"
            })
        ], style={"display": "flex", "justifyContent": "flex-end"})
        
    ], style={"backgroundColor": "#fcfcfd", "borderRadius": "8px", "border": "1px solid #eaeaea", "padding": "30px", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"})
    
], style={"maxWidth": "800px", "margin": "0 auto", "padding": "20px"})
