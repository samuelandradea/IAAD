from dash import html, dcc
import dash_bootstrap_components as dbc

cabecalho = html.Div([
    html.H2("Atualização de Estádio", style={"fontWeight": "700", "marginTop": "40px"}),
    html.P(
        "Indexação de infraestrutura crítica para a Copa do Mundo FIFA 2026. "
        "Preencha os detalhes técnicos para integrar o estádio ao sistema central de comando.",
        style={"color": "#555", "marginBottom": "24px"}
    ),
])


formulario = dbc.Card(
    dbc.CardBody([
        html.Div([
            html.Span("🏟️", style={"marginRight": "8px"}),
            html.Strong("Informações do Estádio", style={"fontSize": "18px"}),
        ], style={"marginBottom": "24px"}),

        dbc.Row([
            dbc.Col([
                dbc.Label("Nome do Estádio"),
                dbc.Input(
                    id="input-estadio-nome",
                    type="text",
                    placeholder="Ex: MetLife Stadium",
                    style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                ),
            ], md=6),

            dbc.Col([
                dbc.Label("Cidade"),
                dbc.Input(
                    id="input-estadio-cidade",
                    type="text",
                    placeholder="Ex: New York / New Jersey",
                    style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                ),
            ], md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Label("País Host"),
                dcc.Dropdown(
                    id="dropdown-estadio-pais",
                    options=[
                        {"label": "Estados Unidos (EUA)", "value": "eua"},
                        {"label": "México",               "value": "mexico"},
                        {"label": "Canadá",               "value": "canada"},
                    ],
                    value="eua",
                    style={"backgroundColor": "#f0f2ff"}
                ),
            ], md=6),

            dbc.Col([
                dbc.Label("Capacidade Total"),
                dbc.InputGroup([
                    dbc.Input(
                        id="input-estadio-capacidade",
                        type="number",
                        placeholder="Ex: 82500",
                        min=0,
                        style={"backgroundColor": "#f0f2ff", "border": "1px solid #d0d5ff"}
                    ),
                    dbc.InputGroupText("assentos"),
                ]),
            ], md=6),
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Button(
                        "Cancelar",
                        id="btn-estadio-cancelar",
                        color="link",
                        style={"color": "#333", "fontWeight": "600", "border": "1px solid #ccc"}
                    ),
                    dbc.Button(
                        "⊕ Atualizar Estádio",
                        id="btn-estadio-cadastrar",
                        style={"backgroundColor": "#1a3ab8", "border": "none", "fontWeight": "600", "color": "white"}
                    ),
                ], style={"display": "flex", "justifyContent": "flex-end", "gap": "12px"}),
            ),
        ]),
        html.Div(id='output-estadio', style={"marginTop": "16px", "fontWeight": "bold"})
    ]),
    style={
        "borderRadius": "12px",
        "border": "1px solid #e0e0e0",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
    }
)

footer = html.Footer(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Strong("Copa SQL 2026", style={"color": "#1a7a3c", "fontSize": "18px"}),
                html.P(
                    "© 2026 FIFA World Cup. Technical Infrastructure by Copa SQL.",
                    style={"color": "#666", "fontSize": "13px", "marginTop": "4px"}
                ),
            ], md=6),
            dbc.Col(
                html.Div([
                    html.A("Legal",             href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("Privacy Policy",    href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("API Docs",          href="#", className="me-3", style={"color": "#333", "fontSize": "13px"}),
                    html.A("Tournament Rules",  href="#",                   style={"color": "#333", "fontSize": "13px"}),
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

tela_estadios = html.Div([
    dbc.Container([
        cabecalho,
        formulario,
    ], style={"maxWidth": "900px"}),
    footer,
], style={"minHeight": "100vh", "display": "flex", "flexDirection": "column"})