from dash import html, dcc
import dash_bootstrap_components as dbc

estilo_label = {
    'fontSize': '13px', 'fontWeight': '600', 'fontFamily': 'monospace',
    'color': '#131b2e', 'marginBottom': '6px', 'display': 'block'
}

estilo_input = {
    'backgroundColor': '#f2f3ff', 'border': '1px solid #bacbb7',
    'borderRadius': '8px', 'padding': '14px 17px', 'fontSize': '15px',
    'width': '100%', 'color': '#131b2e', 'outline': 'none',
    'fontFamily': 'Inter, sans-serif', 'boxSizing': 'border-box'
}

tela_cadastro_selecao = html.Div([

    dbc.Container([

        # Breadcrumb + header
        html.Div([
            html.P([
                html.Span("Admin",                     style={'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Span(" > ",                       style={'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Span("Gerenciamento de Seleções", style={'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Span(" > ",                       style={'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Span("Cadastrar Nova Seleção",    style={'color': '#006e28', 'fontFamily': 'monospace', 'fontSize': '13px', 'fontWeight': '700'}),
            ], style={'marginBottom': '8px', 'textAlign': 'left'}),

            html.H2("Cadastrar Nova Seleção",
                    style={'color': '#131b2e', 'fontWeight': '700', 'fontSize': '30px',
                           'marginBottom': '6px', 'textAlign': 'left'}),
            html.P("Preencha os dados técnicos da federação para incluí-la na base de dados da Copa do Mundo 2026.",
                   style={'color': '#3c4b3b', 'fontSize': '16px', 'textAlign': 'left', 'marginBottom': '24px'}),
        ], style={'maxWidth': '896px', 'margin': '40px auto 0 auto'}),

        # Card do formulário
        html.Div([

            # Acento amarelo no canto superior direito
            html.Div(style={
                'position': 'absolute', 'top': '0', 'right': '0',
                'width': '128px', 'height': '128px', 'opacity': '0.2',
                'borderBottomLeftRadius': '9999px',
                'background': 'linear-gradient(225deg, #ffe16d 0%, rgba(255,225,109,0) 100%)',
                'pointerEvents': 'none'
            }),

            html.Div(id='cadastro-selecao-alert'),

            # Linha 1: Team Name + Continent
            html.Div([
                html.Div([
                    html.Label("Team Name", style=estilo_label),
                    dcc.Input(
                        id='input-nome-selecao', type='text',
                        placeholder='Ex: Brasil, France, etc.',
                        style=estilo_input
                    ),
                ], style={'width': '50%', 'paddingRight': '12px', 'boxSizing': 'border-box'}),

                html.Div([
                    html.Label("Continent", style=estilo_label),
                    dcc.Dropdown(
                        id='input-continente-selecao',
                        options=[
                            {'label': 'CONMEBOL', 'value': 'CONMEBOL'},
                            {'label': 'UEFA',     'value': 'UEFA'},
                            {'label': 'AFC',      'value': 'AFC'},
                            {'label': 'CONCACAF', 'value': 'CONCACAF'},
                            {'label': 'CAF',      'value': 'CAF'},
                            {'label': 'OFC',      'value': 'OFC'},
                        ],
                        placeholder='Select a continent',
                        style={'fontSize': '15px'}
                    ),
                ], style={'width': '50%', 'paddingLeft': '12px', 'boxSizing': 'border-box'}),
            ], style={'display': 'flex', 'marginBottom': '24px'}),

            # Linha 2: Coach + Number of Titles
            html.Div([
                html.Div([
                    html.Label("Coach", style=estilo_label),
                    dcc.Input(
                        id='input-tecnico-selecao', type='text',
                        placeholder='Nome do Treinador',
                        style=estilo_input
                    ),
                ], style={'width': '50%', 'paddingRight': '12px', 'boxSizing': 'border-box'}),

                html.Div([
                    html.Label("Number of Titles", style=estilo_label),
                    html.Div([
                        html.Span("🏆", style={
                            'padding': '0 10px 0 14px', 'fontSize': '16px',
                            'display': 'flex', 'alignItems': 'center',
                            'borderRight': '1px solid #bacbb7',
                        }),
                        dcc.Input(
                            id='input-titulos-selecao', type='number',
                            placeholder='0', min=0, value=0,
                            style={
                                'backgroundColor': 'transparent', 'border': 'none',
                                'fontSize': '15px', 'width': '100%', 'outline': 'none',
                                'padding': '14px', 'color': '#131b2e'
                            }
                        ),
                    ], style={
                        'display': 'flex', 'alignItems': 'center',
                        'backgroundColor': '#f2f3ff', 'border': '1px solid #bacbb7',
                        'borderRadius': '8px', 'height': '52px', 'overflow': 'hidden'
                    }),
                ], style={'width': '50%', 'paddingLeft': '12px', 'boxSizing': 'border-box'}),
            ], style={'display': 'flex', 'marginBottom': '0px'}),

            # Divisor + botões
            html.Hr(style={'borderColor': '#bacbb7', 'margin': '28px 0 24px 0'}),

            html.Div([
                html.Button(
                    "Cancelar",
                    id='btn-cancelar-cadastro-selecao', n_clicks=0,
                    style={
                        'background': 'none', 'border': 'none', 'cursor': 'pointer',
                        'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontWeight': '700',
                        'fontSize': '14px', 'padding': '14px 40px'
                    }
                ),
                html.Button(
                    "✚  Cadastrar Seleção",
                    id='btn-salvar-selecao', n_clicks=0,
                    style={
                        'backgroundColor': '#00df59', 'border': 'none', 'cursor': 'pointer',
                        'borderRadius': '8px', 'color': '#005c20',
                        'fontFamily': 'monospace', 'fontWeight': '700',
                        'fontSize': '14px', 'padding': '14px 40px'
                    }
                ),
            ], style={'display': 'flex', 'justifyContent': 'flex-end', 'gap': '8px'}),

        ], style={
            'position': 'relative', 'overflow': 'hidden',
            'backgroundColor': '#ffffff', 'borderRadius': '12px',
            'border': '1px solid #bacbb7', 'padding': '40px',
            'boxShadow': '0 1px 2px rgba(0,0,0,0.05)',
            'maxWidth': '896px', 'margin': '0 auto 60px auto',
            'textAlign': 'left'
        }),

    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '5%'}),

    html.Footer([
        dbc.Container([
            html.Div([
                html.H5("Copa SQL", style={'color': '#006e28', 'fontWeight': 'bold', 'fontSize': '20px', 'marginBottom': '5px'}),
                html.P("© 2026 FIFA World Cup Database Management System. All rights reserved.",
                       style={'color': '#3c4b3b', 'fontSize': '13px', 'marginBottom': '0'})
            ]),
            html.Div([
                html.A("Privacy Policy",    href="#", style={'color': '#3c4b3b', 'fontSize': '13px', 'marginRight': '20px', 'fontFamily': 'monospace', 'textDecoration': 'underline'}),
                html.A("Terms of Service",  href="#", style={'color': '#3c4b3b', 'fontSize': '13px', 'marginRight': '20px', 'fontFamily': 'monospace', 'textDecoration': 'underline'}),
                html.A("API Documentation", href="#", style={'color': '#3c4b3b', 'fontSize': '13px', 'marginRight': '20px', 'fontFamily': 'monospace', 'textDecoration': 'underline'}),
                html.A("Support",           href="#", style={'color': '#3c4b3b', 'fontSize': '13px', 'fontFamily': 'monospace', 'textDecoration': 'underline'}),
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], fluid=True, style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '30px 5%'})
    ], style={'backgroundColor': '#f2f3ff', 'borderTop': '1px solid #bacbb7', 'marginTop': 'auto'})
])
