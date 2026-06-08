from dash import html, Input, Output, callback, ctx

# Importa as suas telas
from jogadores.tela_jogadores import tela_jogadores
from jogadores.cadastro_jogadores import tela_cadastro_jogadores


tela_principal_jogadores = html.Div([
    html.Div(tela_jogadores, id='view-tabela', style={'display': 'block'}),
    html.Div(tela_cadastro_jogadores, id='view-cadastro', style={'display': 'none'})
])


@callback(
    [Output('view-tabela', 'style'),
     Output('view-cadastro', 'style')],
    [Input('btn-ir-cadastro', 'n_clicks'),
     Input('btn-cancelar', 'n_clicks')],
    prevent_initial_call=True
)
def alternar_telas(click_cadastro, click_cancelar):
    botao_clicado = ctx.triggered_id
    
    # Se clicou para cadastrar: Esconde a tabela, Mostra o cadastro
    if botao_clicado == 'btn-ir-cadastro':
        return {'display': 'none'}, {'display': 'block'}
        
    # Se clicou em cancelar: Mostra a tabela, Esconde o cadastro
    elif botao_clicado == 'btn-cancelar':
        return {'display': 'block'}, {'display': 'none'}
        
    # Padrão de segurança
    return {'display': 'block'}, {'display': 'none'}