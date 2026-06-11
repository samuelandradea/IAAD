## Atualização/update das seleções

from dash import Dash, html, dcc 
import dash 
import dash_bootstrap_components as dbc 


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

estilo_botao_padrao = {
    'background': 'none', 'border': 'none', 'cursor': 'pointer',
    'color': '#4b5563', 'fontWeight': 'bold', 'fontSize': '14px'
}

estilo_botao_ativo = estilo_botao_padrao.copy()
estilo_botao_ativo.update({'color': '#15803d', 'borderBottom': '3px solid #15803d'})



cabecalho = html.Div([
    html.H2("Atualizar Seleção", style={"fontWeight": "700", "marginTop": "40px"}),
    html.P(
        "Atualize os dados técnicos da federação na base de dados da Copa do Mundo 2026.",
        style={"color": "#555", "marginBottom": "24px"}
    ),
])

formulario = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Team Name"),
                dbc.Input(
                    id="input-team",
                    type="text",
                    placeholder="Ex: Brasil, France, etc.",
                    style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                ),
            ], md=6),

            dbc.Col([
                dbc.Label("Continent"),
                dcc.Dropdown(
                    id="dropdown-continent",
                    options=[
                        {"label": "Africa",        "value": "africa"},
                        {"label": "Asia",          "value": "asia"},
                        {"label": "Europe",        "value": "europe"},
                        {"label": "North America", "value": "north_america"},
                        {"label": "Oceania",       "value": "oceania"},
                        {"label": "South America", "value": "south_america"},
                    ],
                    placeholder="Selecione o continente",
                    style={"backgroundColor": "#f0f2ff"}
                ),
            ], md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Coach"),
                dbc.Input(
                    id="input-coach",
                    type="text",
                    placeholder="Nome do Treinador",
                    style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                ),
            ], md=6),

            dbc.Col([
                dbc.Label("Number of Titles"),
                dbc.InputGroup([
                    dbc.InputGroupText("🏆"),
                    dbc.Input(
                        id="input-titles",
                        type="number",
                        value=0,
                        min=0,
                        max=20,
                        style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                    ),
                ]),
            ], md=6),
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button(
                        "Cancelar",
                        id="btn-cancelar-atualizar-selecao",
                        color="link",
                        style={"color": "#333", "fontWeight": "600"}
                    ),
                    dbc.Button(
                        "💾 Atualizar Seleção",
                        id="btn-atualizar-selecao",
                        color="primary",
                        style={"backgroundColor": "#1a3ab8", "border": "none", "fontWeight": "600"}
                    ),
                ], style={"display": "flex", "justifyContent": "flex-end", "gap": "12px"}),
            ),
        ]),
        
        html.Div(id='output-selecao', style={"marginTop": "16px", "fontWeight": "bold"})
    ]),
    style={
        "borderRadius": "12px",
        "border" : "1px solid #e0e0e0",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
    }
)

footer =  html.Footer(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Strong("Copa SQL", style={"color": "#1a7a3c", "fontSize": "18px"}),
                html.P(
                    "© 2026 FIFA World Cup Database Management System. All rights reserved.",
                    style={"color": "#666", "fontSize": "13px", "marginTop": "4px"}
                ),
            ], md=6),

            dbc.Col(
                html.Div([
                    html.A("Privacy Policy",    href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("Terms of Service",  href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("API Documentation", href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("Support",           href="#",                   style={"color": "#333", "fontSize": "13px"}),
                ], style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"}),
            md=6),
        ])
    ], fluid=True),
    style={
        "backgroundColor": "#f8f9fa",
        "borderTop": "1px solid #dee2e6",
        "padding": "24px 40px",
        "marginTop": "auto"
    }
)



tela_selecoes = html.Div([
    dbc.Container([
        dcc.Interval(id='populate-trigger', interval=50, max_intervals=1, n_intervals=0), 
        cabecalho,
        formulario,
    ], style={"maxWidth": "900px"}),
    footer,
], style={"minHeight": "100vh", "display": "flex", "flexDirection": "column"})

if __name__ == "__main__":
    app.run(debug=True)
