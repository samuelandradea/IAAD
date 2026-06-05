from dash import html, dcc
import dash_bootstrap_components as dbc

def _fl():
    return {
        'color': '#4b5563', 'fontSize': '12px',
        'marginRight': '20px', 'textDecoration': 'underline'
    }

PAISES_HOST = [
    {'label': 'Estados Unidos (EUA)', 'value': 'EUA'},
    {'label': 'México',               'value': 'México'},
    {'label': 'Canadá',               'value': 'Canadá'},
    {'label': 'Outro',                'value': 'Outro'},
]

tela_cadastro_estadio = html.Div([

    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'
    ),

    dbc.Container([

        # Cabecalho
        dbc.Row([
            dbc.Col([
                html.H2("Cadastro de Estádio", style={
                    'color': '#111827', 'fontWeight': '700',
                    'fontSize': '28px', 'marginBottom': '8px',
                    'textAlign': 'left'
                }),
                html.P(
                    "Indexação de infraestrutura crítica para a Copa do Mundo FIFA 2026. "
                    "Preencha os detalhes técnicos para integrar o estádio ao sistema central de comando.",
                    style={
                        'color': '#6b7280', 'fontSize': '14px',
                        'maxWidth': '600px', 'textAlign': 'left'
                    }
                ),
            ], md=12),
        ], style={'marginTop': '40px', 'marginBottom': '32px'}),

        # Card do formulario
        dbc.Card([
            dbc.CardBody([

                # Título do card
                html.Div([
                    html.I(className="fa fa-calendar-days me-2",
                           style={'color': '#047857', 'fontSize': '18px'}),
                    html.Span("Informações do Estádio", style={
                        'fontWeight': '700', 'fontSize': '18px', 'color': '#111827'
                    }),
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '24px'}),

                html.Hr(style={'marginBottom': '24px', 'borderColor': '#e5e7eb'}),

                # Nome e Cidade
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Nome do Estádio",
                                  style={'fontWeight': '500', 'fontSize': '13px',
                                         'color': '#374151', 'marginBottom': '6px'}),
                        dbc.Input(
                            id='cadastro-estadio-nome',
                            placeholder='Ex: MetLife Stadium',
                            type='text',
                            style={'borderColor': '#d1d5db', 'borderRadius': '6px',
                                   'fontSize': '14px'}
                        ),
                    ], md=6, className="mb-4"),

                    dbc.Col([
                        dbc.Label("Cidade",
                                  style={'fontWeight': '500', 'fontSize': '13px',
                                         'color': '#374151', 'marginBottom': '6px'}),
                        dbc.Input(
                            id='cadastro-estadio-cidade',
                            placeholder='Ex: New York / New Jersey',
                            type='text',
                            style={'borderColor': '#d1d5db', 'borderRadius': '6px',
                                   'fontSize': '14px'}
                        ),
                    ], md=6, className="mb-4"),
                ]),

                # País e Capacidade
                dbc.Row([
                    dbc.Col([
                        dbc.Label("País Host",
                                  style={'fontWeight': '500', 'fontSize': '13px',
                                         'color': '#374151', 'marginBottom': '6px'}),
                        dcc.Dropdown(
                            id='cadastro-estadio-pais',
                            options=PAISES_HOST,
                            value='EUA',
                            clearable=False,
                            style={'fontSize': '14px'}
                        ),
                    ], md=6, className="mb-4"),

                    dbc.Col([
                        dbc.Label("Capacidade Total",
                                  style={'fontWeight': '500', 'fontSize': '13px',
                                         'color': '#374151', 'marginBottom': '6px'}),
                        dbc.InputGroup([
                            dbc.Input(
                                id='cadastro-estadio-capacidade',
                                placeholder='Ex: 82500',
                                type='number',
                                min=1,
                                style={'borderColor': '#d1d5db', 'borderRadius': '6px 0 0 6px',
                                       'fontSize': '14px'}
                            ),
                            dbc.InputGroupText(
                                "assentos",
                                style={'fontSize': '13px', 'color': '#6b7280',
                                       'backgroundColor': '#f9fafb', 'borderColor': '#d1d5db'}
                            ),
                        ]),
                    ], md=6, className="mb-4"),
                ]),

                # Feedback
                html.Div(id='cadastro-estadio-feedback'),

                html.Hr(style={'margin': '8px 0 24px 0', 'borderColor': '#e5e7eb'}),

                # Botões
                html.Div([
                    dbc.Button(
                        "Cancelar",
                        id='cadastro-estadio-cancelar',
                        color="light",
                        style={
                            'border': '1px solid #d1d5db', 'borderRadius': '8px',
                            'fontWeight': '600', 'fontSize': '14px',
                            'padding': '10px 28px', 'color': '#374151',
                            'marginRight': '12px'
                        }
                    ),
                    dbc.Button(
                        [html.I(className="fa fa-circle-plus me-2"), "Cadastrar Estádio"],
                        id='cadastro-estadio-salvar',
                        style={
                            'backgroundColor': '#16a34a', 'border': 'none',
                            'borderRadius': '8px', 'fontWeight': '600',
                            'fontSize': '14px', 'padding': '10px 28px',
                            'color': '#ffffff',
                            'boxShadow': '0 2px 8px rgba(22,163,74,0.3)'
                        }
                    ),
                ], style={'display': 'flex', 'justifyContent': 'flex-end'}),

            ], style={'padding': '32px'}),
        ], style={
            'borderRadius': '12px', 'border': '1px solid #e5e7eb',
            'boxShadow': '0 2px 8px rgba(0,0,0,0.04)',
            'backgroundColor': '#ffffff', 'marginBottom': '60px'
        }),

    ], fluid=False, style={'maxWidth': '1000px'}),

    # Footer
    html.Footer([
        dbc.Container([
            html.Div([
                html.Span("Copa SQL 2026", style={
                    'color': '#15803d', 'fontWeight': '700', 'fontSize': '16px'
                }),
                html.P("© 2026 FIFA World Cup. Technical Infrastructure by Copa SQL.",
                       style={'color': '#6b7280', 'fontSize': '12px', 'marginBottom': '0'}),
            ]),
            html.Div([
                html.A("Legal",            href="#", style=_fl()),
                html.A("Privacy Policy",   href="#", style=_fl()),
                html.A("API Docs",         href="#", style=_fl()),
                html.A("Tournament Rules", href="#", style={**_fl(), 'marginRight': '0'}),
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], fluid=True, style={
            'display': 'flex', 'justifyContent': 'space-between',
            'alignItems': 'center', 'padding': '28px 5%'
        })
    ], style={
        'backgroundColor': '#f9fafb', 'borderTop': '1px solid #e5e7eb', 'marginTop': 'auto'
    }),
])