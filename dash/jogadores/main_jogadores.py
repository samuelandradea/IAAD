from dash import html, Input, Output, callback, ctx
from dash.exceptions import PreventUpdate

from jogadores.tela_jogadores import tela_jogadores
from jogadores.cadastro_jogadores import tela_cadastro_jogadores
from jogadores.tela_UPDATE_jogadores import build_tela_editar

tela_principal_jogadores = html.Div([
    html.Div(tela_jogadores,          id='view-tabela',  style={'display': 'block'}),
    html.Div(tela_cadastro_jogadores, id='view-cadastro', style={'display': 'none'}),
    html.Div(id='view-edicao',                           style={'display': 'none'}),
])


@callback(
    Output('view-tabela',  'style'),
    Output('view-cadastro','style'),
    Output('view-edicao',  'style'),
    Input('btn-ir-cadastro',    'n_clicks'),
    Input('btn-cancelar',       'n_clicks'),
    Input('btn-cancelar-edicao','n_clicks'),
    Input('jogador-editando-id','data'),
    prevent_initial_call=True
)
def alternar_telas(click_cadastro, click_cancelar, click_cancelar_edicao, id_jogador):
    botao = ctx.triggered_id

    if botao == 'btn-ir-cadastro':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

    if botao in ('btn-cancelar', 'btn-cancelar-edicao'):
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    if botao == 'jogador-editando-id' and id_jogador:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}

    raise PreventUpdate