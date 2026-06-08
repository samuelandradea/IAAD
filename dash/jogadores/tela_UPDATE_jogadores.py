from dash import html, dcc
import dash_bootstrap_components as dbc

def build_tela_editar(nome, id_selecao, opcoes_selecao, numero, posicao, data_str):
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2("Atualizar Jogador", style={'color': '#111827', 'fontWeight': '700', 'fontSize': '28px', 'marginBottom': '5px'}),
                        html.P("Atualize os dados técnicos do atleta na base de dados oficial da FIFA World Cup 2026.",
                               style={'color': '#6b7280', 'fontSize': '14px', 'marginBottom': '30px'}),

                        html.Div([

                            html.Div([
                                html.Label("Nome Completo", style={'fontSize': '12px', 'color': '#6b7280', 'marginBottom': '6px', 'display': 'block'}),
                                dbc.Input(id='edit-nome', value=nome, type='text',
                                          style={'borderRadius': '8px', 'border': '1px solid #d1d5db'}),
                            ], style={'marginBottom': '20px'}),

                            dbc.Row([
                                dbc.Col([
                                    html.Label("Seleção Nacional", style={'fontSize': '12px', 'color': '#6b7280', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Dropdown(id='edit-selecao', options=opcoes_selecao, value=id_selecao),
                                ], width=6),
                                dbc.Col([
                                    html.Label("Número da Camisa", style={'fontSize': '12px', 'color': '#6b7280', 'marginBottom': '6px', 'display': 'block'}),
                                    dbc.Input(id='edit-numero', value=numero, type='number',
                                              style={'borderRadius': '8px', 'border': '1px solid #d1d5db'}),
                                ], width=6),
                            ], style={'marginBottom': '20px'}),

                            dbc.Row([
                                dbc.Col([
                                    html.Label("Posição", style={'fontSize': '12px', 'color': '#6b7280', 'marginBottom': '6px', 'display': 'block'}),
                                    dcc.Dropdown(id='edit-posicao', value=posicao, options=[
                                        {'label': 'Goleiro',    'value': 'Goleiro'},
                                        {'label': 'Defensor',   'value': 'Defensor'},
                                        {'label': 'Meio-campo', 'value': 'Meio-campo'},
                                        {'label': 'Atacante',   'value': 'Atacante'},
                                    ]),
                                ], width=6),
                                dbc.Col([
                                    html.Label("Data de Nascimento", style={'fontSize': '12px', 'color': '#6b7280', 'marginBottom': '6px', 'display': 'block'}),
                                    dbc.Input(id='edit-data-nascimento', value=data_str, type='text',
                                              placeholder='DD/MM/AAAA',
                                              style={'borderRadius': '8px', 'border': '1px solid #d1d5db'}),
                                ], width=6),
                            ], style={'marginBottom': '30px'}),

                            html.Div(id='edit-jogador-feedback'),

                            html.Div([
                                dbc.Button("Cancelar", id='btn-cancelar-edicao', color="light",
                                           style={'marginRight': '12px', 'border': '1px solid #d1d5db', 'borderRadius': '8px'}),
                                dbc.Button([html.Span("✏️", style={'marginRight': '6px'}), "Atualizar Jogador"],
                                           id='btn-confirmar-edicao', color="primary",
                                           style={'backgroundColor': '#2563eb', 'border': 'none', 'borderRadius': '8px'}),
                            ], style={'display': 'flex', 'justifyContent': 'flex-end'}),

                        ], style={
                            'backgroundColor': '#ffffff', 'borderRadius': '12px',
                            'padding': '30px', 'border': '1px solid #e5e7eb',
                            'boxShadow': '0 1px 3px rgba(0,0,0,0.05)'
                        })
                    ])
                ], lg=8, md=10, sm=12)
            ], justify='center', style={'marginTop': '60px', 'marginBottom': '60px'})
        ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '5%'}),
    ])