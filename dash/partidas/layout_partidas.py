from dash import html, dcc, Input, Output, ctx
import dash
from partidas.tela_partidas import tela_partidas
from partidas.tela_cadastro import tela_cadastro
from partidas.atualizar_partida import tela_atualizar_partida  

layout_partidas_container = html.Div([
    # Armazena o ID da partida que o usuário quer deletar temporariamente
    dcc.Store(id='id-partida-para-excluir-store', data=None),
    
    # Store invisível para forçar a tabela a recarregar após deletar
    dcc.Store(id='excluir-trigger-store', data=0),

    # Componente oficial do Dash para caixas de confirmação
    dcc.ConfirmDialog(
        id='confirmacao-exclusao-partida',
        message='Tem certeza que deseja deletar permanentemente esta partida?',
    ),

    html.Div(id='container-lista-partidas', children=tela_partidas, style={'display': 'block'}),
    html.Div(id='container-cadastro-partida', children=tela_cadastro, style={'display': 'none'}),
    html.Div(id='container-atualizar-partida', children=tela_atualizar_partida, style={'display': 'none'})
])

# Callback interno que controla a navegação local
@dash.callback(
    [Output('container-lista-partidas', 'style'),
     Output('container-cadastro-partida', 'style'),
     Output('container-atualizar-partida', 'style')],
    [Input('btn-cadastrar-partida', 'n_clicks'),
     Input('btn-cancelar-cadastro', 'n_clicks'),
     Input('btn-voltar-partidas', 'n_clicks'),
     Input({'type': 'btn-editar-partida', 'index': dash.ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def navegar_entre_telas_partidas(n_cad, n_can, n_vol, n_edit):
    triggered = ctx.triggered_id
    
    if triggered is None:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    
    if triggered == 'btn-cadastrar-partida' and n_cad:
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
        
    if triggered in ['btn-cancelar-cadastro', 'btn-voltar-partidas']:
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
        
    if isinstance(triggered, dict) and triggered.get('type') == 'btn-editar-partida':
        if any(x for x in n_edit if x is not None):
            return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
        
    return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
