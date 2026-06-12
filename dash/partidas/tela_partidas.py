from dash import html, dcc
import dash_bootstrap_components as dbc

card_style = {
    "padding": "20px", 
    "borderRadius": "8px", 
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
    "backgroundColor": "#fcfcfd",
    "border": "1px solid #eaeaea",
    "minHeight": "100px"
}

card_highlight_style = card_style.copy()
card_highlight_style.update({
    "backgroundColor": "#e8fdf2", 
    "borderColor": "#16a34a"
})

tela_partidas = html.Div([

    html.Div([
        html.Div([
            html.H2("Gerenciamento de Partidas", style={"fontWeight": "bold", "color": "#111827", "margin": "0 0 5px 0", "textAlign": "left"}),
            html.P("Monitore e organize os confrontos da Copa do Mundo FIFA 2026.", style={"color": "#6b7280", "margin": "0", "textAlign": "left"}),
        ]),
        html.Button("+ Cadastrar Nova Partida", id="btn-cadastrar-partida", style={
            "backgroundColor": "#059669", "color": "white", "border": "none", 
            "padding": "10px 20px", "borderRadius": "5px", "fontWeight": "bold", "cursor": "pointer"
        })
    ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "30px"}),


    dbc.Row([
        dbc.Col(html.Div([
            html.P("TOTAL DE PARTIDAS", style={"color": "#6b7280", "fontSize": "12px", "fontWeight": "bold", "marginBottom": "10px"}),
            html.H3("0", id="kpi-total-partidas", style={"margin": "0", "color": "#111827", "fontWeight": "bold"})
        ], style=card_style), width=3),
        dbc.Col(html.Div([
            html.P("ESTÁDIOS ATIVOS", style={"color": "#6b7280", "fontSize": "12px", "fontWeight": "bold", "marginBottom": "10px"}),
            html.H3("0", id="kpi-estadios-ativos", style={"margin": "0", "color": "#111827", "fontWeight": "bold"})
        ], style=card_style), width=3),
        dbc.Col(html.Div([
            html.P("TIMES INSCRITOS", style={"color": "#6b7280", "fontSize": "12px", "fontWeight": "bold", "marginBottom": "10px"}),
            html.H3("0", id="kpi-times-inscritos", style={"margin": "0", "color": "#111827", "fontWeight": "bold"})
        ], style=card_style), width=3),
        dbc.Col(html.Div([
            html.P("PARTIDA DE ABERTURA", style={"color": "#059669", "fontSize": "12px", "fontWeight": "bold", "marginBottom": "10px"}),
            html.P("-", id="kpi-partida-abertura", style={"margin": "0", "color": "#047857", "fontWeight": "bold"})
        ], style=card_highlight_style), width=3),
    ], style={"marginBottom": "30px", "marginLeft": "0", "marginRight": "0"}),


    html.Div([
        html.Table([
            html.Thead(
                html.Tr([
                    html.Th("N° DA PARTIDA", style={"padding": "15px", "textAlign": "left", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("DATA", style={"padding": "15px", "textAlign": "left", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("ESTÁDIO", style={"padding": "15px", "textAlign": "left", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("TIME 1", style={"padding": "15px", "textAlign": "left", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("TIME 2", style={"padding": "15px", "textAlign": "left", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("PLACAR", style={"padding": "15px", "textAlign": "center", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                    html.Th("AÇÕES", style={"padding": "15px", "textAlign": "right", "color": "#6b7280", "fontSize": "12px", "borderBottom": "1px solid #eaeaea"}),
                ])
            ),

            html.Tbody(id="tabela-partidas-body")
        ], style={"width": "100%", "borderCollapse": "collapse", "textAlign": "left"}),
        

        html.Div([
            html.Span(id="texto-paginacao-partidas", children="Mostrando 0 partidas", style={"color": "#6b7280", "fontSize": "14px"}),
            html.Div(id="botoes-paginacao-partidas", style={"display": "flex"})
        ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "padding": "15px", "backgroundColor": "#f9fafb", "borderTop": "1px solid #eaeaea", "borderBottomLeftRadius": "8px", "borderBottomRightRadius": "8px"})
        
    ], style={"backgroundColor": "#fcfcfd", "borderRadius": "8px", "border": "1px solid #eaeaea", "boxShadow": "0 2px 4px rgba(0,0,0,0.05)"})
    
], style={"maxWidth": "1200px", "margin": "0 auto", "padding": "20px"})
