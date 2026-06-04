from dash import html, dcc
import dash_bootstrap_components as dbc

tela_selecoes = html.Div([

    dcc.Store(id='selecoes-pagina-atual', data=1),

    dbc.Container([

        dbc.Row([
            dbc.Col([
                html.P("Admin > Gerenciamento de Seleções", style={'color': '#0035c6', 'fontSize': '14px', 'fontFamily': 'monospace', 'marginBottom': '4px'}),
                html.H2("Gerenciamento de Seleções", style={'color': '#131b2e', 'fontWeight': '700', 'fontSize': '28px', 'marginBottom': '5px'}),
                html.P("Administre as federações participantes, seus status de qualificação e detalhes técnicos para a Copa do Mundo 2026.",
                       style={'color': '#3c4b3b', 'fontSize': '14px'})
            ], lg=8, md=7, sm=12),
            dbc.Col([
                dbc.Button("+ Cadastrar Nova Seleção", color="success",
                           style={'backgroundColor': '#006e28', 'border': 'none', 'padding': '12px 24px',
                                  'borderRadius': '8px', 'fontWeight': '600', 'fontSize': '14px'})
            ], lg=4, md=5, sm=12, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end'}),
        ], style={'marginTop': '40px', 'marginBottom': '30px'}),

        html.Div([

            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("SELEÇÃO",       style={'padding': '14px 24px', 'color': '#3c4b3b', 'fontSize': '13px', 'fontWeight': '700', 'fontFamily': 'monospace', 'textTransform': 'uppercase', 'borderBottom': '2px solid #0035c6', 'width': '30%'}),
                        html.Th("CONFEDERAÇÃO",  style={'padding': '14px 24px', 'color': '#3c4b3b', 'fontSize': '13px', 'fontWeight': '700', 'fontFamily': 'monospace', 'textTransform': 'uppercase', 'borderBottom': '2px solid #0035c6', 'width': '25%'}),
                        html.Th("TÍTULOS",       style={'padding': '14px 24px', 'color': '#3c4b3b', 'fontSize': '13px', 'fontWeight': '700', 'fontFamily': 'monospace', 'textTransform': 'uppercase', 'borderBottom': '2px solid #0035c6', 'width': '25%'}),
                        html.Th("AÇÕES",         style={'padding': '14px 24px', 'color': '#3c4b3b', 'fontSize': '13px', 'fontWeight': '700', 'fontFamily': 'monospace', 'textTransform': 'uppercase', 'borderBottom': '2px solid #0035c6', 'textAlign': 'center', 'width': '20%'}),
                    ]),
                    style={'backgroundColor': '#f2f3ff'}
                ),
                html.Tbody(id='tabela-selecoes-body'),
            ], borderless=True, hover=True, style={'marginBottom': '0px', 'width': '100%', 'tableLayout': 'fixed'}),

            html.Div([
                html.Span(id='selecoes-info-texto', style={'color': '#3c4b3b', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Div(id='selecoes-botoes-pagina', style={'display': 'flex', 'alignItems': 'center'})
            ], style={
                'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                'padding': '15px 20px', 'borderTop': '1px solid #bacbb7', 'backgroundColor': '#f2f3ff'
            })

        ], style={
            'backgroundColor': '#faf8ff', 'borderRadius': '12px', 'overflow': 'hidden',
            'boxShadow': '0 1px 2px rgba(0,0,0,0.05)',
            'border': '1px solid #bacbb7', 'marginBottom': '60px', 'width': '100%'
        })

    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '5%'}),

    html.Footer([
        dbc.Container([
            html.Div([
                html.H5("Copa SQL", style={'color': '#006e28', 'fontWeight': 'bold', 'fontSize': '20px', 'marginBottom': '5px'}),
                html.P("© 2026 FIFA World Cup Database Management System. All rights reserved.", style={'color': '#3c4b3b', 'fontSize': '13px', 'marginBottom': '0'})
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
