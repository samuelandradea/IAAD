from dash import html
import dash_bootstrap_components as dbc



tela_home = html.Div([

    # ── HERO ────────────────────────────────────────────────────────────────
    dbc.Container([
        dbc.Row([

            # Coluna esquerda
            dbc.Col([

                html.Div([
                    html.Div(style={
                        'width': '10px', 'height': '10px', 'backgroundColor': '#00df59',
                        'borderRadius': '50%', 'display': 'inline-block',
                        'marginRight': '8px', 'verticalAlign': 'middle'
                    }),
                    html.Span("Copa do Mundo 2026 · Sistema de Gestão", style={
                        'color': '#065f46', 'fontWeight': '600', 'fontSize': '12px',
                        'verticalAlign': 'middle', 'fontFamily': 'monospace'
                    })
                ], style={
                    'backgroundColor': '#d1fae5', 'padding': '6px 16px',
                    'borderRadius': '20px', 'display': 'inline-block',
                    'marginBottom': '28px', 'border': '1px solid #a7f3d0'
                }),

                html.H1([
                    html.Span("Copa ", style={'color': '#131b2e', 'fontWeight': '900', 'fontSize': '62px'}),
                    html.Span("SQL", style={'color': '#00df59', 'fontWeight': '900', 'fontSize': '62px'}),
                ], style={'marginBottom': '8px', 'lineHeight': '1.1'}),

                html.P(
                    "Gerencie seleções, estádios, jogadores e partidas da Copa do Mundo 2026 "
                    "em um único painel. Dados em tempo real, operações seguras e interface intuitiva.",
                    style={
                        'color': '#3c4b3b', 'fontSize': '17px', 'lineHeight': '1.7',
                        'maxWidth': '480px', 'marginBottom': '40px'
                    }
                ),

                html.Div([
                    html.Button("⚽  Ver Seleções", id='hero-btn-selecoes', n_clicks=0, style={
                        'backgroundColor': '#00df59', 'border': 'none', 'cursor': 'pointer',
                        'borderRadius': '8px', 'color': '#004d1a', 'fontWeight': '700',
                        'fontSize': '15px', 'padding': '13px 32px', 'marginRight': '12px',
                        'fontFamily': 'monospace'
                    }),
                    html.Button("🏟  Ver Estádios", id='hero-btn-estadios', n_clicks=0, style={
                        'backgroundColor': 'transparent', 'border': '2px solid #bacbb7',
                        'cursor': 'pointer', 'borderRadius': '8px', 'color': '#131b2e',
                        'fontWeight': '700', 'fontSize': '15px', 'padding': '11px 32px',
                        'fontFamily': 'monospace'
                    }),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '8px'}),

            ], lg=5, md=12, style={'paddingTop': '80px', 'paddingBottom': '40px', 'textAlign': 'left'}),

            # Coluna direita — painel SQL
            dbc.Col([
                html.Div([
                    html.Div([

                        # Barra de título do editor
                        html.Div([
                            html.Span("COPA_SQL · QUERY_EDITOR", style={
                                'fontFamily': 'monospace', 'fontSize': '12px',
                                'color': '#006e28', 'fontWeight': '700', 'letterSpacing': '0.05em'
                            }),
                            html.Div([
                                html.Span(style={'width': '11px', 'height': '11px', 'backgroundColor': '#ef4444', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                                html.Span(style={'width': '11px', 'height': '11px', 'backgroundColor': '#eab308', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                                html.Span(style={'width': '11px', 'height': '11px', 'backgroundColor': '#22c55e', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                            ])
                        ], style={
                            'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
                            'borderBottom': '1px solid #e5e7eb', 'paddingBottom': '14px', 'marginBottom': '20px'
                        }),

                        # Código SQL
                        html.Div([
                            html.Div([html.Span("SELECT  ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("s.nome, s.continente, s.tecnico,", style={'color': '#374151'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("        ", style={}), html.Span("COUNT(j.id) AS total_jogadores", style={'color': '#374151'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("FROM    ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("selecao s", style={'color': '#374151'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("JOIN    ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("jogador j ", style={'color': '#374151'}), html.Span("ON ", style={'color': '#9333ea', 'fontWeight': 'bold'}), html.Span("j.selecao_id = s.id", style={'color': '#374151'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("WHERE   ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("s.continente = ", style={'color': '#374151'}), html.Span("'América do Sul'", style={'color': '#16a34a'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("GROUP BY ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("s.id", style={'color': '#374151'})], style={'marginBottom': '6px'}),
                            html.Div([html.Span("ORDER BY ", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span("s.titulos ", style={'color': '#374151'}), html.Span("DESC", style={'color': '#2563eb', 'fontWeight': 'bold'}), html.Span(";", style={'color': '#374151'})]),
                        ], style={'fontFamily': 'monospace', 'fontSize': '13px', 'lineHeight': '1.8', 'color': '#374151'}),

                        # Barra de progresso
                        html.Div([
                            html.Div([
                                html.Div(style={'width': '82%', 'backgroundColor': '#00df59', 'height': '100%', 'borderRadius': '4px'}),
                            ], style={'width': '100%', 'backgroundColor': '#e5e7eb', 'height': '6px', 'borderRadius': '4px', 'marginBottom': '8px'}),
                            html.Div([
                                html.Span("✓ 32 rows returned", style={'color': '#6b7280', 'fontSize': '11px', 'fontFamily': 'monospace'}),
                                html.Span("0.04s", style={'color': '#00df59', 'fontWeight': '700', 'fontSize': '11px', 'fontFamily': 'monospace'})
                            ], style={'display': 'flex', 'justifyContent': 'space-between'})
                        ], style={'marginTop': '28px'})

                    ], style={
                        'backgroundColor': '#ffffff', 'padding': '28px',
                        'borderRadius': '14px',
                        'boxShadow': '0 20px 40px rgba(0,0,0,0.10)',
                        'width': '88%', 'border': '1px solid #e5e7eb'
                    })
                ], style={
                    'backgroundColor': '#eaf5e4',
                    'backgroundImage': 'linear-gradient(135deg, #eaf5e4 0%, #d4edca 100%)',
                    'height': '100%', 'minHeight': '520px',
                    'borderTopLeftRadius': '40px', 'borderBottomLeftRadius': '40px',
                    'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
                })
            ], lg=7, md=12, style={'paddingRight': '0px'})

        ], className="align-items-center")
    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '0px', 'backgroundColor': '#ffffff'}),

])
