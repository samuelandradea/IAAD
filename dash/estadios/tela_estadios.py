from dash import html, dcc
import dash_bootstrap_components as dbc

def _th():
    return {
        'padding': '12px 16px', 'color': '#4b5563',
        'fontSize': '12px', 'fontWeight': '600', 'letterSpacing': '0.05em'
    }

def _footer_link():
    return {
        'color': '#4b5563', 'fontSize': '12px',
        'marginRight': '20px', 'textDecoration': 'underline'
    }

tela_estadios = html.Div([

    dcc.Store(id='estadios-pagina-atual', data=1),

    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'
    ),

    dbc.Container([

        # Cabecalho
        dbc.Row([
            dbc.Col([
                html.H2("Gerenciamento de Estádios", style={
                    'color': '#111827', 'fontWeight': '700',
                    'fontSize': '28px', 'marginBottom': '5px'
                }),
                html.P(
                    "Controle de infraestrutura e capacidades para a Copa do Mundo 2026.",
                    style={'color': '#6b7280', 'fontSize': '14px'}
                ),
            ], lg=8, md=7, sm=12),

            dbc.Col([
                dbc.Button(
                    [html.I(className="fa fa-plus me-2"), "Cadastrar Novo Estádio"],
                    id='btn-ir-cadastro-estadio',
                    color="success",
                    n_clicks=0,
                    style={
                        'backgroundColor': '#047857', 'border': 'none',
                        'padding': '10px 20px', 'borderRadius': '8px',
                        'fontWeight': '600', 'fontSize': '14px'
                    }
                )
            ], lg=4, md=5, sm=12, style={
                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'flex-end'
            }),
        ], style={'marginTop': '40px', 'marginBottom': '30px'}),

        # Tabela
        html.Div([
            dbc.Table([
                html.Thead(
                    html.Tr([
                        html.Th("NOME",       style=_th()),
                        html.Th("CIDADE",     style=_th()),
                        html.Th("PAÍS",       style=_th()),
                        html.Th("CAPACIDADE", style=_th()),
                        html.Th("AÇÕES",      style={**_th(), 'textAlign': 'right', 'width': '10%'}),
                    ]),
                    style={'backgroundColor': '#eff6ff', 'borderBottom': '1px solid #e5e7eb'}
                ),
                html.Tbody(id='tabela-estadios-body'),
            ], borderless=True, hover=True,
               style={'marginBottom': '0px', 'width': '100%', 'tableLayout': 'fixed'}),

            html.Div([
                html.Span(id='estadios-info-texto',
                          style={'color': '#6b7280', 'fontFamily': 'monospace', 'fontSize': '13px'}),
                html.Div(id='estadios-botoes-pagina',
                         style={'display': 'flex', 'alignItems': 'center'})
            ], style={
                'display': 'flex', 'justifyContent': 'space-between',
                'alignItems': 'center', 'padding': '15px 20px',
                'borderTop': '1px solid #e5e7eb', 'backgroundColor': '#ffffff'
            })
        ], style={
            'backgroundColor': '#ffffff', 'borderRadius': '12px',
            'overflow': 'hidden', 'boxShadow': '0 4px 6px -1px rgba(0,0,0,0.05)',
            'border': '1px solid #e5e7eb', 'marginBottom': '60px', 'width': '100%'
        }),

    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '5%'}),

    # Modal de confirmação de exclusão
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle("Confirmar Exclusão",
                           style={'color': '#111827', 'fontWeight': '700'})
        ),
        dbc.ModalBody(
            html.P("Tem certeza que deseja excluir este estádio? Esta ação não pode ser desfeita.",
                   style={'color': '#4b5563'})
        ),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id='btn-cancelar-delete-estadio',
                       color="light", className="me-2",
                       style={'border': '1px solid #d1d5db'}),
            dbc.Button(
                [html.I(className="fa fa-trash me-2"), "Excluir"],
                id='btn-confirmar-delete-estadio',
                style={'backgroundColor': '#dc2626', 'border': 'none', 'fontWeight': '600'}
            ),
        ]),
    ], id='modal-confirmar-delete-estadio', is_open=False, centered=True),

    dcc.Store(id='estadio-delete-id', data=None),

    # Footer
    html.Footer([
        dbc.Container([
            html.Div([
                html.H5("Copa SQL", style={
                    'color': '#111827', 'fontWeight': 'bold',
                    'fontSize': '18px', 'marginBottom': '5px'
                }),
                html.P("© 2026 FIFA World Cup Database Management System. All rights reserved.",
                       style={'color': '#6b7280', 'fontSize': '12px', 'marginBottom': '0'})
            ]),
            html.Div([
                html.A("Privacy Policy",    href="#", style=_footer_link()),
                html.A("Terms of Service",  href="#", style=_footer_link()),
                html.A("API Documentation", href="#", style=_footer_link()),
                html.A("Support",           href="#", style={**_footer_link(), 'marginRight': '0'}),
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], fluid=True, style={
            'display': 'flex', 'justifyContent': 'space-between',
            'alignItems': 'center', 'padding': '30px 5%'
        })
    ], style={'backgroundColor': '#f9fafb', 'borderTop': '1px solid #e5e7eb', 'marginTop': 'auto'}),
])