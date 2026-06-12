from dash import html
import dash_bootstrap_components as dbc

tela_jogadores = html.Div([

    dbc.Container([

        dbc.Row([
            dbc.Col([
                html.H2("Player Management", style={'color': '#111827', 'fontWeight': '700', 'fontSize': '28px', 'marginBottom': '5px'}),
                html.P("Registry of all competing athletes for the FIFA World Cup 2026 database.", style={'color': '#6b7280', 'fontSize': '14px'})
            ], lg=8, md=7, sm=12),
            dbc.Col([
                dbc.Button(
                    "+ Cadastrar Novo Jogador",
                    id='btn-ir-cadastro',
                    color="success",
                    style={
                        'backgroundColor': '#047857', 'border': 'none', 'padding': '10px 20px',
                        'borderRadius': '8px', 'fontWeight': '600', 'fontSize': '14px'
                    }
                )
            ], lg=4, md=5, sm=12, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end'}),
        ], style={'marginTop': '40px', 'marginBottom': '30px'}),

        html.Div([

            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("NOME",          style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'width': '30%'}),
                        html.Th("POSIÇÃO",      style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'width': '20%'}),
                        html.Th("NÚMERO DA CAMISA",  style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'width': '15%'}),
                        html.Th("SELEÇÃO NACIONAL", style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'width': '15%'}),
                        html.Th("IDADE",           style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'width': '10%'}),
                        html.Th("AÇÕES",       style={'padding': '12px 16px', 'color': '#4b5563', 'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em', 'textAlign': 'right', 'width': '10%'}),
                    ]),
                    style={'backgroundColor': '#eff6ff', 'borderBottom': '1px solid #e5e7eb'}
                ),
                html.Tbody(id='tabela-jogadores-body'),
            ], borderless=True, hover=True, style={'marginBottom': '0px', 'width': '100%', 'tableLayout': 'fixed'}),

            html.Div([
                html.Span(id='jogadores-info-texto', style={'color': '#6b7280', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Div(id='jogadores-botoes-pagina', style={'display': 'flex', 'alignItems': 'center'})
            ], style={
                'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                'padding': '15px 20px', 'borderTop': '1px solid #e5e7eb', 'backgroundColor': '#ffffff'
            })

        ], style={
            'backgroundColor': '#ffffff', 'borderRadius': '12px', 'overflow': 'hidden',
            'boxShadow': '0 4px 6px -1px rgba(0,0,0,0.05)',
            'border': '1px solid #e5e7eb', 'marginBottom': '60px', 'width': '100%'
        })

    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '5%'}),

    html.Footer([
        dbc.Container([
            html.Div([
                html.H5("Copa SQL", style={'color': '#111827', 'fontWeight': 'bold', 'fontSize': '18px', 'marginBottom': '5px'}),
                html.P("© 2026 FIFA World Cup Database Management System. All rights reserved.", style={'color': '#6b7280', 'fontSize': '12px', 'marginBottom': '0'})
            ]),
            html.Div([
                html.A("Privacy Policy",    href="#", style={'color': '#4b5563', 'fontSize': '12px', 'marginRight': '20px', 'textDecoration': 'underline'}),
                html.A("Terms of Service",  href="#", style={'color': '#4b5563', 'fontSize': '12px', 'marginRight': '20px', 'textDecoration': 'underline'}),
                html.A("API Documentation", href="#", style={'color': '#4b5563', 'fontSize': '12px', 'marginRight': '20px', 'textDecoration': 'underline'}),
                html.A("Support",           href="#", style={'color': '#4b5563', 'fontSize': '12px', 'textDecoration': 'underline'}),
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], fluid=True, style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '30px 5%'})
    ], style={'backgroundColor': '#f9fafb', 'borderTop': '1px solid #e5e7eb', 'marginTop': 'auto'})
])