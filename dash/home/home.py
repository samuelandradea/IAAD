from dash import html
import dash_bootstrap_components as dbc

#componente tela home

tela_home = html.Div([
    dbc.Container([
        dbc.Row([
            
            
            #coluna esquerda
            
            dbc.Col([
                
                #Tag superior (Badge)
                html.Div([
                    
                    html.Div(style={
                        'width': '14px', 'height': '14px', 'backgroundColor': 'Green', 
                        'borderRadius': '50%', 'display': 'inline-block', 'marginRight': '8px',
                        'verticalAlign': 'middle'
                    }),
                    html.Span("Dashboard copa do mundo", style={
                        'color': '#065f46', 'fontWeight': '600', 'fontSize': '12px', 'verticalAlign': 'middle'
                    })
                ], style={
                    'backgroundColor': '#d1fae5', 'padding': '6px 16px', 'borderRadius': '20px', 
                    'display': 'inline-block', 'marginBottom': '25px', 'border': '1px solid #a7f3d0'
                }),
                
                #Título Principal
                html.H1([
                    html.Span("Copa ", style={'color': '#111827', 'fontWeight': '900', 'fontSize': '64px'}),
                    html.Span("SQL", style={'color': '#15803d', 'fontWeight': '900', 'fontSize': '64px'})
                ], style={'marginBottom': '15px', 'fontFamily': 'sans-serif'}),
                
                #Subtítulo / Descrição
                html.P(
                    "Sistema de Gerenciamento de banco de dados para a Copa do "
                    "mundo de 2026. A unified command center for high-stakes sports "
                    "analytics and real-time tournament operations.",
                    style={
                        'color': '#4b5563', 'fontSize': '18px', 'lineHeight': '1.6', 
                        'maxWidth': '90%', 'marginBottom': '40px','textAlign': 'left',
                        
                    }
                ),
                
                
                html.Div([
                    dbc.Button(
                        "Dashboard", 
                        color="success", 
                        className="me-3", 
                        style={
                            'backgroundColor': '#059669', 'border': 'none', 
                            'padding': '12px 32px', 'borderRadius': '8px', 
                            'fontWeight': 'bold', 'fontSize': '18px'
                        }
                    ),
                    dbc.Button(
                        "Documentação", 
                        outline=True, 
                        color="primary", 
                        style={
                            'border': '2px solid #2563eb', 'color': '#2563eb', 
                            'padding': '10px 32px', 'borderRadius': '8px', 
                            'fontWeight': 'bold', 'fontSize': '18px', 'backgroundColor': 'transparent'
                        }
                    )
                ], style={'display': 'flex'})
                
            ], lg=5, md=12, style={'paddingTop': '80px', 'paddingBottom': '80px','textAlign': 'left'}), 
            
           #coluna direita
            dbc.Col([
                html.Div([
                    
                    
                    html.Div([
                        
                       
                        html.Div([
                            html.Span("QUERY_EDITOR.SQL", style={
                                'fontFamily': 'monospace', 'fontSize': '13px', 'color': '#2563eb', 'fontWeight': 'bold'
                            }),
                            html.Div([
                                html.Span(style={'width': '12px', 'height': '12px', 'backgroundColor': '#ef4444', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                                html.Span(style={'width': '12px', 'height': '12px', 'backgroundColor': '#eab308', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                                html.Span(style={'width': '12px', 'height': '12px', 'backgroundColor': '#22c55e', 'borderRadius': '50%', 'display': 'inline-block', 'marginLeft': '6px'}),
                            ])
                        ], style={
                            'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 
                            'borderBottom': '1px solid #e5e7eb', 'paddingBottom': '15px', 'marginBottom': '20px'
                        }),
                        
                        
                        html.Div([
                            html.Div([html.Span("SELECT ", style={'color': '#2563eb', 'fontWeight': 'bold'}), "stadium_name, capacity"], style={'marginBottom': '10px'}),
                            html.Div([html.Span("FROM ", style={'color': '#2563eb', 'fontWeight': 'bold'}), "world_cup_2026.venues"], style={'marginBottom': '10px'}),
                            html.Div([html.Span("WHERE ", style={'color': '#2563eb', 'fontWeight': 'bold'}), "host_country = ", html.Span("'Mexico'", style={'color': '#16a34a'})], style={'marginBottom': '10px'}),
                            html.Div([html.Span("ORDER BY ", style={'color': '#2563eb', 'fontWeight': 'bold'}), "capacity ", html.Span("DESC", style={'color': '#2563eb', 'fontWeight': 'bold'}), ";"], style={'marginBottom': '10px'}),
                        ], style={'fontFamily': 'monospace', 'fontSize': '14px', 'color': '#374151'}),
                        
                        
                        html.Div([
                            html.Div([
                                html.Div(style={'width': '67%', 'backgroundColor': '#15803d', 'height': '100%', 'borderRadius': '4px'}),
                            ], style={'width': '100%', 'backgroundColor': '#e0e7ff', 'height': '8px', 'borderRadius': '4px', 'marginBottom': '10px'}),
                            
                            html.Div([
                                html.Span("Querying Live Nodes...", style={'color': '#6b7280', 'fontSize': '11px'}),
                                html.Span("67%", style={'color': '#15803d', 'fontWeight': 'bold', 'fontSize': '11px'})
                            ], style={'display': 'flex', 'justifyContent': 'space-between', 'fontFamily': 'monospace'})
                        ], style={'marginTop': '40px'})
                        
                    ], style={
                       
                        'backgroundColor': '#ffffff', 'padding': '30px', 'borderRadius': '12px',
                        'boxShadow': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                        'width': '85%', 'border': '1px solid #f3f4f6'
                    })
                    
                ], style={
                    
                    'backgroundColor': '#e8f3e2', 
                    'backgroundImage': 'linear-gradient(135deg, #e8f3e2 0%, #d4e8c9 100%)',
                    'height': '100%', 'minHeight': '600px',
                    'borderTopLeftRadius': '40px', 'borderBottomLeftRadius': '40px',
                    'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
                })
            ], lg=7, md=12, style={'paddingRight': '0px'}) 
        ], className="align-items-center") 
    ], fluid=True, style={'paddingLeft': '5%', 'paddingRight': '0px'})
])